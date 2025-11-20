"""
File management utilities for TTS Notify v2

This module provides file system utilities for managing audio files,
configurations, and paths.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
import platform
import tempfile
import shutil

from .text_normalizer import TextNormalizer


class FileManager:
    """File management utility with cross-platform support"""

    def __init__(self):
        self._system = platform.system()
        self._user_home = Path.home()
        self._desktop_path = self._get_desktop_path()

    def _get_desktop_path(self) -> Path:
        """Get the desktop path for the current platform"""
        if self._system == "Darwin":  # macOS
            return self._user_home / "Desktop"
        elif self._system == "Windows":
            # Try common Windows desktop paths
            desktop_paths = [
                self._user_home / "Desktop",
                Path(os.environ.get("USERPROFILE", "")) / "Desktop",
                Path(os.environ.get("HOME", "")) / "Desktop"
            ]
            for path in desktop_paths:
                if path.exists():
                    return path
            return self._user_home / "Desktop"  # Fallback
        else:  # Linux and others
            # Try common Linux desktop paths
            desktop_paths = [
                self._user_home / "Desktop",
                self._user_home / "Escritorio",  # Spanish
                Path(os.environ.get("XDG_DESKTOP_DIR", "")),
            ]
            for path in desktop_paths:
                if path.exists():
                    return path
            return self._user_home / "Desktop"  # Fallback

    def get_current_user(self) -> str:
        """Get the current system username"""
        try:
            # Try to get username from system
            result = subprocess.run(["whoami"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Fallback to environment variables
        return os.environ.get("USER", os.environ.get("USERNAME", "unknown"))

    def get_default_output_dir(self) -> Path:
        """Get the default output directory for audio files"""
        return self._desktop_path

    def ensure_directory_exists(self, path: Path) -> bool:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            path: Directory path to ensure exists

        Returns:
            True if directory exists or was created successfully
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    def get_unique_filename(self, base_name: str, extension: str, output_dir: Optional[Path] = None) -> Path:
        """
        Get a unique filename to avoid overwriting existing files.

        Args:
            base_name: Base name for the file
            extension: File extension (without dot)
            output_dir: Output directory (uses default if None)

        Returns:
            Unique file path
        """
        if output_dir is None:
            output_dir = self.get_default_output_dir()

        # Ensure output directory exists
        self.ensure_directory_exists(output_dir)

        # Sanitize filename
        safe_name = TextNormalizer.sanitize_filename(base_name)

        # Ensure extension doesn't have dot
        extension = extension.lstrip('.')

        filename = f"{safe_name}.{extension}"
        file_path = output_dir / filename

        # If file doesn't exist, return it
        if not file_path.exists():
            return file_path

        # Add timestamp to make unique
        import time
        timestamp = int(time.time())
        filename = f"{safe_name}_{timestamp}.{extension}"
        file_path = output_dir / filename

        return file_path

    def cleanup_temp_files(self, pattern: str = "tts_notify_*", older_than_hours: int = 24) -> int:
        """
        Clean up temporary files matching a pattern.

        Args:
            pattern: Glob pattern for files to clean up
            older_than_hours: Only clean files older than this many hours

        Returns:
            Number of files cleaned up
        """
        import time

        temp_dir = Path(tempfile.gettempdir())
        cleaned_count = 0
        cutoff_time = time.time() - (older_than_hours * 3600)

        try:
            for file_path in temp_dir.glob(pattern):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        cleaned_count += 1
                    except Exception:
                        pass  # Ignore individual file errors
        except Exception:
            pass  # Ignore temp directory errors

        return cleaned_count

    def get_file_size_human_readable(self, file_path: Path) -> str:
        """
        Get human-readable file size.

        Args:
            file_path: Path to file

        Returns:
            Human-readable file size string
        """
        if not file_path.exists():
            return "File not found"

        try:
            size_bytes = file_path.stat().st_size

            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
        except Exception:
            return "Unknown"

    def validate_audio_file(self, file_path: Path, min_size_bytes: int = 100) -> bool:
        """
        Validate that an audio file exists and has minimum size.

        Args:
            file_path: Path to audio file
            min_size_bytes: Minimum file size in bytes

        Returns:
            True if file appears valid
        """
        if not file_path.exists():
            return False

        try:
            file_size = file_path.stat().st_size
            return file_size >= min_size_bytes
        except Exception:
            return False

    def get_audio_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Get metadata for an audio file.

        Args:
            file_path: Path to audio file

        Returns:
            Dictionary with file metadata
        """
        metadata = {
            "exists": False,
            "size": 0,
            "size_human": "0 B",
            "created": None,
            "modified": None,
            "extension": "",
            "is_valid": False
        }

        try:
            if file_path.exists():
                stat = file_path.stat()
                metadata.update({
                    "exists": True,
                    "size": stat.st_size,
                    "size_human": self.get_file_size_human_readable(file_path),
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime,
                    "extension": file_path.suffix.lower(),
                    "is_valid": self.validate_audio_file(file_path)
                })
        except Exception:
            pass

        return metadata

    def backup_file(self, file_path: Path, backup_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Create a backup of a file.

        Args:
            file_path: File to backup
            backup_dir: Directory to store backup (uses file's directory if None)

        Returns:
            Path to backup file, or None if failed
        """
        if not file_path.exists():
            return None

        if backup_dir is None:
            backup_dir = file_path.parent

        self.ensure_directory_exists(backup_dir)

        try:
            import time
            timestamp = int(time.time())
            backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name

            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None

    def create_desktop_shortcut_macos(self, target_path: Path, shortcut_name: str) -> bool:
        """
        Create a desktop shortcut on macOS.

        Args:
            target_path: Target file or application
            shortcut_name: Name for the shortcut

        Returns:
            True if successful
        """
        if self._system != "Darwin":
            return False

        try:
            shortcut_path = self._desktop_path / f"{shortcut_name}.command"

            command = f'''#!/bin/bash
open "{target_path.absolute()}"
'''

            with open(shortcut_path, 'w') as f:
                f.write(command)

            # Make executable
            os.chmod(shortcut_path, 0o755)
            return True
        except Exception:
            return False

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information relevant to TTS operations.

        Returns:
            Dictionary with system information
        """
        info = {
            "platform": self._system,
            "user": self.get_current_user(),
            "home": str(self._user_home),
            "desktop": str(self._desktop_path),
            "python_version": platform.python_version(),
            "temp_dir": tempfile.gettempdir(),
        }

        # Check for macOS-specific features
        if self._system == "Darwin":
            try:
                # Check if say command is available
                result = subprocess.run(["which", "say"], capture_output=True, text=True)
                info["say_available"] = result.returncode == 0
                if result.returncode == 0:
                    info["say_path"] = result.stdout.strip()
            except Exception:
                info["say_available"] = False

        return info


# Global file manager instance
file_manager = FileManager()