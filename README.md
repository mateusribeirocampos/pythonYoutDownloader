# Universal Video Downloader

<div align="center">
  
![Python Universal Video Downloader](assets/video_downloader.png)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type Checker: mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)](https://mypy.readthedocs.io/)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-blue.svg)](https://flake8.pycqa.org/)
[![Testing: pytest](https://img.shields.io/badge/testing-pytest-green.svg)](https://docs.pytest.org/)
[![Packaging: pyproject.toml](https://img.shields.io/badge/packaging-pyproject.toml-orange.svg)](https://peps.python.org/pep-0518/)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/mateusribeirocampos/pythonYoutDownloader/graphs/commit-activity)

**A professional, interactive universal video downloader built with Python and yt-dlp**

*Supports YouTube, Vimeo, HLS/DASH streams, and Chunked/Segmented Videos*

</div>

---

## 🌟 Features

- **🎯 Interactive Terminal Interface** - User-friendly step-by-step process
- **🔗 Universal URL Support** - YouTube, Vimeo, HLS (.m3u8), DASH (.mpd), and direct video URLs
- **🧩 Segmented Video Support** - Automatic detection and download of chunked/segmented videos
- **📹 Quality Selection** - Choose from available video formats and resolutions
- **📁 Flexible Output** - Select custom download directory with auto-creation
- **📊 Video Information** - Display title, duration, views, and channel info
- **🔄 Retry Mechanism** - Automatic retry for failed segments and downloads
- **📈 Progress Tracking** - Real-time progress for both regular and segmented downloads
- **✅ URL Testing** - Pre-download validation to ensure video accessibility
- **🛡️ Robust Error Handling** - Comprehensive error management and user feedback
- **🏗️ Professional Architecture** - Clean, maintainable, and tested codebase

### 🆕 New in v3.0 - Advanced Bypass Edition

- **🔗 Chunked/Segmented Video Downloads** - Handle videos delivered in chunks/fragments
- **🌐 Generic URL Support** - Download from any video URL with embedded content
- **⚡ Enhanced Streaming** - Optimized for HLS (.m3u8) and DASH (.mpd) formats
- **🔍 Smart Detection** - Automatic platform and format detection
- **📦 Vimeo CDN Support** - Download individual chunks from Vimeo CDN URLs
- **🎯 Embed Page Support** - Extract videos from embed pages automatically

### 🛡️ NEW: Advanced Restriction Bypass System

- **🍪 Auto Cookie Detection** - Automatically extracts cookies from Chrome, Safari, Firefox
- **📱 Multiple User Agents** - Android, iOS, Smart TV, and Web clients for maximum compatibility
- **🌍 Geo-Restriction Bypass** - Multiple country bypass strategies
- **🔓 Age-Restriction Bypass** - Advanced techniques to access age-restricted content
- **🔄 Multi-Client Fallback** - 6+ different client strategies in cascade
- **🚀 Enhanced Retry Logic** - Up to 20 attempts per video with intelligent fallbacks
- **⚙️ YouTube API Optimization** - Latest InnerTube API configurations
- **🔐 Authentication Support** - Automatic login state detection and cookie management

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)

### Installation

```bash
# Clone the repository
git clone https://github.com/mateusribeirocampos/pythonYoutDownloader.git
cd pythonYoutDownloader

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\\Scripts\\activate

# Install dependencies
make install
# Or manually: pip install -r requirements.txt
```

### Usage

```bash
# Run the interactive downloader
python src/universal_video_downloader.py

# Or use make command
make run
```

---

## 📖 How It Works

The application guides you through a **3-step process**:

### Step 1: Video URL

- Enter a video URL (YouTube, Vimeo, or any embed page)
- Automatic validation and platform detection
- Support for chunked/segmented videos and streaming formats

### Step 2: Video Format

- View available quality options and formats
- Automatic detection of HLS/DASH segmented formats
- Optimized format selection for chunked videos

### Step 3: Output Directory

- Choose download location
- Automatic directory creation
- Path validation and confirmation

### Download Summary

- Review all settings before download
- Confirmation prompt
- Real-time download progress

---

## 🏗️ Project Structure

```bash
youtube-video-downloader/
├── 📄 README.md                 # Project documentation
├── ⚙️ pyproject.toml           # Modern Python packaging
├── 📦 requirements.txt         # Production dependencies  
├── 🛠️ requirements-dev.txt     # Development dependencies
├── 🔨 Makefile                 # Build automation
├── 🚫 .gitignore              # Git ignore patterns
│
├── 📁 src/                     # Source code
│   ├── 🔧 __init__.py         # Package initialization
│   └── 🎯 universal_video_downloader.py # Main application
│
├── 🧪 tests/                  # Test suite
│   ├── 🔧 __init__.py         # Test package init
│   ├── ✅ test_downloader.py  # Unit tests
│   ├── 🎮 demo.py             # Demo script
│   ├── 🔍 test_problematic_videos.py # Problematic video testing
│   └── 📺 test_segmented_video.py    # Segmented video testing
│
├── 📚 docs/                   # Documentation
│   ├── 🌍 ENVIRONMENT_SETUP_EN.md
│   ├── 🇧🇷 ENVIRONMENT_SETUP.md  
│   ├── 🌍 PACKAGE_MANAGEMENT_EN.md
│   └── 🇧🇷 PACKAGE_MANAGEMENT.md
│
└── 🎨 assets/                 # Static assets
    └── pythonYout.png
```

---

## 💻 Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Type checking
make type-check
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install production dependencies |
| `make install-dev` | Install development dependencies |
| `make test` | Run test suite |
| `make run` | Run the application |
| `make format` | Format code with Black |
| `make lint` | Run flake8 linting |
| `make type-check` | Run mypy type checking |
| `make clean` | Clean build artifacts |
| `make build` | Build distribution package |

---

## 🧪 Testing

```bash
# Run all tests
python tests/test_downloader.py

# Test segmented video functionality
python tests/test_segmented_video.py

# Test problematic video handling
python tests/test_problematic_videos.py

# Run demo
python tests/demo.py

# Run example scripts
python examples/segmented_video_example.py

# Or use pytest (if installed)
pytest tests/
```

### Test Coverage

- ✅ URL validation testing
- ✅ Segmented video download testing
- ✅ Problematic video handling
- ✅ Edge case handling
- ✅ Import verification
- ✅ Integration demos

---

## 📝 API Reference

### Core Functions

```python
from src.universal_video_downloader import (
    download_video,
    validate_youtube_url,
    test_video_url,
    get_advanced_youtube_config
)

# Validate YouTube URL
is_valid = validate_youtube_url("https://www.youtube.com/watch?v=VIDEO_ID")

# Test video accessibility with advanced bypass (NEW!)
success, info = test_video_url("https://www.youtube.com/watch?v=VIDEO_ID")
if success:
    print(f"✅ Video accessible: {info['title']}")
    print(f"⏱️ Duration: {info['duration']} seconds")
else:
    print(f"❌ Error: {info['suggestion']}")

# Download video (supports YouTube, Vimeo, HLS, and segmented videos)
success = download_video(
    url="https://www.youtube.com/watch?v=VIDEO_ID",  # or any supported URL
    output_path="./downloads",
    format_selector="best[height<=720]"
)

# Example with segmented video
success = download_video(
    url="https://videoaddress.com.br/aula-123",  # Generic embed page
    output_path="./downloads",
    format_selector="best"  # Automatically handles HLS/DASH formats
)

# Advanced configuration with custom settings (NEW!)
advanced_config = get_advanced_youtube_config(
    cookies_path="/path/to/cookies.txt",  # Optional: Manual cookies
    proxy="http://proxy:8080"            # Optional: Proxy server
)
```

### Advanced Bypass Strategies (NEW!)

The downloader now automatically employs multiple advanced strategies:

#### 🍪 **Cookie Management**

```python
# Automatic browser cookie extraction
# - Chrome: ~/Library/Application Support/Google/Chrome/Default/Cookies
# - Safari: ~/Library/Containers/com.apple.Safari/Data/Library/Cookies/
# - Firefox: ~/.mozilla/firefox/profiles/*/cookies.sqlite

# Manual cookie support
# 1. Export cookies from browser using extensions
# 2. Save as cookies.txt file
# 3. Pass to advanced config
```

#### 📱 **Multi-Client Strategy**

```python
# Client Priority Order (Automatic):
# 1. 🏆 Browser Cookie + Advanced Headers
# 2. 📱 Android Creator/Music clients
# 3. 🍎 iOS mobile clients
# 4. 📺 Smart TV embedded clients
# 5. 🌐 Standard web clients
# 6. ⚡ Minimal fallback

# Each client has specific User-Agents and API configs
# Bypasses different types of restrictions
```

#### 🌍 **Geographic & Age Bypass**

```python
# Geographic Bypass:
# - Multiple country IP masking (US, UK, etc.)
# - Regional header spoofing
# - DNS bypass techniques

# Age Restriction Bypass:
# - Embedded player extraction
# - Client combinations that skip age verification
# - Authentication-free access methods
```

#### ⚡ **Enhanced Retry Logic**

```python
# Retry Configuration:
# - Up to 6 different client strategies
# - 20 retry attempts per strategy
# - Fragment retries: 20 attempts
# - Socket timeout: 120 seconds
# - Intelligent error classification and fallback
```

### Configuration Options

```python
# yt-dlp format selectors
'best'                    # Best quality available (with advanced bypass)
'best[height<=720]'       # Max 720p quality
'best[height<=1080]'      # Max 1080p quality
'worst'                   # Lowest quality

# Advanced format options (NEW!)
'best[ext=mp4]'          # Best MP4 format
'best[height<=720][ext=mp4]'  # 720p MP4 specifically
```

---

## 🛡️ Error Handling

The application includes comprehensive error handling for:

- **Invalid URLs** - Clear validation messages
- **Network Issues** - Retry suggestions and troubleshooting
- **Permission Errors** - Directory creation and file access
- **Video Restrictions** - Geo-blocking and private videos
- **Format Unavailability** - Fallback options

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow **PEP 8** style guidelines
- Add **type hints** to all functions
- Write **comprehensive docstrings**
- Include **unit tests** for new features
- Update **documentation** as needed

---

## 📋 Requirements

### Runtime Dependencies

- `yt-dlp>=2023.1.6` - YouTube video downloading

### Development Dependencies

- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `flake8>=4.0.0` - Code linting
- `mypy>=0.950` - Type checking

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'yt_dlp'` | Run `pip install yt-dlp` in activated virtual environment |
| `Permission denied` when creating directory | Check write permissions or run with appropriate privileges |
| `Video unavailable` | Check if video is public and accessible in your region |
| `Invalid URL` error | Ensure URL follows YouTube format patterns |

### 🆕 Advanced Troubleshooting (Restriction Bypass)

#### 🔐 Authentication Required Errors

```bash
# Error: "Please sign in. Use --cookies-from-browser"
# Solution: The downloader automatically tries to extract cookies, but you can:

# 1. Make sure you're logged into YouTube in your browser
# 2. Close browser completely, then try downloading
# 3. For manual cookie export:
#    - Install browser extension: "Get cookies.txt LOCALLY"
#    - Export YouTube cookies to cookies.txt
#    - Place file in project directory
```

#### 🚫 "Content not available on this app" Errors

```bash
# The downloader now tries 6 different bypass strategies automatically:
# ✅ Strategy 1: Browser cookies + Advanced headers
# ✅ Strategy 2: Android Creator/Music clients
# ✅ Strategy 3: iOS mobile clients
# ✅ Strategy 4: Smart TV embedded clients
# ✅ Strategy 5: Standard web clients
# ✅ Strategy 6: Minimal fallback

# If ALL strategies fail, the video likely has severe restrictions:
# - Copyright protection
# - Region blocking (even with bypass)
# - Private/unlisted status
# - Platform-specific blocking
```

#### 🌍 Geographic Restrictions

```bash
# The downloader includes multiple geo-bypass methods:
# - IP masking (US/UK regions)
# - DNS bypass techniques
# - Regional header spoofing

# For additional geographic bypass:
# 1. Try different times of day
# 2. Use a VPN service
# 3. Check if video is region-locked permanently
```

#### ⚠️ Age-Restricted Content

```bash
# Advanced age bypass strategies are automatic:
# - Embedded player extraction
# - Client combinations that skip verification
# - Authentication-free methods

# If age bypass fails:
# 1. Ensure you're logged into YouTube (18+ account)
# 2. Try manual cookie export (see above)
# 3. Some content may require explicit age verification
```

### Getting Help

- 📖 Check our [documentation](docs/)
- 🐛 [Report bugs](https://github.com/mateusribeirocampos/pythonYoutDownloader/issues)
- 💡 [Request features](https://github.com/mateusribeirocampos/pythonYoutDownloader/issues)
- 💬 [Start discussions](https://github.com/mateusribeirocampos/pythonYoutDownloader/discussions)

---

## ⚖️ Legal & Ethics

### Important Notice

This software is intended for **educational purposes** and **personal use** only.

### Terms of Use

- ✅ **Personal backups** of your own content
- ✅ **Educational content** with proper permissions  
- ✅ **Public domain** videos
- ❌ **Copyrighted material** without permission
- ❌ **Commercial redistribution**
- ❌ **Terms of service violations**

### Responsibility

**Users are solely responsible** for ensuring their use complies with:

- YouTube's Terms of Service
- Local copyright laws
- Content creator rights
- Platform guidelines

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```bash
MIT License - Copyright (c) 2025 YouTube Video Downloader Team
Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Powerful video downloading library
- **Python Community** - For excellent tooling and libraries
- **Contributors** - Thank you for your valuable contributions

---

## 📊 Project Stats

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/mateusribeirocampos/pythonYoutDownloader)
![GitHub code size](https://img.shields.io/github/languages/code-size/mateusribeirocampos/pythonYoutDownloader)
![GitHub top language](https://img.shields.io/github/languages/top/mateusribeirocampos/pythonYoutDownloader)

**Made with ❤️ by the YouTube Video Downloader Team**

</div>

---

<div align="center">
  
### ⭐ Star this repository if you found it helpful!

[⬆️ Back to Top](#youtube-video-downloader)

</div>