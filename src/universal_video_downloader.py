#!/usr/bin/env python3
"""
Video Downloader (YouTube, Vimeo & Generic Videos)

A comprehensive video downloader supporting multiple platforms and formats using yt-dlp.
Supports segmented/chunked videos, streaming formats (HLS, DASH), and direct video URLs.
Allows downloading with configurable quality and metadata extraction.

Supported platforms:
    - YouTube (youtube.com, youtu.be)
    - Vimeo (vimeo.com, player.vimeo.com)
    - Generic video URLs (.mp4, .avi, .mkv, etc.)
    - Streaming formats (HLS .m3u8, DASH .mpd, segmented videos)

Features:
    - Automatic detection of video segments/chunks
    - Retry mechanism for failed segments
    - Progress tracking for segmented downloads
    - Multiple format/quality options
    - Metadata extraction

Dependencies:
    - yt-dlp: Library for video downloading
    - Python 3.8+

Usage:
    python universal_video_downloader.py
    
Or import as module:
    from universal_video_downloader import download_video
    download_video('https://www.youtube.com/watch?v=VIDEO_ID')
    download_video('https://vimeo.com/123456789')
    download_video('https://example.com/video.m3u8')  # HLS streaming

Author: Developed for educational purposes
Date: 2025
"""

import yt_dlp
import os
import re
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse
from pathlib import Path

def _check_and_update_ytdlp() -> None:
    """
    Checks for yt-dlp updates once a week using a timestamp cache file.
    Uses ~/.cache/ytdlp_last_update to avoid checking on every run.
    """
    cache_file = Path.home() / '.cache' / 'ytdlp_last_update'
    update_interval = timedelta(days=7)

    should_update = True
    if cache_file.exists():
        try:
            last_check = datetime.fromisoformat(cache_file.read_text().strip())
            if datetime.now() - last_check < update_interval:
                should_update = False
        except (ValueError, OSError):
            pass

    if not should_update:
        return

    print("🔄 Checking for yt-dlp updates (weekly check)...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp', '--quiet'],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            import importlib.metadata
            version = importlib.metadata.version('yt-dlp')
            print(f"✅ yt-dlp up to date (v{version})")
        else:
            print(f"⚠️  Could not update yt-dlp: {result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️  Update check failed (continuing anyway): {e}")
    finally:
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(datetime.now().isoformat())
        except OSError:
            pass


def load_cookies_from_browser() -> str:
    """
    Attempts to find and load cookies from common browser locations.

    Returns:
        str: Path to cookies file if found, None otherwise
    """
    # Common browser cookie locations
    home = Path.home()
    cookie_paths = [
        # Chrome/Chromium on macOS
        home / 'Library/Application Support/Google/Chrome/Default/Cookies',
        home / 'Library/Application Support/Chromium/Default/Cookies',
        # Chrome on Linux
        home / '.config/google-chrome/Default/Cookies',
        home / '.config/chromium/Default/Cookies',
        # Firefox on macOS
        home / 'Library/Application Support/Firefox/Profiles',
        # Firefox on Linux
        home / '.mozilla/firefox',
    ]

    for path in cookie_paths:
        if path.exists():
            if 'Firefox' in str(path) or 'firefox' in str(path):
                # For Firefox, need to find the profile directory
                if path.is_dir():
                    for profile_dir in path.iterdir():
                        if profile_dir.is_dir() and 'default' in profile_dir.name.lower():
                            cookies_db = profile_dir / 'cookies.sqlite'
                            if cookies_db.exists():
                                return str(cookies_db)
            else:
                # For Chrome/Chromium
                return str(path)

    return None

def get_advanced_youtube_config(cookies_path: str = None, proxy: str = None) -> dict:
    """
    Creates an advanced yt-dlp configuration for bypassing YouTube restrictions.

    Args:
        cookies_path (str): Path to cookies file
        proxy (str): Proxy URL (http://user:pass@host:port)

    Returns:
        dict: Advanced yt-dlp configuration
    """
    config = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,

        # JavaScript runtime for n-challenge solving (yt-dlp 2026+)
        # Tries to find node/bun in PATH; falls back gracefully if not found
        'remote_components': ['ejs:github'],

        # Network and retry options
        'retries': 15,
        'fragment_retries': 20,
        'extractor_retries': 10,
        'file_access_retries': 10,
        'socket_timeout': 120,

        # Geo-blocking bypass
        'geo_bypass': True,
        'geo_bypass_country': 'US',

        # Additional options
        'prefer_insecure': False,
        'no_check_certificate': False,
    }

    # Configure JS runtime for n-challenge (needed for yt-dlp 2026+)
    node_path = shutil.which('node')
    if node_path:
        config['js_runtimes'] = {'node': {'path': node_path}}

    # Use cookies directly from Chrome browser (more reliable than cookie file)
    config['cookiesfrombrowser'] = ('chrome',)

    # Add proxy if specified
    if proxy:
        config['proxy'] = proxy
        print(f"🌐 Using proxy: {proxy}")

    return config

