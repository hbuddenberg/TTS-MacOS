#!/usr/bin/env python3
"""
TTS Notify v2 - REST API Server

FastAPI-based REST API for TTS Notify v2 using the new modular architecture.
Provides comprehensive text-to-speech functionality via HTTP endpoints.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import from the new modular architecture
from core.config_manager import config_manager
from core.voice_system import VoiceManager, VoiceFilter
from core.tts_engine import MacOSTTSEngine
from core.models import TTSRequest, AudioFormat, Voice, Gender, VoiceQuality, Language
from core.exceptions import TTSNotifyError, VoiceNotFoundError, ValidationError, TTSError
from utils.logger import setup_logging, get_logger


# Pydantic models for API
class SpeakRequest(BaseModel):
    """Request model for text-to-speech"""
    text: str = Field(..., min_length=1, max_length=50000, description="Text to speak")
    voice: Optional[str] = Field(None, description="Voice name (flexible search)")
    rate: Optional[int] = Field(None, ge=100, le=300, description="Speech rate in WPM")
    pitch: Optional[float] = Field(None, ge=0.5, le=2.0, description="Pitch multiplier")
    volume: Optional[float] = Field(None, ge=0.0, le=1.0, description="Volume multiplier")


class SaveAudioRequest(BaseModel):
    """Request model for saving audio"""
    text: str = Field(..., min_length=1, max_length=50000, description="Text to convert")
    filename: str = Field(..., min_length=1, max_length=255, description="Output filename (without extension)")
    voice: Optional[str] = Field(None, description="Voice name (flexible search)")
    rate: Optional[int] = Field(None, ge=100, le=300, description="Speech rate in WPM")
    pitch: Optional[float] = Field(None, ge=0.5, le=2.0, description="Pitch multiplier")
    volume: Optional[float] = Field(None, ge=0.0, le=1.0, description="Volume multiplier")
    format: Optional[str] = Field("aiff", regex=r"^(aiff|wav|mp3|ogg|m4a|flac)$", description="Audio format")


class VoiceResponse(BaseModel):
    """Response model for voice information"""
    name: str
    gender: Optional[str]
    quality: Optional[str]
    language: Optional[str]
    description: Optional[str]


class SpeakResponse(BaseModel):
    """Response model for speak requests"""
    success: bool
    voice_used: str
    actual_rate: int
    message: str


class SaveAudioResponse(BaseModel):
    """Response model for save audio requests"""
    success: bool
    filename: str
    file_path: str
    format: str
    message: str


class StatusResponse(BaseModel):
    """Response model for server status"""
    status: str
    version: str
    voices_available: int
    config_profile: str
    server_mode: str


class TTSNotifyAPIServer:
    """FastAPI server for TTS Notify v2"""

    def __init__(self):
        self.config_manager = config_manager
        self.voice_manager = VoiceManager()
        self.tts_engine = MacOSTTSEngine()
        self.logger = None

        # Load configuration
        self.config = self.config_manager.get_config()

        # Setup logging
        self._setup_logging()

        # Create FastAPI app
        self.app = FastAPI(
            title="TTS Notify API",
            description="REST API for Text-to-Speech functionality on macOS",
            version="2.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )

        # Setup middleware
        self._setup_middleware()

        # Register routes
        self._register_routes()

    def _setup_logging(self):
        """Setup logging based on configuration"""
        setup_logging(
            level=getattr(self.config, 'TTS_NOTIFY_LOG_LEVEL', 'INFO'),
            verbose=getattr(self.config, 'TTS_NOTIFY_VERBOSE', False)
        )
        self.logger = get_logger(__name__)

        if self.logger:
            self.logger.info("TTS Notify API Server v2.0.0 starting up")

    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self):
        """Register API routes"""

        @self.app.get("/", response_model=Dict[str, Any])
        async def root():
            """Root endpoint with API information"""
            return {
                "name": "TTS Notify API",
                "version": "2.0.0",
                "description": "REST API for Text-to-Speech functionality on macOS",
                "endpoints": {
                    "speak": "/speak",
                    "save": "/save",
                    "voices": "/voices",
                    "status": "/status",
                    "config": "/config"
                },
                "docs": "/docs"
            }

        @self.app.get("/status", response_model=StatusResponse)
        async def get_status():
            """Get server status and information"""
            try:
                voices = await self.voice_manager.get_all_voices()
                return StatusResponse(
                    status="running",
                    version="2.0.0",
                    voices_available=len(voices),
                    config_profile=getattr(self.config, 'TTS_NOTIFY_PROFILE', 'default'),
                    server_mode="api"
                )
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Status endpoint error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/voices", response_model=List[VoiceResponse])
        async def get_voices(
            gender: Optional[str] = Query(None, regex="^(male|female)$", description="Filter by gender"),
            language: Optional[str] = Query(None, description="Filter by language"),
            quality: Optional[str] = Query(None, regex="^(basic|enhanced|premium|siri|neural)$", description="Filter by quality"),
            search: Optional[str] = Query(None, description="Search term for voice names")
        ):
            """Get available voices with optional filtering"""
            try:
                # Get all voices
                voices = await self.voice_manager.get_all_voices()

                # Apply filters
                if gender or language or quality:
                    voice_filter = VoiceFilter()
                    voices = voice_filter.filter_voices(
                        voices, gender=gender, language=language, quality=quality
                    )

                # Apply search filter
                if search:
                    search_lower = search.lower()
                    voices = [v for v in voices if search_lower in v.name.lower()]

                # Convert to response format
                voice_responses = []
                for voice in voices:
                    voice_response = VoiceResponse(
                        name=voice.name,
                        gender=voice.gender.value if voice.gender else None,
                        quality=voice.quality.value if voice.quality else None,
                        language=voice.language.value if voice.language else None,
                        description=getattr(voice, 'description', None)
                    )
                    voice_responses.append(voice_response)

                if self.logger:
                    self.logger.info(f"API get_voices: returned {len(voice_responses)} voices")

                return voice_responses

            except TTSNotifyError as e:
                if self.logger:
                    self.logger.error(f"API get_voices error: {e}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                if self.logger:
                    self.logger.exception("API get_voices unexpected error")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.post("/speak", response_model=SpeakResponse)
        async def speak_text(request: SpeakRequest):
            """Convert text to speech and play it"""
            try:
                # Create TTS request
                tts_request = TTSRequest(
                    text=request.text,
                    voice_name=request.voice or getattr(self.config, 'TTS_NOTIFY_VOICE', 'monica'),
                    rate=request.rate or getattr(self.config, 'TTS_NOTIFY_RATE', 175),
                    pitch=request.pitch or getattr(self.config, 'TTS_NOTIFY_PITCH', 1.0),
                    volume=request.volume or getattr(self.config, 'TTS_NOTIFY_VOLUME', 1.0),
                    language=getattr(self.config, 'TTS_NOTIFY_LANGUAGE', 'es')
                )

                # Validate request
                validation_errors = tts_request.validate()
                if validation_errors:
                    error_msg = "; ".join(validation_errors)
                    raise HTTPException(status_code=400, detail=f"Validation error: {error_msg}")

                # Speak text
                response = await self.tts_engine.speak(tts_request)

                result = SpeakResponse(
                    success=True,
                    voice_used=response.voice_used,
                    actual_rate=response.actual_rate,
                    message=f"Text spoken successfully with voice '{response.voice_used}'"
                )

                if self.logger:
                    self.logger.info(f"API speak_text: {request.text[:50]}... -> {response.voice_used}")

                return result

            except (VoiceNotFoundError, ValidationError, TTSError) as e:
                if self.logger:
                    self.logger.error(f"API speak_text error: {e}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                if self.logger:
                    self.logger.exception("API speak_text unexpected error")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.post("/save", response_model=SaveAudioResponse)
        async def save_audio(request: SaveAudioRequest, background_tasks: BackgroundTasks):
            """Convert text to audio file and return it"""
            try:
                # Validate format
                try:
                    audio_format = AudioFormat(request.format)
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Unsupported audio format: {request.format}")

                # Determine output path
                output_dir = Path(getattr(self.config, 'TTS_NOTIFY_OUTPUT_DIR', Path.home() / "Desktop"))
                output_path = output_dir / f"{request.filename}.{audio_format.value}"

                # Create TTS request
                tts_request = TTSRequest(
                    text=request.text,
                    voice_name=request.voice or getattr(self.config, 'TTS_NOTIFY_VOICE', 'monica'),
                    rate=request.rate or getattr(self.config, 'TTS_NOTIFY_RATE', 175),
                    pitch=request.pitch or getattr(self.config, 'TTS_NOTIFY_PITCH', 1.0),
                    volume=request.volume or getattr(self.config, 'TTS_NOTIFY_VOLUME', 1.0),
                    language=getattr(self.config, 'TTS_NOTIFY_LANGUAGE', 'es'),
                    output_format=audio_format,
                    output_path=str(output_path)
                )

                # Validate request
                validation_errors = tts_request.validate()
                if validation_errors:
                    error_msg = "; ".join(validation_errors)
                    raise HTTPException(status_code=400, detail=f"Validation error: {error_msg}")

                # Save audio
                response = await self.tts_engine.synthesize(tts_request)

                # Schedule cleanup of old files (optional)
                if self.logger:
                    self.logger.info(f"API save_audio: {request.text[:50]}... -> {output_path}")

                return SaveAudioResponse(
                    success=True,
                    filename=f"{request.filename}.{audio_format.value}",
                    file_path=str(output_path),
                    format=audio_format.value,
                    message=f"Audio saved successfully to {output_path}"
                )

            except (VoiceNotFoundError, ValidationError, TTSError) as e:
                if self.logger:
                    self.logger.error(f"API save_audio error: {e}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                if self.logger:
                    self.logger.exception("API save_audio unexpected error")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.get("/download/{filename}")
        async def download_file(filename: str):
            """Download generated audio file"""
            try:
                # Security check - ensure filename is safe
                safe_filename = Path(filename).name
                if safe_filename != filename:
                    raise HTTPException(status_code=400, detail="Invalid filename")

                # Look for file in output directory
                output_dir = Path(getattr(self.config, 'TTS_NOTIFY_OUTPUT_DIR', Path.home() / "Desktop"))
                file_path = output_dir / safe_filename

                if not file_path.exists():
                    raise HTTPException(status_code=404, detail="File not found")

                return FileResponse(
                    path=file_path,
                    filename=safe_filename,
                    media_type=f"audio/{file_path.suffix[1:]}"
                )

            except HTTPException:
                raise
            except Exception as e:
                if self.logger:
                    self.logger.error(f"API download_file error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.get("/config", response_model=Dict[str, Any])
        async def get_config():
            """Get current server configuration"""
            try:
                # Get MCP environment variables (safe for API)
                mcp_vars = self.config_manager.get_mcp_environment_variables()

                # Get system validation
                validation_issues = self.config_manager.validate_system()

                return {
                    "version": "2.0.0",
                    "profile": getattr(self.config, 'TTS_NOTIFY_PROFILE', 'default'),
                    "settings": mcp_vars,
                    "validation": {
                        "valid": len(validation_issues) == 0,
                        "issues": validation_issues
                    },
                    "features": {
                        "tts_enabled": getattr(self.config, 'TTS_NOTIFY_ENABLED', True),
                        "cache_enabled": getattr(self.config, 'TTS_NOTIFY_CACHE_ENABLED', True),
                        "streaming": getattr(self.config, 'TTS_NOTIFY_STREAMING', False)
                    }
                }

            except Exception as e:
                if self.logger:
                    self.logger.error(f"API get_config error: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.app.post("/config/reload")
        async def reload_config():
            """Reload server configuration"""
            try:
                self.config_manager.reload_config()
                self.config = self.config_manager.get_config()

                if self.logger:
                    self.logger.info("API configuration reloaded")

                return {"message": "Configuration reloaded successfully"}

            except Exception as e:
                if self.logger:
                    self.logger.error(f"API reload_config error: {e}")
                raise HTTPException(status_code=500, detail="Failed to reload configuration")

    def get_app(self) -> FastAPI:
        """Get the FastAPI app instance"""
        return self.app

    async def run(self, host: str = None, port: int = None):
        """Run the API server"""
        host = host or getattr(self.config, 'TTS_NOTIFY_API_HOST', 'localhost')
        port = port or getattr(self.config, 'TTS_NOTIFY_API_PORT', 8000)

        if self.logger:
            self.logger.info(f"Starting TTS Notify API Server on http://{host}:{port}")

        import uvicorn
        await uvicorn.run(self.app, host=host, port=port)


# Global server instance
api_server = TTSNotifyAPIServer()


async def main():
    """Main entry point for API server"""
    await api_server.run()


if __name__ == "__main__":
    asyncio.run(main())