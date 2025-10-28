#!/usr/bin/env python3
"""
Setup para instalar tts-macos como comando global
"""
from setuptools import setup
import os

# Leer el README para la descripción larga
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tts-macos',
    version='1.0.0',
    description='Text-to-Speech para macOS usando TTS nativo',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TTS macOS Project',
    author_email='',
    url='https://github.com/yourusername/mcp-tts-macos',
    license='MIT',
    
    # Scripts ejecutables
    scripts=['tts-macos'],
    
    # Clasificadores de PyPI
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Utilities',
    ],
    
    # Requisitos
    python_requires='>=3.10',
    install_requires=[],
    
    # Dependencias opcionales para el servidor MCP
    extras_require={
        'mcp': ['mcp>=1.0.0'],
    },
    
    # Keywords para búsqueda
    keywords='tts text-to-speech macos voice speech audio cli',
    
    # Entry points alternativos
    entry_points={
        'console_scripts': [
            'tts=tts-macos:main',
        ],
    },
)
