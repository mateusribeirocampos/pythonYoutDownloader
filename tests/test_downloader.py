#!/usr/bin/env python3
"""
Test script for YouTube downloader functions.
Tests URL validation and format functionality without requiring user input.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from universal_video_downloader import validate_youtube_url

class TestYouTubeDownloader:
    """Test class for YouTube downloader functions"""
    
    def test_valid_youtube_urls(self):
        """Test validation of valid YouTube URLs"""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "youtube.com/watch?v=dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        for url in valid_urls:
            result = validate_youtube_url(url)
            assert result == True, f"Should be valid: {url}"
    
    def test_invalid_youtube_urls(self):
        """Test validation of invalid YouTube URLs"""
        invalid_urls = [
            "https://example.com",
            "https://vimeo.com/123456",
            "not a url",
            "",
            "youtube.com/watch?v=short"
        ]
        
        for url in invalid_urls:
            result = validate_youtube_url(url)
            assert result == False, f"Should be invalid: {url}"
    
    def test_edge_case_urls(self):
        """Test edge cases for URL validation"""
        edge_cases = [
            ("https://youtube.com/watch?v=", False),
            ("https://youtube.com/watch?", False),
            ("youtube.com/watch?v=dQw4w9WgXcQ123", False),  # Too long
            ("youtube.com/watch?v=dQw4w9WgXc", False),      # Too short
        ]
        
        for url, expected in edge_cases:
            result = validate_youtube_url(url)
            assert result == expected, f"URL: {url}, Expected: {expected}, Got: {result}"

def test_url_validation():
    """Test URL validation function (legacy function for backward compatibility)"""
    print("🧪 Testing URL validation...")
    
    # Valid URLs
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "youtube.com/watch?v=dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
    
    # Invalid URLs
    invalid_urls = [
        "https://example.com",
        "https://vimeo.com/123456",
        "not a url",
        "",
        "youtube.com/watch?v=short"
    ]
    
    print("✅ Testing valid URLs:")
    for url in valid_urls:
        result = validate_youtube_url(url)
        print(f"   {url}: {result}")
        assert result == True, f"Should be valid: {url}"
    
    print("❌ Testing invalid URLs:")
    for url in invalid_urls:
        result = validate_youtube_url(url)
        print(f"   {url}: {result}")
        assert result == False, f"Should be invalid: {url}"
    
    print("✅ All URL validation tests passed!")

def test_import():
    """Test if all functions can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from universal_video_downloader import (
            validate_youtube_url,
            get_available_formats,
            get_user_input_url,
            get_user_format_choice,
            get_user_output_directory,
            download_video
        )
        print("✅ All functions imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 YouTube Downloader Test Suite")
    print("=" * 40)
    
    # Test imports
    if not test_import():
        sys.exit(1)
    
    # Test URL validation
    test_url_validation()
    
    print("\n🎉 All tests completed successfully!")
    print("📋 Program is ready for interactive use.")
    print("💡 Run 'python src/universal_video_downloader.py' to use interactively.")