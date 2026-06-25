#!/usr/bin/env python3

import os
import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from decoder import IonicubeDecoder
from exceptions import EasyToYouError, LoginError

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[
        logging.FileHandler("decoder.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="easy-to-you-automation",
        description="easy-to-you-automation v2.1 -- IonicCube batch decoder via easytoyou.eu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -u username -p password -s /path/to/source -o /path/to/output
  python main.py -u user -p pass -s ./encoded -o ./decoded -w -v
  python main.py -u user -p pass -s ./source --watermark "/* Custom Watermark */"
        """,
    )

    parser.add_argument("-u", "--username", required=True, help="easytoyou.eu username")
    parser.add_argument("-p", "--password", required=True, help="easytoyou.eu password")
    parser.add_argument("-s", "--source", required=True, help="source directory")
    parser.add_argument("-o", "--destination", help="output directory (default: source_decoded)")
    parser.add_argument("-d", "--decoder", default="ic11php72", help="decoder version (default: ic11php72)")
    parser.add_argument("-w", "--overwrite", action="store_true", help="overwrite existing decoded files")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose logging")
    parser.add_argument("--watermark", help="custom watermark text")
    parser.add_argument("--retry", type=int, default=4, metavar="N", help="max retry attempts per batch (default: 4)")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.destination:
        args.destination = os.path.basename(args.source.rstrip("/\\")) + "_decoded"

    if not os.path.isdir(args.source):
        logger.error(f"Source directory not found: {args.source}")
        return 1

    info_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info_table.add_column(style="dim")
    info_table.add_column(style="bold")
    info_table.add_row("Source", args.source)
    info_table.add_row("Output", args.destination)
    info_table.add_row("Decoder", args.decoder)
    info_table.add_row("Overwrite", str(args.overwrite))
    info_table.add_row("Max retries", str(args.retry))
    info_table.add_row("Watermark", "custom" if args.watermark else "RBW-Tech default")
    console.print(Panel(info_table, title="[bold]easy-to-you-automation[/]", border_style="cyan"))

    try:
        decoder = IonicubeDecoder(
            args.username,
            args.password,
            args.decoder,
            custom_watermark=args.watermark,
            max_retries=args.retry,
        )
    except Exception as e:
        logger.error(f"Failed to initialize decoder: {e}")
        return 1

    try:
        success = decoder.decode_directory(args.source, args.destination, args.overwrite)

        total    = getattr(decoder, "processed_count", 0)
        failed   = getattr(decoder, "not_decoded", [])

        summary = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        summary.add_column(style="dim")
        summary.add_column(justify="right", style="bold")
        summary.add_row("Decoded", f"[green]{total}[/]")
        summary.add_row("Failed", f"[red]{len(failed)}[/]")
        summary.add_row("Output", args.destination)
        console.print(Panel(
            summary,
            title="[bold]Done[/]",
            border_style="green" if not failed else "yellow",
        ))

        if failed:
            for f in failed:
                logger.warning(f"  FAILED: {f}")

        return 0 if success else 1

    except LoginError as e:
        logger.error(f"Login failed: {e}")
        return 1
    except EasyToYouError as e:
        logger.error(f"Decoder error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())

