#!/usr/bin/env python3
"""
Enhanced IonicCube Decoder v2.0
Professional implementation with improved performance and reliability
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from easytoyou import IonicubeDecoder
from easytoyou.exceptions import EasyToYouError, LoginError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('decoder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        prog="easy-to-you-automation",
        description="Professional IonicCube Decoder using easytoyou.eu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -u username -p password -s /path/to/source -o /path/to/output
  python main.py -u user -p pass -s ./encoded_files -o ./decoded_files -w -v

For more information, visit: https://github.com/rbwtech/easy-to-you-automation
        """
    )
    
    parser.add_argument("-u", "--username", required=True, 
                       help="easytoyou.eu username")
    parser.add_argument("-p", "--password", required=True, 
                       help="easytoyou.eu password")
    parser.add_argument("-s", "--source", required=True, 
                       help="source directory containing ionCube files")
    parser.add_argument("-o", "--destination", 
                       help="destination directory (default: source_decoded)")
    parser.add_argument("-d", "--decoder", default="ic11php72",
                       help="decoder version (default: ic11php72)")
    parser.add_argument("-w", "--overwrite", action='store_true',
                       help="overwrite existing decoded files")
    parser.add_argument("-v", "--verbose", action='store_true',
                       help="enable verbose logging for debugging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Set default destination
    if not args.destination:
        source_name = os.path.basename(args.source.rstrip('/\\'))
        args.destination = f"{source_name}_decoded"
    
    # Validate source directory
    if not os.path.exists(args.source):
        logger.error(f"Source directory does not exist: {args.source}")
        return 1
    
    if not os.path.isdir(args.source):
        logger.error(f"Source path is not a directory: {args.source}")
        return 1
    
    logger.info("=" * 60)
    logger.info("Easy-To-You Automation v2.0")
    logger.info("Professional IonicCube Decoder")
    logger.info("=" * 60)
    logger.info(f"Source: {args.source}")
    logger.info(f"Destination: {args.destination}")
    logger.info(f"Decoder: {args.decoder}")
    logger.info(f"Overwrite: {args.overwrite}")
    logger.info("=" * 60)
    
    # Initialize decoder
    try:
        decoder = IonicubeDecoder(args.username, args.password, args.decoder)
        logger.info("Decoder initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize decoder: {e}")
        return 1
    
    # Start decoding process
    try:
        success = decoder.decode_directory(args.source, args.destination, args.overwrite)
        
        if success:
            logger.info("🎉 Decoding completed successfully!")
            logger.info(f"📊 Processed {decoder.processed_count} files")
            if decoder.not_decoded:
                logger.warning(f"⚠️  {len(decoder.not_decoded)} files failed to decode")
            logger.info(f"📁 Output directory: {args.destination}")
            return 0
        else:
            logger.error("❌ Decoding process failed")
            return 1
            
    except LoginError as e:
        logger.error(f"❌ Login failed: {e}")
        logger.error("Please check your username and password")
        return 1
    except EasyToYouError as e:
        logger.error(f"❌ Decoder error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("🛑 Process interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return 1

if __name__ == '__main__':
    exit(main())
