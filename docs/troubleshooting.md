Troubleshooting Guide
Common Issues and Solutions
Authentication Issues
"Login failed" Error
❌ Login failed: Invalid credentials
Solutions:

Verify credentials on easytoyou.eu
Check account status - ensure subscription is active
Try logging in manually on the website first
Check for special characters in password

"Your browser not supported" Error
❌ error: couldnt find upload form
Your browser not supported.You are probably using bots
Solutions:

Use v2 script (main.py) which has enhanced bot detection avoidance
Update to latest version of the script
Try different decoder version: -d ic10php72
Wait and retry - temporary rate limiting

Upload and Processing Issues
"Couldn't find upload form" Error
❌ Could not find upload form
Solutions:

Check easytoyou.eu website for layout changes
Try different decoder: -d ic11php72 or -d ic10php72
Use verbose mode to see detailed error: -v
Check internet connection and proxy settings

Files Fail to Upload
⚠️ Upload failed: Connection timeout
Solutions:

Reduce batch size (modify batch_size in source code)
Check network stability
Retry with verbose logging: -v
Use legacy version: python scripts/easy4us.py

File Processing Issues
No IonicCube Files Detected
Found 0 ionCube encoded PHP files
Solutions:

Verify files are actually IonicCube encoded:
bashgrep -r "ionCube Loader" /path/to/files

Check file extensions - only .php files are processed
Verify file permissions - ensure files are readable

Some Files Not Decoded
⚠️ 15 files failed to decode
Solutions:

Check log file for specific errors:
bashgrep "ERROR" decoder.log

Try failed files separately with different decoder
Some files may not be IonicCube encoded
Check file corruption in original files

Network and Connection Issues
Timeout Errors
❌ Network error during login: Connection timeout
Solutions:

Check internet connection
Try again later - server might be busy
Use VPN if geographical restrictions apply
Configure proxy if behind corporate firewall:
bashexport HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=http://proxy:8080

SSL Certificate Errors
❌ SSL: CERTIFICATE_VERIFY_FAILED
Solutions:

Update certificates:
bashpip install --upgrade certifi

Update Python to latest version
Corporate firewall: Contact IT for certificate bundle

Performance Issues
Very Slow Processing
Processing 100 files taking 2+ hours
Solutions:

Check network speed - upload speed affects processing time
Reduce file size by processing in smaller chunks
Use wired connection instead of WiFi
Process during off-peak hours

High Memory Usage
Process using 2GB+ RAM
Solutions:

Process smaller directories at a time
Close other applications
Update to v2 which has memory optimizations
Use 64-bit Python for large datasets

Environment Issues
Import Errors
ModuleNotFoundError: No module named 'easytoyou'
Solutions:

Install dependencies:
bashpip install -r requirements.txt

Use virtual environment:
bashpython -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

Check Python path in scripts

Permission Errors (Linux/macOS)
❌ Permission denied: '/path/to/output'
Solutions:

Change directory permissions:
bashchmod 755 /path/to/output

Run with appropriate user
Use --user flag for pip installs

Windows-specific Issues
❌ 'python' is not recognized as an internal or external command
Solutions:

Add Python to PATH during installation
Use full path:
cmdC:\Python38\python.exe scripts\main.py

Use Python Launcher:
cmdpy scripts\main.py

Advanced Troubleshooting
Debug Mode
bash# Enable maximum verbosity
python scripts/main.py -u user -p pass -s ./source -v

# Monitor all network requests

python scripts/main.py -u user -p pass -s ./source -v 2>&1 | tee debug.log
Log Analysis
bash# Check successful uploads
grep "Successfully uploaded" decoder.log

# Check failed uploads

grep "failed to decode" decoder.log

# Check network errors

grep -i "network\|timeout\|connection" decoder.log

# Check progress

grep "Progress:" decoder.log | tail -5
Manual Testing
bash# Test login only
python -c "
from src.easytoyou import IonicubeDecoder
decoder = IonicubeDecoder('user', 'pass')
print('Login successful!' if decoder.login() else 'Login failed!')
"
Reset and Clean Start
bash# Clear any cached data
rm -f decoder.log

# Use fresh virtual environment

rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Try with minimal test case

mkdir test_input

# Add one small ionCube file

python scripts/main.py -u user -p pass -s ./test_input -o ./test_output -v
Getting Additional Help
Information to Collect
When reporting issues, please include:

Operating system and version
Python version: python --version
Complete error message and stack trace
Command used (without credentials)
Log file contents (without sensitive data)
File types and sizes being processed

Where to Get Help

GitHub Issues: Report bugs
GitHub Discussions: Ask questions
Email Support: contact@triatech.net

Before Reporting

Search existing issues for similar problems
Try the latest version of the script
Test with minimal example to isolate the issue
Check easytoyou.eu status and your account
