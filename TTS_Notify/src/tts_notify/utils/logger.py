"""
Logging utilities for TTS Notify v2

This module provides structured logging with configuration support.
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import json

from .file_manager import file_manager


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    console_output: bool = True,
    structured: bool = False
) -> logging.Logger:
    """
    Setup logging configuration for TTS Notify.

    Args:
        level: Logging level (DEBUG, INFO, WARN, ERROR)
        log_file: Optional log file path
        console_output: Whether to output to console
        structured: Whether to use structured JSON logging

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("tts_notify")
    logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatters
    if structured:
        formatter = StructuredFormatter()
    else:
        formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_manager.ensure_directory_exists(log_file.parent)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"tts_notify.{name}")


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',   # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        # Get the original formatted message
        formatted = super().format(record)

        # Add color based on log level
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            formatted = f"{color}{formatted}{reset}"

        return formatted


class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for logging"""

    def format(self, record):
        # Create structured log entry
        log_entry = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add exception information if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno',
                              'pathname', 'filename', 'module', 'lineno',
                              'funcName', 'created', 'msecs', 'relativeCreated',
                              'thread', 'threadName', 'processName', 'process',
                              'exc_info', 'exc_text', 'stack_info']:
                    log_entry[key] = value

        return json.dumps(log_entry, default=str)


class TTSLoggerAdapter(logging.LoggerAdapter):
    """Adapter for TTS-specific logging context"""

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        # Add TTS-specific context to log entries
        context = {
            'component': 'tts_notify',
            'version': '2.0.0',
            **self.extra
        }

        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra'].update(context)
        return msg, kwargs


class ContextLogger:
    """Context manager for adding logging context"""

    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.adapter = None

    def __enter__(self):
        self.adapter = TTSLoggerAdapter(self.logger, self.context)
        return self.adapter

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def log_function_call(logger: logging.Logger):
    """Decorator to log function calls with timing"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            import inspect

            start_time = time.time()
            func_name = func.__name__
            module_name = func.__module__

            logger.debug(f"Calling {func_name} with args={args}, kwargs={kwargs}")

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{func_name} completed successfully in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{func_name} failed after {duration:.3f}s: {e}")
                raise

        return wrapper

    return decorator


def configure_logging_from_config(config: Dict[str, Any]) -> logging.Logger:
    """
    Configure logging from a configuration dictionary.

    Args:
        config: Configuration dictionary

    Returns:
        Configured logger
    """
    level = config.get('TTS_NOTIFY_LOG_LEVEL', 'INFO')
    debug_mode = config.get('TTS_NOTIFY_DEBUG_MODE', False)
    verbose = config.get('TTS_NOTIFY_VERBOSE', False)

    # Determine log level
    if debug_mode:
        log_level = 'DEBUG'
    elif verbose:
        log_level = 'DEBUG'
    else:
        log_level = level

    # Determine log file
    log_file = None
    if config.get('TTS_NOTIFY_DEBUG_FILE'):
        log_file = Path(config['TTS_NOTIFY_DEBUG_FILE'])
    elif debug_mode or verbose:
        # Create debug log file in user's home
        log_file = file_manager._user_home / ".tts_notify_debug.log"

    return setup_logging(
        level=log_level,
        log_file=log_file,
        console_output=True,
        structured=config.get('TTS_NOTIFY_STRUCTURED_LOGGING', False)
    )


def get_audit_logger() -> logging.Logger:
    """
    Get a logger for auditing TTS operations.

    Returns:
        Audit logger instance
    """
    audit_logger = logging.getLogger("tts_notify.audit")

    # Only setup once
    if not audit_logger.handlers:
        # Create audit log file
        audit_log_file = file_manager._user_home / ".tts_notify_audit.log"
        file_manager.ensure_directory_exists(audit_log_file.parent)

        handler = logging.FileHandler(audit_log_file)
        formatter = StructuredFormatter()
        handler.setFormatter(formatter)
        audit_logger.addHandler(handler)
        audit_logger.setLevel(logging.INFO)

    return audit_logger


# Default logger for the module
logger = get_logger(__name__)