def _progress_hook(d):
    """
    Progress hook for yt-dlp downloads, specially optimized for segmented videos.
    
    Args:
        d (dict): Download progress information from yt-dlp
    """
    if d['status'] == 'downloading':
        if 'fragment_index' in d and 'fragment_count' in d:
            # For segmented/chunked videos (like HLS, DASH)
            fragment_current = d['fragment_index']
            fragment_total = d['fragment_count']
            percent = (fragment_current / fragment_total) * 100
            print(f"\r🔗 Downloading chunk {fragment_current}/{fragment_total} ({percent:.1f}%)", end='', flush=True)
        elif '_percent_str' in d:
            # For regular downloads with percentage
            print(f"\r📥 Downloading: {d['_percent_str'].strip()}", end='', flush=True)
        elif '_total_bytes_str' in d and '_downloaded_bytes_str' in d:
            # For downloads with size information
            print(f"\r📥 Downloaded: {d['_downloaded_bytes_str']} / {d['_total_bytes_str']}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\n✅ Download finished: {d['filename']}")
    elif d['status'] == 'error':
        print(f"\n❌ Download error: {d.get('error', 'Unknown error')}")

def try_alternative_extraction_methods(url: str) -> list[str]:
    """
    Generate alternative URLs to try for problematic videos.
    
    Args:
        url (str): Original video URL
        
    Returns:
        list[str]: List of alternative URLs to try
    """
    alternatives = []
    
    # For Vimeo embed URLs
    if 'player.vimeo.com' in url:
        # Extract video ID and create standard Vimeo URL
        vimeo_id_match = re.search(r'/video/(\d+)', url)
        if vimeo_id_match:
            video_id = vimeo_id_match.group(1)
            alternatives.append(f"https://vimeo.com/{video_id}")
            alternatives.append(f"https://www.vimeo.com/{video_id}")
    
    # For standard Vimeo URLs, try embed format
    elif 'vimeo.com' in url and '/video/' not in url:
        vimeo_id_match = re.search(r'vimeo\.com/(\d+)', url)
        if vimeo_id_match:
            video_id = vimeo_id_match.group(1)
            alternatives.append(f"https://player.vimeo.com/video/{video_id}")
    
    return alternatives

def detect_vimeo_chunk(url: str) -> dict:
    """
    Detects if URL is a Vimeo CDN chunk and extracts metadata.
    
    Args:
        url (str): URL to analyze
        
    Returns:
        dict: Chunk information or empty dict if not a chunk
    """
    if 'vod-adaptive-ak.vimeocdn.com' not in url.lower():
        return {}
    
    # Extract chunk information
    chunk_info = {'is_chunk': True, 'original_url': url}
    
    # Extract video ID from path
    video_id_match = re.search(r'/([a-f0-9-]+)/v2/', url)
    if video_id_match:
        chunk_info['video_id'] = video_id_match.group(1)
    
    # Extract range information
    range_match = re.search(r'range=(\d+)-(\d+)', url)
    if range_match:
        chunk_info['range_start'] = int(range_match.group(1))
        chunk_info['range_end'] = int(range_match.group(2))
        chunk_info['chunk_size'] = chunk_info['range_end'] - chunk_info['range_start']
    
    # Extract file name
    filename_match = re.search(r'/([^/]+\.mp4)', url)
    if filename_match:
        chunk_info['filename'] = filename_match.group(1)
    
    return chunk_info

def create_vimeo_direct_download_config() -> dict:
    """
    Creates specific yt-dlp configuration for Vimeo CDN chunks.
        
    Returns:
        dict: yt-dlp configuration optimized for direct chunk download
    """
    return {
        'format': 'best',
        'outtmpl': '%(title)s_chunk.%(ext)s',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://player.vimeo.com/',
            'Sec-Ch-Ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        },
        # Bypass format selection issues
        'ignoreerrors': False,
        'no_warnings': False,
        'extractaudio': False,
        'audioformat': 'best',
        'prefer_ffmpeg': True,
        # Direct download without extraction
        'extract_flat': False,
        'force_url': True,
    }

