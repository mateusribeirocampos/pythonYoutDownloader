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

def download_video(url: str, output_path: str = '.') -> bool:
    """
    Downloads a YouTube video using yt-dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video (default: current directory)
        
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
        # Format: best quality available up to 720p for space efficiency
        'format': 'best[height<=720]',
        
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
    Main function to execute the video downloader.
    
    Allows customization of URL and output directory via code.
    For interactive use, modify the variables below.
    """
    # Video configuration to be downloaded
    video_url = 'https://www.youtube.com/watch?v=-oBfkrpqW1M'  # Change to desired URL
    output_directory = '.'  # Current directory - change if needed
    
    print("🎬 YouTube Video Downloader")
    print("=" * 40)
    print(f"🔗 URL: {video_url}")
    print(f"📁 Output directory: {os.path.abspath(output_directory)}")
    print("=" * 40)
    
    # Execute the download
    success = download_video(video_url, output_directory)
    
    if success:
        print("\n🎉 Operation completed successfully!")
    else:
        print("\n💥 Download failed. Check the URL and try again.")
        exit(1)


if __name__ == "__main__":
    main()