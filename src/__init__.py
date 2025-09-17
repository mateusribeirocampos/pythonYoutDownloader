"""
Universal Video Downloader Package

A simple and efficient universal video downloader using Python and yt-dlp.
Supports YouTube, Vimeo, HLS/DASH streams, and segmented videos.
"""

__version__ = "3.0.0"
__author__ = "Universal Video Downloader Team"
__email__ = "contact@example.com"

from .universal_video_downloader import download_video, validate_youtube_url

__all__ = ["download_video", "validate_youtube_url"]