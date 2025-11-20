"""
pytest configuration and fixtures for TTS Notify v2.0.0 tests
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_dir(temp_dir):
    """Create a mock configuration directory."""
    config_dir = temp_dir / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def mock_voices():
    """Mock voice data for testing."""
    from core.models import Voice, Gender, VoiceQuality, Language

    return [
        Voice(
            name="monica",
            gender=Gender.FEMALE,
            quality=VoiceQuality.BASIC,
            language=Language.ES
        ),
        Voice(
            name="jorge",
            gender=Gender.MALE,
            quality=VoiceQuality.ENHANCED,
            language=Language.ES
        ),
        Voice(
            name="alex",
            gender=Gender.MALE,
            quality=VoiceQuality.BASIC,
            language=Language.EN
        ),
        Voice(
            name="siri-female",
            gender=Gender.FEMALE,
            quality=VoiceQuality.PREMIUM,
            language=Language.EN
        )
    ]


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for TTS command testing."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = """monica es_ES    # Spanish voice
jorge es_ES    # Spanish voice
alex en_US    # English voice"""
    mock_result.stderr = ""

    with patch('subprocess.run', return_value=mock_result):
        yield mock_result


@pytest.fixture
def mock_environment_variables():
    """Mock environment variables for testing."""
    original_env = os.environ.copy()

    test_env = {
        'TTS_NOTIFY_VOICE': 'monica',
        'TTS_NOTIFY_RATE': '175',
        'TTS_NOTIFY_LANGUAGE': 'es',
        'TTS_NOTIFY_ENABLED': 'true',
        'TTS_NOTIFY_LOG_LEVEL': 'INFO'
    }

    os.environ.update(test_env)
    yield test_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_config_file(mock_config_dir):
    """Create a mock configuration file."""
    import yaml

    config_data = {
        'TTS_NOTIFY_VOICE': 'jorge',
        'TTS_NOTIFY_RATE': 200,
        'TTS_NOTIFY_LANGUAGE': 'es',
        'TTS_NOTIFY_QUALITY': 'enhanced'
    }

    config_file = mock_config_dir / "default.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)

    return config_file


@pytest.fixture
def mock_profile_file(mock_config_dir):
    """Create a mock profile configuration file."""
    import yaml

    profiles_data = {
        'profiles': {
            'test-profile': {
                'TTS_NOTIFY_VOICE': 'test-voice',
                'TTS_NOTIFY_RATE': 150,
                'TTS_NOTIFY_LOG_LEVEL': 'DEBUG'
            }
        }
    }

    profile_file = mock_config_dir / "profiles.yaml"
    with open(profile_file, 'w') as f:
        yaml.dump(profiles_data, f)

    return profile_file


@pytest.fixture
def mock_audio_file(temp_dir):
    """Create a mock audio file."""
    audio_file = temp_dir / "test.aiff"
    audio_file.write_bytes(b"mock audio data")
    return audio_file


# pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "macos_only: marks tests that only run on macOS"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on file location
        if "test_api.py" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "test_cli.py" in str(item.fspath):
            item.add_marker(pytest.mark.cli)
        elif "test_core.py" in str(item.fspath):
            item.add_marker(pytest.mark.core)

        # Add integration marker for tests that use external dependencies
        if "integration" in item.name or "Integration" in str(item.cls):
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)


# Skip macOS-specific tests on other platforms
def pytest_runtest_setup(item):
    """Setup for individual tests."""
    # Skip tests that require macOS if not on macOS
    if "macos_only" in item.keywords:
        import platform
        if platform.system() != "Darwin":
            pytest.skip("macOS-only test")