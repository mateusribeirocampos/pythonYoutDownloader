"""
YouTube Video Downloader Package

A simple and efficient YouTube video downloader using Python and yt-dlp.
"""

__version__ = "1.0.0"
__author__ = "YouTube Downloader Team"
__email__ = "contact@example.com"

from .youtube_downloader import download_video, validate_youtube_url

__all__ = ["download_video", "validate_youtube_url"]