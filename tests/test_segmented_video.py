#!/usr/bin/env python3
"""
Test script for segmented video downloads.
This script demonstrates how to download videos that come in segments/chunks.
"""

from src.universal_video_downloader import download_video, test_video_url, detect_platform

def test_url(url: str):
    """Test a URL and show its platform detection and accessibility."""
    print(f"\n🔍 Testing URL: {url}")
    print("-" * 60)
    
    # Detect platform
    platform = detect_platform(url)
    print(f"🎯 Platform detected: {platform}")
    
    # Test accessibility
    print("🔍 Testing accessibility...")
    success, info = test_video_url(url)
    
    if success:
        print("✅ URL is accessible!")
        print(f"📺 Title: {info.get('title', 'N/A')}")
        print(f"⏱️  Duration: {info.get('duration', 'N/A')} seconds")
        print(f"🎬 Formats available: {len(info.get('formats', []))}")
        
        # Check if it's segmented
        formats = info.get('formats', [])
        segmented_formats = [f for f in formats if f.get('fragments') is not None]
        if segmented_formats:
            print(f"🔗 Segmented formats found: {len(segmented_formats)}")
            for fmt in segmented_formats[:3]:  # Show first 3
                fragment_count = len(fmt.get('fragments', []))
                print(f"   - Format {fmt.get('format_id', 'N/A')}: {fragment_count} segments")
    else:
        print(f"❌ URL not accessible: {info.get('error', 'Unknown error')}")

def main():
    """Test various types of video URLs."""
    print("🧪 Video URL Testing Tool")
    print("=" * 60)
    
    # Test URLs - you can modify these for your testing
    test_urls = [
        # YouTube example
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        
        # The URL you provided (you can uncomment and test)
        # "https://videoaddress.com.br/ijs-aula-4744",
        
        # Generic HLS example (this is a sample, may not work)
        # "https://example.com/video.m3u8",
    ]
    
    for url in test_urls:
        test_url(url)
    
    # Interactive testing
    print("\n" + "=" * 60)
    print("🔍 Interactive Testing")
    print("Enter URLs to test (empty to quit):")
    
    while True:
        url = input("\n🔗 Enter URL: ").strip()
        if not url:
            break
        test_url(url)
        
        # Ask if user wants to try downloading
        download = input("\n💾 Try downloading this video? (y/N): ").strip().lower()
        if download in ['y', 'yes']:
            print("\n🚀 Starting download...")
            success = download_video(url, './downloads/', 'best[height<=720]')
            if success:
                print("✅ Download completed!")
            else:
                print("❌ Download failed!")

if __name__ == "__main__":
    main()