def download_vimeo_chunk_direct(url: str, output_path: str, chunk_info: dict) -> bool:
    """
    Downloads a Vimeo CDN chunk directly using yt-dlp with optimized settings.
    
    Args:
        url (str): Vimeo CDN chunk URL
        output_path (str): Directory to save the chunk
        chunk_info (dict): Chunk metadata from detect_vimeo_chunk()
        
    Returns:
        bool: True if download was successful, False otherwise
    """
    print(f"🚀 Attempting direct chunk download...")
    
    # Create output directory if needed
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
            print(f"📁 Directory created: {output_path}")
        except OSError as e:
            print(f"❌ Error creating directory {output_path}: {e}")
            return False
    
    # Generate filename based on chunk info
    filename = chunk_info.get('filename', 'vimeo_chunk.mp4')
    if 'range_start' in chunk_info and 'range_end' in chunk_info:
        name_base = filename.replace('.mp4', '')
        filename = f"{name_base}_chunk_{chunk_info['range_start']}-{chunk_info['range_end']}.mp4"
    
    # Configure yt-dlp for direct chunk download
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_path, filename),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://player.vimeo.com/',
            'Sec-Ch-Ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        },
        # Skip format extraction issues
        'extract_flat': False,
        'ignoreerrors': True,
        'no_warnings': False,
        'retries': 10,
        'socket_timeout': 30,
        'progress_hooks': [_progress_hook],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 Downloading chunk: {filename}")
            print(f"🔗 Source: {url[:100]}...")
            
            # Download the chunk
            ydl.download([url])
            
            print(f"✅ Chunk downloaded successfully!")
            print(f"📂 File: {os.path.join(output_path, filename)}")
            
            # Show chunk information
            print(f"\n📊 Chunk Information:")
            print(f"   📦 Size: {chunk_info.get('chunk_size', 'unknown')} bytes")
            print(f"   📋 Range: {chunk_info.get('range_start', '?')}-{chunk_info.get('range_end', '?')}")
            if 'video_id' in chunk_info:
                print(f"   🎬 Video ID: {chunk_info['video_id']}")
            
            return True
            
    except yt_dlp.DownloadError as e:
        error_str = str(e)
        print(f"❌ Download error: {error_str}")
        
        # Provide specific suggestions for chunk download issues
        if "Requested format is not available" in error_str:
            print("💡 This chunk URL might require the full video context.")
            print("🔍 Try to find the original video page that contains this chunk.")
            
        elif "HTTP Error 403" in error_str or "HTTP Error 401" in error_str:
            print("💡 Authentication/permission error.")
            print("🔍 This chunk might be expired or require specific cookies.")
            
        elif "HTTP Error 404" in error_str:
            print("💡 Chunk not found.")
            print("🔍 The chunk URL might be expired or incorrect.")
            
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def suggest_full_video_from_chunk(chunk_info: dict) -> list[str]:
    """
    Suggests possible full video URLs based on chunk information.
    
    Args:
        chunk_info (dict): Chunk metadata from detect_vimeo_chunk()
        
    Returns:
        list[str]: Suggested URLs to try for the full video
    """
    suggestions = []
    
    if 'video_id' in chunk_info:
        video_id = chunk_info['video_id']
        
        # Convert chunk UUID to possible Vimeo video IDs
        # This is mostly speculative, but we can try common patterns
        suggestions.extend([
            f"https://vimeo.com/{video_id}",
            f"https://player.vimeo.com/video/{video_id}",
        ])
        
        # Try to extract numeric ID if present
        numeric_match = re.search(r'(\d+)', video_id)
        if numeric_match:
            numeric_id = numeric_match.group(1)
            suggestions.extend([
                f"https://vimeo.com/{numeric_id}",
                f"https://player.vimeo.com/video/{numeric_id}",
            ])
    
    return suggestions

