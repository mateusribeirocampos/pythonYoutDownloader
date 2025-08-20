#!/usr/bin/env python3
"""
YouTube Video Downloader

A simple and efficient downloader for YouTube videos using yt-dlp.
Allows downloading videos with configurable quality and metadata extraction.

Dependencies:
    - yt-dlp: Library for video downloading
    - Python 3.8+

Usage:
    python youtube_downloader.py
    
Or import as module:
    from youtube_downloader import download_video
    download_video('https://www.youtube.com/watch?v=VIDEO_ID')

Author: Developed for educational purposes
Date: 2025
"""

import yt_dlp
import os
import re
from urllib.parse import urlparse, parse_qs

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
        ydl_opts = {
            'listformats': True,
            'quiet': True,
            'no_warnings': True,
        }
        
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
    Prompts user for YouTube URL and validates it.
    
    Returns:
        str: Valid YouTube URL
    """
    while True:
        url = input("\n🔗 Enter YouTube URL: ").strip()
        
        if not url:
            print("❌ URL cannot be empty!")
            continue
            
        if validate_youtube_url(url):
            print("✅ Valid URL!")
            return url
        else:
            print("❌ Invalid URL! Please enter a valid YouTube URL.")
            print("   Valid examples:")
            print("   - https://www.youtube.com/watch?v=VIDEO_ID")
            print("   - https://youtu.be/VIDEO_ID")
            print("   - youtube.com/watch?v=VIDEO_ID")

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
                return 'best'
            
            choice_num = int(choice)
            if 1 <= choice_num <= min(len(formats), 8):
                selected_format = formats[choice_num - 1]
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

def download_video(url: str, output_path: str = '.', format_selector: str = 'best[height<=720]') -> bool:
    """
    Downloads a YouTube video using yt-dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video (default: current directory)
        format_selector (str): Format selection string for yt-dlp
        
    Returns:
        bool: True if download was successful, False otherwise
        
    Example:
        >>> download_video('https://www.youtube.com/watch?v=-oBfkrpqW1M')
        True
        
        >>> download_video('https://youtube.com/watch?v=invalid', '/tmp')
        False
    """
    # yt-dlp configuration
    ydl_opts = {
        # Format: use the provided format selector
        'format': format_selector,
        
        # File name template: uses video title
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        
        # Additional options for better experience
        'extractaudio': False,          # Keep video (don't extract audio only)
        'audioformat': 'mp3',           # Audio format if extracting
        'embed_subs': True,             # Embed subtitles if available
        'writesubtitles': False,        # Don't save subtitles as separate file
        'ignoreerrors': False,          # Stop on error
    }
    
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
    - YouTube URL (with validation)
    - Video format/resolution
    - Output directory
    
    Then downloads the video with the selected options.
    """
    print("🎬 YouTube Video Downloader")
    print("=" * 50)
    print("📱 Interactive YouTube Video Downloader")
    print("=" * 50)
    
    try:
        # Step 1: Get and validate YouTube URL
        print("\n🔸 STEP 1: Video URL")
        video_url = get_user_input_url()
        
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