Usage Guide
Quick Start
Basic Command Structure
bashpython scripts/main.py -u USERNAME -p PASSWORD -s SOURCE_DIR -o OUTPUT_DIR [OPTIONS]
Essential Examples
Decode a Single Directory
bashpython scripts/main.py -u myuser -p mypass -s ./encoded_project -o ./decoded_project
Decode with Verbose Logging
bashpython scripts/main.py -u myuser -p mypass -s ./source -o ./output -v
Overwrite Existing Files
bashpython scripts/main.py -u myuser -p mypass -s ./source -o ./output -w
Advanced Usage
Different Decoder Versions
bash# For PHP 7.2 (older projects)
python scripts/main.py -u user -p pass -s ./source -d ic10php72

# For PHP 7.3+ (modern projects)

python scripts/main.py -u user -p pass -s ./source -d ic11php73
Large Directory Processing
bash# Process large directories with progress tracking
python scripts/main.py -u user -p pass -s ./large_webapp -o ./decoded_webapp -v

# Monitor progress in separate terminal

tail -f decoder.log | grep "Progress\|Error\|Success"
Legacy Version (v1)
bash# Use original easy4us script for compatibility
python scripts/easy4us.py -u user -p pass -s ./source -o ./output -w
Directory Structure Examples
WordPress Plugin/Theme
wp-plugin/
├── admin/
│ ├── admin.php # IonicCube encoded
│ └── functions.php # IonicCube encoded
├── includes/
│ ├── class-main.php # IonicCube encoded
│ └── helpers.php # Regular PHP
├── assets/
│ ├── css/ # Static files (copied as-is)
│ └── js/ # Static files (copied as-is)
└── plugin.php # IonicCube encoded
After decoding:
wp-plugin_decoded/
├── admin/
│ ├── admin.php # ✅ Decoded
│ └── functions.php # ✅ Decoded
├── includes/
│ ├── class-main.php # ✅ Decoded
│ └── helpers.php # 📄 Copied as-is
├── assets/ # 📁 Copied as-is
└── plugin.php # ✅ Decoded
E-commerce Platform
bash# Large e-commerce site with 500+ files
python scripts/main.py -u user -p pass -s ./magento_encoded -o ./magento_source -v

# Expected processing time: 15-30 minutes

# Expected success rate: 95%+

Monitoring and Logging
Real-time Progress Monitoring
bash# Terminal 1: Run decoder
python scripts/main.py -u user -p pass -s ./large_project -v

# Terminal 2: Monitor logs

tail -f decoder.log

# Terminal 3: Monitor specific events

tail -f decoder.log | grep -E "(Progress|Batch|Error)"
Log File Analysis
bash# Check for errors
grep "ERROR" decoder.log

# Check success rate

grep "Successfully uploaded" decoder.log | wc -l

# Check failed files

grep "failed to decode" decoder.log
Performance Optimization
Batch Size Tuning
The default batch size is 20 files. For different scenarios:

Small files (<100KB): Default (20) works well
Large files (>1MB): Consider reducing batch size
Slow network: Reduce batch size to 10-15
Fast network: Can increase to 25-30

Network Optimization
bash# For slow/unreliable connections
python scripts/main.py -u user -p pass -s ./source -v

# (Automatic retry will handle network issues)

# For corporate networks with proxies

# Set environment variables:

export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
Error Recovery
Resume Interrupted Process
bash# Simply rerun the same command - existing files are skipped automatically
python scripts/main.py -u user -p pass -s ./source -o ./output

# Force overwrite if needed

python scripts/main.py -u user -p pass -s ./source -o ./output -w
Handle Failed Files
bash# Check failed files in log
grep "failed to decode" decoder.log

# Try processing failed files separately

mkdir failed_files

# Copy failed files to separate directory

python scripts/main.py -u user -p pass -s ./failed_files -o ./retry_output -v
Integration Examples
Bash Script Integration
bash#!/bin/bash

# decode_project.sh

PROJECT_DIR="$1"
OUTPUT_DIR="${PROJECT_DIR}\_decoded"

echo "Starting decode of $PROJECT_DIR..."

python scripts/main.py \
 -u "$EASYTOYOU_USER" \
    -p "$EASYTOYOU_PASS" \
 -s "$PROJECT_DIR" \
    -o "$OUTPUT_DIR" \
 -v

if [ $? -eq 0 ]; then
echo "✅ Decode completed successfully!"
echo "📁 Output: $OUTPUT_DIR"
else
echo "❌ Decode failed!"
exit 1
fi
Python Script Integration
python#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

from easytoyou import IonicubeDecoder

def decode_project(source_dir, username, password):
"""Decode a project directory"""
decoder = IonicubeDecoder(username, password)

    output_dir = f"{source_dir}_decoded"
    success = decoder.decode_directory(source_dir, output_dir)

    if success:
        print(f"✅ Successfully decoded {decoder.processed_count} files")
        return output_dir
    else:
        print(f"❌ Decoding failed")
        return None

# Usage

if **name** == "**main**":
result = decode_project("./my_project", "username", "password")
Best Practices
Before Starting

Backup original files before decoding
Test with small directory first
Check easytoyou.eu account status and remaining quota
Ensure stable internet connection

During Processing

Don't interrupt the process unnecessarily
Monitor logs for any issues
Check available disk space for output
Avoid running multiple instances simultaneously

After Completion

Verify decoded files work correctly
Check log file for any warnings
Compare file counts between source and output
Test critical functionality of decoded application
