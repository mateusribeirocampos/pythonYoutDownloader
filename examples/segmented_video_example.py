#!/usr/bin/env python3
"""
Example script showing how to download segmented/chunked videos.

This script demonstrates the new capabilities of the Universal Video Downloader
for handling videos that come in segments (like HLS streams, DASH formats).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.universal_video_downloader import download_video, detect_platform, test_video_url

def example_segmented_download():
    """Example of downloading a segmented video."""
    
    print("🔗 Segmented Video Download Example")
    print("=" * 50)
    
    # Example URLs (you can modify these for testing)
    example_urls = {
        "YouTube (often segmented)": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "HLS Stream (example)": "https://example.com/video.m3u8",  # Replace with actual HLS URL
        "DASH Stream (example)": "https://example.com/manifest.mpd",  # Replace with actual DASH URL
    }
    
    print("\n📋 Example URLs for different types:")
    for desc, url in example_urls.items():
        platform = detect_platform(url)
        print(f"   {desc}: {platform}")
    
    print("\n🔍 Interactive Testing:")
    print("Enter a video URL to test segmented download capabilities.")
    print("Good examples include:")
    print("- YouTube videos (automatically handled)")
    print("- HLS streams (.m3u8 files)")
    print("- DASH streams (.mpd files)")
    print("- Any URL that serves video in chunks")
    
    while True:
        url = input("\n🔗 Enter video URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not url:
            continue
            
        # Detect platform
        platform = detect_platform(url)
        print(f"\n🎯 Platform detected: {platform}")
        
        # Test URL
        print("🔍 Testing URL accessibility...")
        success, info = test_video_url(url)
        
        if not success:
            print(f"❌ URL not accessible: {info.get('error', 'Unknown error')}")
            continue
            
        print("✅ URL is accessible!")
        
        # Show video info
        if 'title' in info:
            print(f"📺 Title: {info['title']}")
        if 'duration' in info:
            print(f"⏱️  Duration: {info['duration']} seconds")
            
        # Check for segmented formats
        formats = info.get('formats', [])
        segmented_formats = [f for f in formats if f.get('fragments')]
        
        if segmented_formats:
            print(f"🔗 Found {len(segmented_formats)} segmented formats!")
            print("📋 Segmented format details:")
            for fmt in segmented_formats[:3]:  # Show first 3
                fragment_count = len(fmt.get('fragments', []))
                quality = fmt.get('height', 'unknown')
                ext = fmt.get('ext', 'unknown')
                print(f"   - {quality}p {ext}: {fragment_count} segments")
        else:
            print("ℹ️  This video uses regular (non-segmented) format.")
            
        # Ask if user wants to download
        download_choice = input("\n💾 Download this video? (y/N): ").strip().lower()
        if download_choice in ['y', 'yes']:
            print("\n🚀 Starting download...")
            print("Note: For segmented videos, you'll see progress for each segment.")
            
            # Create downloads directory
            downloads_dir = "./downloads"
            os.makedirs(downloads_dir, exist_ok=True)
            
            # Start download with segment-optimized settings
            success = download_video(
                url=url,
                output_path=downloads_dir,
                format_selector='best[height<=720]'  # Good balance for testing
            )
            
            if success:
                print("✅ Download completed successfully!")
                print(f"📁 File saved to: {downloads_dir}")
            else:
                print("❌ Download failed. Check the error messages above.")

def explain_segmented_videos():
    """Explain what segmented videos are and how they work."""
    
    print("\n" + "=" * 60)
    print("📚 What are Segmented Videos?")
    print("=" * 60)
    
    print("""
🔗 Segmented videos are broken into small chunks for efficient streaming:

📋 Common formats:
   • HLS (.m3u8) - HTTP Live Streaming
   • DASH (.mpd) - Dynamic Adaptive Streaming over HTTP
   • YouTube's adaptive streaming
   • Vimeo's segmented delivery

⚡ Benefits:
   • Faster initial playback
   • Adaptive quality based on network
   • Better error recovery
   • Efficient bandwidth usage

🛠️ How this downloader handles them:
   • Automatically detects segments
   • Downloads each chunk sequentially
   • Shows progress per segment
   • Retries failed segments
   • Merges into final video file

💡 Examples of segmented URLs:
   • https://example.com/video.m3u8 (HLS playlist)
   • https://example.com/manifest.mpd (DASH manifest)
   • YouTube URLs (automatically segmented)
   • Live stream recordings
""")

if __name__ == "__main__":
    explain_segmented_videos()
    example_segmented_download()