def try_download_full_video_from_chunk(url: str, output_path: str) -> bool:
    """
    Attempts to find and download the full video from a chunk URL.
    
    Args:
        url (str): Original chunk URL
        output_path (str): Directory to save the video
        
    Returns:
        bool: True if successful, False otherwise
    """
    chunk_info = detect_vimeo_chunk(url)
    
    if not chunk_info.get('is_chunk'):
        print("❌ Not a recognized Vimeo chunk URL")
        return False
    
    print(f"\n🔍 Attempting to find full video from chunk...")
    print(f"📦 Chunk info: {chunk_info.get('video_id', 'unknown')}")
    
    suggestions = suggest_full_video_from_chunk(chunk_info)
    
    if not suggestions:
        print("❌ Could not generate video URL suggestions from chunk")
        return False
    
    print(f"🔗 Trying {len(suggestions)} possible full video URLs...")
    
    for i, suggested_url in enumerate(suggestions, 1):
        print(f"\n🔍 Attempt {i}: {suggested_url}")
        
        # Test if URL is accessible
        success, info = test_video_url(suggested_url)
        
        if success:
            print(f"✅ Found accessible video!")
            print(f"📺 Title: {info.get('title', 'N/A')}")
            
            # Ask user if they want to download this
            print(f"\n💡 This might be the full video containing your chunk.")
            download_choice = input("💾 Download this full video? (y/N): ").strip().lower()
            
            if download_choice in ['y', 'yes']:
                print(f"🚀 Downloading full video...")
                return download_video(suggested_url, output_path, 'best[height<=720]')
            else:
                print("⏭️ Skipping this video...")
                continue
        else:
            print(f"❌ Not accessible: {info.get('error', 'Unknown error')[:50]}...")
    
    print("❌ Could not find the full video from chunk information")
    return False

def validate_vimeo_url(url: str) -> bool:
    """
    Validates if a URL is a valid Vimeo video URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
        
    Example:
        >>> validate_vimeo_url('https://vimeo.com/123456789')
        True
        
        >>> validate_vimeo_url('https://player.vimeo.com/video/123456789')
        True
        
        >>> validate_vimeo_url('https://example.com')
        False
    """
    # Vimeo URL patterns
    vimeo_patterns = [
        r'vimeo\.com/(\d+)',
        r'player\.vimeo\.com/video/(\d+)',
        r'player\.vimeo\.com/([a-f0-9\-]{36})',  # For URLs like the one you mentioned
        r'vimeo\.com/channels/[\w-]+/(\d+)',
        r'vimeo\.com/groups/[\w-]+/videos/(\d+)',
    ]
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url
            parsed = urlparse(url)
        
        # Check if it's a Vimeo domain
        valid_domains = ['vimeo.com', 'www.vimeo.com', 'player.vimeo.com']
        if parsed.netloc not in valid_domains:
            return False
        
        # Check URL pattern and extract video ID
        for pattern in vimeo_patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # Vimeo video IDs can be numeric or UUID format
                if video_id.isdigit() or len(video_id) == 36:  # UUID length
                    return True
                
        return False
    except Exception:
        return False

def detect_platform(url: str) -> str:
    """
    Detects the video platform from URL.
    
    Args:
        url (str): Video URL to analyze
        
    Returns:
        str: Platform name ('youtube', 'vimeo', 'generic', 'unknown')
        
    Example:
        >>> detect_platform('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        'youtube'
        
        >>> detect_platform('https://vimeo.com/123456789')
        'vimeo'
        
        >>> detect_platform('https://videoaddress.com.br/video.m3u8')
        'generic'
        
        >>> detect_platform('https://example.com')
        'unknown'
    """
    if validate_youtube_url(url):
        return 'youtube'
    elif validate_vimeo_url(url):
        return 'vimeo'
    elif is_generic_video_url(url):
        return 'generic'
    else:
        return 'unknown'

def is_generic_video_url(url: str) -> bool:
    """
    Checks if URL might be a generic video URL (including segmented videos).
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if URL appears to be a video, False otherwise
    """
    # Common video file extensions and streaming formats
    video_extensions = [
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.m3u8', '.mpd', '.ts', '.m4s'  # Streaming formats
    ]
    
    # Check if URL ends with video extension
    parsed_url = urlparse(url.lower())
    path = parsed_url.path
    
    for ext in video_extensions:
        if path.endswith(ext):
            return True
    
    # Check for common streaming indicators in URL
    streaming_indicators = ['m3u8', 'mpd', 'segments', 'chunks', 'stream']
    for indicator in streaming_indicators:
        if indicator in url.lower():
            return True
    
    # Special case: Vimeo CDN chunks
    if 'vod-adaptive-ak.vimeocdn.com' in url.lower() and 'range=' in url.lower():
        return True
    
    # Special case: VideoAddress embed pages (contain embedded videos)
    if 'videoaddress.com.br' in url.lower() and ('aula' in url.lower() or 'video' in url.lower()):
        return True
    
    # Generic check: URLs that might contain embedded videos
    # Check for common patterns that indicate video content pages
    video_page_indicators = [
        'watch', 'video', 'play', 'stream', 'embed', 'player',
        'aula', 'lesson', 'course', 'lecture'  # Educational content
    ]
    
    for indicator in video_page_indicators:
        if indicator in url.lower():
            return True
    
    return False

