#!/usr/bin/env python3
"""
Test script specifically for problematic video downloads.
Tests various error conditions and recovery methods.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.universal_video_downloader import (
    test_video_url, 
    download_video, 
    detect_platform, 
    try_alternative_extraction_methods
)

def test_problematic_urls():
    """Test various problematic video URLs and show recovery suggestions."""
    
    print("🧪 Testing Problematic Video URLs")
    print("=" * 50)
    
    # Test cases for different error types
    test_cases = [
        {
            'url': 'https://player.vimeo.com/video/EXAMPLE_ID',
            'description': 'Vimeo Embed URL (OAuth issues)',
            'expected_error': 'oauth_error'
        },
        {
            'url': 'https://vimeo.com/EXAMPLE_ID', 
            'description': 'Direct Vimeo URL (same video)',
            'expected_error': 'oauth_error'
        },
        {
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'description': 'YouTube URL (should work)',
            'expected_error': None
        },
        {
            'url': 'https://vimeo.com/999999999999',
            'description': 'Non-existent Vimeo video',
            'expected_error': 'unavailable'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"📋 URL: {test_case['url']}")
        
        # Detect platform
        platform = detect_platform(test_case['url'])
        print(f"🎯 Platform: {platform}")
        
        # Test URL accessibility
        print("⚡ Testing accessibility...")
        success, info = test_video_url(test_case['url'])
        
        if success:
            print("✅ Video accessible!")
            print(f"📺 Title: {info.get('title', 'N/A')}")
            
            # Check for segments
            formats = info.get('formats', [])
            segmented = [f for f in formats if f.get('fragments')]
            if segmented:
                print(f"🔗 Segmented formats: {len(segmented)}")
        else:
            error_type = info.get('error_type', 'unknown')
            print(f"❌ Error type: {error_type}")
            print(f"💬 Error: {info.get('error', 'Unknown')[:100]}...")
            
            if 'suggestion' in info:
                print(f"💡 Suggestion: {info['suggestion']}")
            
            # Try alternative URLs for Vimeo
            if 'vimeo.com' in test_case['url']:
                alternatives = try_alternative_extraction_methods(test_case['url'])
                if alternatives:
                    print(f"🔄 Found {len(alternatives)} alternative URLs to try:")
                    for alt in alternatives:
                        print(f"   - {alt}")
        
        print("-" * 50)

def demonstrate_chunked_video_handling():
    """Demonstrate how the program handles chunked videos."""
    
    print("\n🔗 Chunked Video Handling Demo")
    print("=" * 50)
    
    print("""
📋 The enhanced downloader now includes:

🔧 Technical Improvements:
   • Multiple fallback configurations
   • Enhanced HTTP headers to avoid blocks
   • Increased retry counts for fragments (15 retries)
   • Sequential fragment downloads for stability
   • Longer timeout for slow connections (60s)
   • Native HLS downloader preference
   
🔗 Chunk-Specific Features:
   • Real-time progress for each chunk
   • Automatic fragment retry on failure
   • Smart error handling for missing segments
   • Optimized settings for HLS (.m3u8) and DASH (.mpd)
   
🛡️ Error Recovery:
   • OAuth token fallback methods
   • Alternative URL generation for Vimeo
   • Detailed error messages with suggestions
   • Geographic bypass attempts
   
📈 Progress Tracking:
   • "Downloading chunk X/Y" messages
   • Percentage completion for segmented downloads
   • Status updates for each fragment
""")

def interactive_troubleshooting():
    """Interactive troubleshooting for user's specific videos."""
    
    print("\n🔧 Interactive Troubleshooting")
    print("=" * 50)
    
    while True:
        url = input("\n🔗 Enter problematic video URL (or 'quit' to exit): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not url:
            continue
        
        print(f"\n🔍 Analyzing: {url}")
        
        # Step 1: Platform detection
        platform = detect_platform(url)
        print(f"🎯 Platform: {platform}")
        
        # Step 2: Test accessibility
        print("⚡ Testing accessibility...")
        success, info = test_video_url(url)
        
        if success:
            print("✅ Video is accessible!")
            print(f"📺 Title: {info.get('title', 'N/A')}")
            
            # Check if segmented
            formats = info.get('formats', [])
            segmented_formats = [f for f in formats if f.get('fragments')]
            
            if segmented_formats:
                print(f"🔗 Segmented video detected! ({len(segmented_formats)} formats)")
                print("ℹ️  This video will be downloaded in chunks with optimized settings.")
                
                # Ask if user wants to download
                download_choice = input("\n💾 Download this video? (y/N): ").strip().lower()
                if download_choice in ['y', 'yes']:
                    print("\n🚀 Starting optimized chunked download...")
                    
                    success = download_video(
                        url=url,
                        output_path='./downloads',
                        format_selector='best[height<=720]'
                    )
                    
                    if success:
                        print("✅ Download completed!")
                    else:
                        print("❌ Download failed - check error messages above")
            else:
                print("ℹ️  Regular (non-segmented) video format")
        else:
            error_type = info.get('error_type', 'unknown')
            print(f"❌ Error type: {error_type}")
            print(f"💬 {info.get('error', 'Unknown error')}")
            
            # Show suggestions
            if 'suggestion' in info:
                print(f"\n💡 Suggestion: {info['suggestion']}")
            if 'help' in info:
                print(f"🆘 Help: {info['help']}")
            
            # Show troubleshooting steps based on error type
            if error_type == 'oauth_error':
                print("\n🔧 OAuth Error Troubleshooting:")
                print("   1. This video may be private or restricted")
                print("   2. Try finding a webpage that embeds this video")
                print("   3. Some Vimeo videos require special permissions")
                print("   4. The video might only work when embedded")
                
                # Show alternative URLs
                alternatives = try_alternative_extraction_methods(url)
                if alternatives:
                    print(f"\n🔄 Try these alternative URLs:")
                    for alt in alternatives:
                        print(f"   - {alt}")

if __name__ == "__main__":
    test_problematic_urls()
    demonstrate_chunked_video_handling()
    interactive_troubleshooting()