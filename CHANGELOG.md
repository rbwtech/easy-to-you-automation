# Changelog

## [2.1.0] - 2026-06-25

### New Features
- Rich terminal progress bar with spinner, ETA, and file counter during decode
- `--retry N` CLI flag to configure max retry attempts per batch (default: 4)
- `max_retries` parameter on `IonicubeDecoder.__init__`

### Improvements
- Flatten package structure: `src/easytoyou/` -> `src/` (simpler imports)
- `_retry()` helper centralizes all retry logic with configurable backoff schedule
- `upload_files()` guarantees file handle cleanup via `finally` block
- `download_decoded_files()` wrapped in retry -- handles 522/timeout from server
- `process_directory_batch()` retries at the batch level, not just request level
- `clear_decoder_queue()` bounded to 5 passes, handles 404 cleanly
- `processed_count` only increments on confirmed success
- `main.py` shows Rich Panel for config summary and completion report
- `requirements.txt` trimmed to direct dependencies only

### Bug Fixes
- File handles leaked when upload POST raised an exception
- `processed_count` was incremented unconditionally even for failed batches
- Infinite loop risk in `clear_decoder_queue` replaced with bounded loop

### Breaking Changes
- Package import path changed from `from easytoyou import ...` to `from decoder import ...` when using the `src/` directory directly
- `scripts/easy4us.py` (legacy v1) removed

---

## [2.0.0] - 2025-06-12

### New Features
- Object-oriented decoder with session management and connection pooling
- Batch processing (20 files per batch) with automatic retry
- Custom watermark replacement (RBW-Tech header)
- Comprehensive exception hierarchy
- Type hints throughout

### Improvements
- Realistic browser headers to avoid bot detection
- Smart ionCube file detection before upload
- Detailed logging to console and file

### Bug Fixes
- "Your browser not supported" error via enhanced headers
- Upload form not found -- multiple fallback selectors
- Character encoding issues for non-UTF-8 PHP files

---

## [1.0.0] - 2025-06-12

- Initial release (`scripts/easy4us.py`)
- Basic ionCube decoding via easytoyou.eu
- Directory walking and batch upload
