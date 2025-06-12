# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Issues

#### "Login failed" Error

```
❌ Login failed: Invalid credentials
```

**Solutions:**

1. **Verify credentials** on [easytoyou.eu](https://easytoyou.eu)
2. **Check account status** - ensure subscription is active
3. **Try logging in manually** on the website first
4. **Check for special characters** in password

#### "Your browser not supported" Error

```
❌ error: couldnt find upload form
Your browser not supported.You are probably using bots
```

**Solutions:**

1. **Use v2 script** (main.py) which has enhanced bot detection avoidance
2. **Update to latest version** of the script
3. **Try different decoder version**: `-d ic10php72`
4. **Wait and retry** - temporary rate limiting

### Upload and Processing Issues

#### "Couldn't find upload form" Error

```
❌ Could not find upload form
```

**Solutions:**

1. **Check easytoyou.eu website** for layout changes
2. **Try different decoder**: `-d ic11php72` or `-d ic10php72`
3. **Use verbose mode** to see detailed error: `-v`
4. **Check internet connection** and proxy settings

#### Files Fail to Upload

```
⚠️ Upload failed: Connection timeout
```

**Solutions:**

1. **Reduce batch size** (modify batch_size in source code)
2. **Check network stability**
3. **Retry with verbose logging**: `-v`
4. **Use legacy version**: `python scripts/easy4us.py`

### File Processing Issues

#### No IonicCube Files Detected

```
Found 0 ionCube encoded PHP files
```

**Solutions:**

1. **Verify files are actually IonicCube encoded**:
   ```bash
   grep -r "ionCube Loader" /path/to/files
   ```
2. **Check file extensions** - only `.php` files are processed
3. **Verify file permissions** - ensure files are readable

#### Some Files Not Decoded

```
⚠️ 15 files failed to decode
```

**Solutions:**

1. **Check log file** for specific errors:
   ```bash
   grep "ERROR" decoder.log
   ```
2. **Try failed files separately** with different decoder
3. **Some files may not be IonicCube encoded**
4. **Check file corruption** in original files

### Network and Connection Issues

#### Timeout Errors

```
❌ Network error during login: Connection timeout
```

**Solutions:**

1. **Check internet connection**
2. **Try again later** - server might be busy
3. **Use VPN** if geographical restrictions apply
4. **Configure proxy** if behind corporate firewall:
   ```bash
   export HTTP_PROXY=http://proxy:8080
   export HTTPS_PROXY=http://proxy:8080
   ```

#### SSL Certificate Errors

```
❌ SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**

1. **Update certificates**:
   ```bash
   pip install --upgrade certifi
   ```
2. **Update Python** to latest version
3. **Corporate firewall**: Contact IT for certificate bundle

### Performance Issues

#### Very Slow Processing

```
Processing 100 files taking 2+ hours
```

**Solutions:**

1. **Check network speed** - upload speed affects processing time
2. **Reduce file size** by processing in smaller chunks
3. **Use wired connection** instead of WiFi
4. **Process during off-peak hours**

#### High Memory Usage

```
Process using 2GB+ RAM
```

**Solutions:**

1. **Process smaller directories** at a time
2. **Close other applications**
3. **Update to v2** which has memory optimizations
4. **Use 64-bit Python** for large datasets

### Environment Issues

#### Import Errors

```
ModuleNotFoundError: No module named 'easytoyou'
```

**Solutions:**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Check Python path** in scripts

#### Permission Errors (Linux/macOS)

```
❌ Permission denied: '/path/to/output'
```

**Solutions:**

1. **Change directory permissions**:
   ```bash
   chmod 755 /path/to/output
   ```
2. **Run with appropriate user**
3. **Use --user flag** for pip installs

#### Windows-specific Issues

```
❌ 'python' is not recognized as an internal or external command
```

**Solutions:**

1. **Add Python to PATH** during installation
2. **Use full path**:
   ```cmd
   C:\Python38\python.exe scripts\main.py
   ```
3. **Use Python Launcher**:
   ```cmd
   py scripts\main.py
   ```

## Advanced Troubleshooting

### Debug Mode

```bash
# Enable maximum verbosity
python scripts/main.py -u user -p pass -s ./source -v

# Monitor all network requests
python scripts/main.py -u user -p pass -s ./source -v 2>&1 | tee debug.log
```

### Log Analysis

```bash
# Check successful uploads
grep "Successfully uploaded" decoder.log

# Check failed uploads
grep "failed to decode" decoder.log

# Check network errors
grep -i "network\|timeout\|connection" decoder.log

# Check progress
grep "Progress:" decoder.log | tail -5
```

### Manual Testing

```bash
# Test login only
python -c "
from src.easytoyou import IonicubeDecoder
decoder = IonicubeDecoder('user', 'pass')
print('Login successful!' if decoder.login() else 'Login failed!')
"
```

### Reset and Clean Start

```bash
# Clear any cached data
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
```

## Getting Additional Help

### Information to Collect

When reporting issues, please include:

1. **Operating system** and version
2. **Python version**: `python --version`
3. **Complete error message** and stack trace
4. **Command used** (without credentials)
5. **Log file contents** (without sensitive data)
6. **File types and sizes** being processed

### Where to Get Help

- **GitHub Issues**: [Report bugs](https://github.com/rbwtech/easy-to-you-automation/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/rbwtech/easy-to-you-automation/discussions)
- **Email Support**: [radipta111@gmail.com](mailto:radipta111@gmail.com)

### Before Reporting

1. **Search existing issues** for similar problems
2. **Try the latest version** of the script
3. **Test with minimal example** to isolate the issue
4. **Check easytoyou.eu status** and your account