def validate_video_url(url: str) -> bool:
    """
    Validates if a URL is a valid video URL from supported platforms.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    return validate_youtube_url(url) or validate_vimeo_url(url) or is_generic_video_url(url)

def validate_youtube_url(url: str) -> bool:
    """
    Validates if a URL is a valid YouTube video URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
        
    Example:
        >>> validate_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        True
        
        >>> validate_youtube_url('https://example.com')
        False
    """
    # YouTube URL patterns
    youtube_patterns = [
        r'(?:youtube\.com/watch\?v=|youtube\.com/embed/|youtu\.be/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*[&?]v=([a-zA-Z0-9_-]{11})',
    ]
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url
            parsed = urlparse(url)
        
        # Check if it's a YouTube domain
        valid_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
        if parsed.netloc not in valid_domains:
            return False
        
        # Check URL pattern and extract video ID
        for pattern in youtube_patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                # YouTube video IDs are exactly 11 characters long
                if len(video_id) == 11:
                    return True
                
        return False
    except Exception:
        return False

def get_available_formats(url: str) -> list:
    """
    Gets available video formats for a YouTube URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        list: List of available formats with resolution info
    """
    try:
        ydl_opts = get_advanced_youtube_config()
        ydl_opts['listformats'] = True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Filter video formats and organize by resolution
            video_formats = []
            resolutions_seen = set()
            
            for fmt in formats:
                if fmt.get('vcodec') != 'none' and fmt.get('height'):
                    height = fmt.get('height')
                    if height not in resolutions_seen:
                        video_formats.append({
                            'format_id': fmt.get('format_id'),
                            'resolution': f"{fmt.get('width', 'N/A')}x{height}",
                            'height': height,
                            'ext': fmt.get('ext', 'mp4'),
                            'filesize': fmt.get('filesize', 0)
                        })
                        resolutions_seen.add(height)
            
            # Sort by resolution (highest first)
            video_formats.sort(key=lambda x: x['height'], reverse=True)
            
            return video_formats
            
    except Exception as e:
        print(f"❌ Error getting formats: {e}")
        return []

def get_user_input_url() -> str:
    """
    Prompts user for video URL and validates it (supports YouTube, Vimeo, and generic video URLs).
    
    Returns:
        str: Valid video URL
    """
    while True:
        url = input("\n🔗 Enter video URL (YouTube, Vimeo, or direct video): ").strip()
        
        if not url:
            print("❌ URL cannot be empty!")
            continue
            
        platform = detect_platform(url)
        if platform != 'unknown':
            if platform == 'generic':
                print("✅ Valid video URL detected!")
                print("ℹ️  This appears to be a direct video URL or streaming link.")
            else:
                print(f"✅ Valid {platform.title()} URL!")
            return url
        else:
            print("❌ Invalid URL! Please enter a valid video URL.")
            print("   Valid examples:")
            print("   YouTube:")
            print("   - https://www.youtube.com/watch?v=VIDEO_ID")
            print("   - https://youtu.be/VIDEO_ID")
            print("   Vimeo:")
            print("   - https://vimeo.com/123456789")
            print("   - https://player.vimeo.com/video/123456789")
            print("   Direct/Streaming videos:")
            print("   - https://example.com/video.mp4")
            print("   - https://example.com/stream.m3u8 (HLS)")
            print("   - https://example.com/manifest.mpd (DASH)")

def get_user_format_choice(url: str) -> str:
    """
    Prompts user to choose video format/resolution.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Selected format string for yt-dlp
    """
    print("\n🔍 Getting available formats...")
    formats = get_available_formats(url)
    
    if not formats:
        print("⚠️  Could not get formats. Using default quality (720p).")
        return 'best[height<=720]'
    
    print("\n📹 Available formats:")
    print("0. Best quality available (recommended)")
    
    for i, fmt in enumerate(formats[:8], 1):  # Limit to 8 options
        size_info = ""
        if fmt['filesize'] > 0:
            size_mb = fmt['filesize'] / (1024 * 1024)
            size_info = f" (~{size_mb:.1f}MB)"
        print(f"{i}. {fmt['resolution']} ({fmt['ext']}){size_info}")
    
    while True:
        try:
            choice = input(f"\n🎯 Choose format (0-{min(len(formats), 8)}): ").strip()
            
            if choice == '0':
                # For HLS/segmented videos, use specific format strategy
                if any('hls-' in str(fmt.get('format_id', '')) for fmt in formats):
                    # Try to find the best single format for HLS to avoid ffmpeg requirement
                    video_formats = [f for f in formats if f.get('height') and f.get('height') > 0]
                    if video_formats:
                        # Get the highest quality video format
                        best_video = max(video_formats, key=lambda x: x.get('height', 0))
                        format_id = best_video.get('format_id', '')
                        print(f"ℹ️  Selected HLS format: {format_id}")
                        return format_id
                    else:
                        return 'mp4'  # Fallback for HLS
                else:
                    return 'best'
            
            choice_num = int(choice)
            if 1 <= choice_num <= min(len(formats), 8):
                selected_format = formats[choice_num - 1]
                
                # For HLS formats, use the specific format ID
                format_id = selected_format.get('format_id', '')
                if 'hls-' in str(format_id):
                    print(f"✅ Selected HLS format: {format_id}")
                    return format_id
                else:
                    format_string = f"best[height<={selected_format['height']}]"
                    print(f"✅ Selected: {selected_format['resolution']} ({selected_format['ext']})")
                    return format_string
            else:
                print(f"❌ Invalid choice! Enter a number between 0 and {min(len(formats), 8)}.")
                
        except ValueError:
            print("❌ Enter a valid number!")

def get_user_output_directory() -> str:
    """
    Prompts user for output directory.
    
    Returns:
        str: Selected output directory path
    """
    print(f"\n📁 Current directory: {os.path.abspath('.')}")
    
    while True:
        choice = input("\n📂 Enter directory path (or Enter to use current): ").strip()
        
        if not choice:
            return '.'
        
        # Expand user directory (~)
        choice = os.path.expanduser(choice)
        
        if os.path.exists(choice):
            if os.path.isdir(choice):
                print(f"✅ Directory selected: {os.path.abspath(choice)}")
                return choice
            else:
                print("❌ The specified path is not a directory!")
        else:
            create = input(f"📁 Directory '{choice}' does not exist. Create? (y/N): ").strip().lower()
            if create in ['y', 'yes']:
                try:
                    os.makedirs(choice, exist_ok=True)
                    print(f"✅ Directory created: {os.path.abspath(choice)}")
                    return choice
                except OSError as e:
                    print(f"❌ Error creating directory: {e}")
            else:
                print("❌ Choose an existing directory or allow creation of a new one.")

def test_video_url(url: str) -> tuple[bool, dict]:
    """
    Tests if a video URL is accessible and extractable by yt-dlp.
    Uses multiple fallback methods for problematic videos including advanced bypass techniques.

    Args:
        url (str): Video URL to test

    Returns:
        tuple[bool, dict]: (Success status, video info dict)
    """
    # Multiple configurations to try in order - from most advanced to basic
    test_configs = [
        # Ultra-advanced configuration with browser cookie extraction
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'cookiesfrombrowser': ('chrome',),  # Try Chrome cookies first
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator', 'android_music', 'android', 'web', 'ios', 'tv_embedded'],
                    'player_skip': ['configs', 'webpage'],
                    'skip': [],
                    'innertube_api_version': '1.20220908.01.00'
                }
            },
            'retries': 15,
            'fragment_retries': 20,
            'geo_bypass': True,
            'age_limit': None,
        },

        # Try Safari cookies if on macOS
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'cookiesfrombrowser': ('safari',),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                }
            },
            'retries': 10,
            'geo_bypass': True,
        },

        # Ultra-advanced configuration without cookies
        get_advanced_youtube_config(),

        # Mobile Android client (often less restricted)
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/17.31.35 (Linux; U; Android 11) gzip',
                'X-YouTube-Client-Name': '3',
                'X-YouTube-Client-Version': '17.31.35',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'innertube_api_version': '1.20220908.01.00'
                }
            },
            'retries': 10,
            'fragment_retries': 15,
            'geo_bypass': True,
        },

        # iOS client bypass (Apple devices often less restricted)
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/17.33.2 (iPhone14,3; U; CPU iOS 15_6 like Mac OS X)',
                'X-YouTube-Client-Name': '5',
                'X-YouTube-Client-Version': '17.33.2',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                }
            },
            'retries': 10,
            'geo_bypass': True,
        },

        # TV/Smart TV client (often bypasses many restrictions)
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (SMART-TV; LINUX; Tizen 2.4.0) AppleWebKit/538.1 (KHTML, like Gecko) Version/2.4.0 TV Safari/538.1',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv_embedded'],
                }
            },
            'retries': 10,
            'geo_bypass': True,
        },

        # Age-restricted bypass attempt
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_embedded'],
                    'skip': ['dash', 'hls']
                }
            },
            'age_limit': None,  # Try to bypass age restrictions
            'retries': 5,
        },

        # Standard web configuration with enhanced settings
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web']
                }
            },
            'retries': 5,
        },

        # Minimal fallback
        {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
    ]
    
    last_error = None
    
    for ydl_opts in test_configs:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return True, info
                
        except Exception as e:
            last_error = e
            error_str = str(e).lower()
            
            # For some errors, don't try other configs
            if any(term in error_str for term in ['private video', 'video removed', 'this video is unavailable']):
                break
                
            # Continue to next config for other errors
            continue
    
    # All configs failed, return detailed error info
    error_str = str(last_error)
    
    # Enhanced error handling with specific suggestions
    if 'oauth token' in error_str.lower():
        return False, {
            'error': error_str,
            'error_type': 'oauth_error',
            'suggestion': 'Vimeo OAuth authentication failed. This video may require special permissions or be restricted.',
            'help': 'Try using the webpage URL that embeds this video instead of the direct player URL.'
        }
    elif 'embed-only video' in error_str:
        return False, {
            'error': error_str,
            'error_type': 'embed_only',
            'suggestion': 'This video can only be played when embedded. Find the webpage that shows this video.',
            'help': 'Look for articles or pages that display this video and use that URL instead.'
        }
    elif 'private video' in error_str.lower():
        return False, {
            'error': error_str,
            'error_type': 'private',
            'suggestion': 'This video is private and cannot be downloaded.',
            'help': 'Only the video owner can access private videos.'
        }
    elif 'unavailable' in error_str.lower():
        return False, {
            'error': error_str,
            'error_type': 'unavailable',
            'suggestion': 'Video is unavailable. May be deleted, private, or geo-restricted.',
            'help': 'Check if the video exists and is accessible from your location.'
        }
    else:
        return False, {
            'error': error_str,
            'error_type': 'general',
            'suggestion': 'Unknown error occurred. The video may have restrictions or be inaccessible.',
            'help': 'Try a different video URL or check your internet connection.'
        }

def download_video(url: str, output_path: str = '.', format_selector: str = 'best[height<=720]') -> bool:
    """
    Downloads a video from supported platforms (YouTube, Vimeo) using yt-dlp.
    Supports segmented/chunked videos and streaming formats (DASH, HLS).
    
    Args:
        url (str): Video URL (YouTube, Vimeo, etc.)
        output_path (str): Directory to save the video (default: current directory)
        format_selector (str): Format selection string for yt-dlp
        
    Returns:
        bool: True if download was successful, False otherwise
        
    Example:
        >>> download_video('https://www.youtube.com/watch?v=EXAMPLE_VIDEO')
        True
        
        >>> download_video('https://vimeo.com/123456789')
        True
        
        >>> download_video('https://example.com/video', '/tmp')
        False
    """
    # Check if this is a Vimeo CDN chunk URL
    chunk_info = detect_vimeo_chunk(url)
    if chunk_info.get('is_chunk'):
        print(f"🔗 Detected Vimeo CDN chunk!")
        print(f"📦 Chunk size: {chunk_info.get('chunk_size', 'unknown')} bytes")
        print(f"📋 Range: {chunk_info.get('range_start', '?')}-{chunk_info.get('range_end', '?')}")
        
        # Use direct download approach for chunks
        chunk_success = download_vimeo_chunk_direct(url, output_path, chunk_info)
        
        # If chunk download failed, offer to try finding the full video
        if not chunk_success:
            print(f"\n💡 Chunk download failed. Would you like to try finding the full video?")
            try_full = input("🔍 Search for full video from chunk? (y/N): ").strip().lower()
            if try_full in ['y', 'yes']:
                return try_download_full_video_from_chunk(url, output_path)
        
        return chunk_success
    
    # Build download config based on the advanced base config (includes js_runtimes, remote_components, cookies)
    ydl_opts = get_advanced_youtube_config()
    ydl_opts.update({
        'format': format_selector,
        'outtmpl': os.path.join(output_path, '%(title).200s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,

        # Fragment/segment handling
        'fragment_retries': 15,
        'skip_unavailable_fragments': False,
        'keep_fragments': False,
        'abort_on_unavailable_fragment': True,

        # Network options
        'http_chunk_size': 10485760,    # 10MB chunks
        'concurrent_fragment_downloads': 1,

        # HLS/DASH
        'hls_prefer_native': True,
        'hls_use_mpegts': False,

        # Progress and output
        'progress_hooks': [_progress_hook],
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': False,
    })
    
    # Validate if output directory exists
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
            print(f"📁 Directory created: {output_path}")
        except OSError as e:
            print(f"❌ Error creating directory {output_path}: {e}")
            return False
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🔍 Extracting video information...")
            
            # Get video information without downloading
            info = ydl.extract_info(url, download=False)
            
            # Display video metadata
            title = info.get('title', 'N/A')
            duration = info.get('duration', 0)
            view_count = info.get('view_count', 0)
            uploader = info.get('uploader', 'N/A')
            upload_date = info.get('upload_date', 'N/A')
            
            print(f"📺 Title: {title}")
            print(f"⏱️  Duration: {duration // 60}:{duration % 60:02d} ({duration}s)")
            print(f"👁️  Views: {view_count:,}")
            print(f"📺 Channel: {uploader}")
            print(f"📅 Upload date: {upload_date}")
            
            # Confirm before download
            print(f"\n⬇️  Starting download...")
            
            # Perform the download
            ydl.download([url])
            
            print(f"✅ Download completed successfully!")
            print(f"📂 File saved to: {output_path}")
            return True
            
    except yt_dlp.DownloadError as e:
        print(f"❌ yt-dlp specific error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error downloading video: {str(e)}")
        return False

def main() -> None:
    """
    Main function to execute the video downloader with interactive terminal interface.
    
    Prompts user for:
    - Video URL (YouTube/Vimeo with validation)
    - Video format/resolution
    - Output directory
    
    Then downloads the video with the selected options.
    """
    print("🎬 Universal Video Downloader")
    print("=" * 60)
    print("📱 Interactive Video Downloader")
    print("🎯 Supports: YouTube, Vimeo, HLS/DASH streams, Direct videos")
    print("🔗 Handles segmented/chunked videos automatically")
    print("=" * 60)

    _check_and_update_ytdlp()

    try:
        # Step 1: Get and validate video URL
        print("\n🔸 STEP 1: Video URL")
        video_url = get_user_input_url()
        
        # Step 1.5: Test video URL accessibility
        print("\n🔍 Testing video URL accessibility...")
        success, info = test_video_url(video_url)
        if not success:
            error_type = info.get('error_type', 'general')
            print(f"❌ Cannot access video: {info.get('error', 'Unknown error')}")
            
            # Show specific suggestions based on error type
            if 'suggestion' in info:
                print(f"💡 Suggestion: {info['suggestion']}")
            if 'help' in info:
                print(f"🆘 Help: {info['help']}")
                
            # Special handling for OAuth errors
            if error_type == 'oauth_error':
                print("\n🔧 Troubleshooting OAuth errors:")
                print("   1. Try using a different Vimeo URL format")
                print("   2. Look for the webpage that embeds this video")
                print("   3. Some Vimeo videos require special permissions")
                print("   4. The video may be restricted or private")
            
            return
        else:
            print("✅ Video URL is accessible!")
            if 'title' in info:
                print(f"📺 Title: {info['title']}")
            
            # Show if video is segmented/chunked
            formats = info.get('formats', [])
            segmented_formats = [f for f in formats if f.get('fragments')]
            if segmented_formats:
                print(f"🔗 Detected {len(segmented_formats)} segmented/chunked formats")
                print("ℹ️  This video uses chunks - optimized download settings will be applied")
        
        # Step 2: Select video format/resolution
        print("\n🔸 STEP 2: Video format")
        format_selector = get_user_format_choice(video_url)
        
        # Step 3: Select output directory
        print("\n🔸 STEP 3: Output directory")
        output_directory = get_user_output_directory()
        
        # Show summary before download
        print("\n" + "=" * 50)
        print("📋 DOWNLOAD SUMMARY:")
        print(f"🔗 URL: {video_url}")
        print(f"🎯 Format: {format_selector}")
        print(f"📁 Destination: {os.path.abspath(output_directory)}")
        print("=" * 50)
        
        # Confirm before starting download
        confirm = input("\n▶️  Start download? (Y/n): ").strip().lower()
        if confirm in ['n', 'no']:
            print("❌ Download cancelled by user.")
            return
        
        # Execute the download
        print("\n🚀 Starting download...")
        success = download_video(video_url, output_directory, format_selector)
        
        if success:
            print("\n🎉 Download completed successfully!")
            print(f"📂 File saved to: {os.path.abspath(output_directory)}")
        else:
            print("\n💥 Download failed. Check the URL and try again.")
            exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Download interrupted by user.")
        print("👋 Goodbye!")
        exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try again or check your internet connection.")
        exit(1)


if __name__ == "__main__":
    main()