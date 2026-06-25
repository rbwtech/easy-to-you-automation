# easy-to-you-automation

Batch ionCube decoder automation via [easytoyou.eu](https://easytoyou.eu). Handles large PHP codebases with per-batch retry, exponential backoff, and integrity verification.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Requirements

- Python 3.8+
- Active [easytoyou.eu](https://easytoyou.eu) subscription

## Installation

```bash
git clone https://github.com/rbwtech/easy-to-you-automation.git
cd easy-to-you-automation
pip install -r requirements.txt
```

## Usage

```bash
python scripts/main.py -u USERNAME -p PASSWORD -s /path/to/encoded -o /path/to/decoded
```

Options:

| Flag          | Description                  | Default            |
| ------------- | ---------------------------- | ------------------ |
| `-u`          | easytoyou.eu username        | required           |
| `-p`          | easytoyou.eu password        | required           |
| `-s`          | source directory             | required           |
| `-o`          | output directory             | `{source}_decoded` |
| `-d`          | decoder version              | `ic11php74`        |
| `-w`          | overwrite existing files     | off                |
| `-v`          | verbose logging              | off                |
| `--retry N`   | max retry attempts per batch | 4                  |
| `--watermark` | custom watermark text        | RBW-Tech default   |

## Python API

```python
import sys
sys.path.insert(0, 'src')

from decoder import IonicubeDecoder

decoder = IonicubeDecoder("username", "password")
decoder.decode_directory("./encoded", "./decoded")

print(f"Decoded : {decoder.processed_count}")
print(f"Failed  : {len(decoder.not_decoded)}")
```

## Available decoders

| Value       | PHP target                      |
| ----------- | ------------------------------- |
| `ic10php72` | PHP 7.2 (IonCube 10)            |
| `ic11php72` | PHP 7.2 (IonCube 11)            |
| `ic11php73` | PHP 7.3 (IonCube 11)            |
| `ic11php74` | PHP 7.4 (IonCube 11) -- default |

Check [easytoyou.eu](https://easytoyou.eu) for the current list.

## Project structure

```
easy-to-you-automation/
├── scripts/
│   └── main.py        # CLI entrypoint with rich progress display
├── src/
│   ├── decoder.py     # IonicubeDecoder -- upload, download, watermark, retry
│   ├── session.py     # HTTP session management
│   ├── utils.py       # File discovery and batching utilities
│   ├── exceptions.py  # Custom exception hierarchy
│   └── __init__.py
├── requirements.txt
└── setup.py
```

## Monitoring

```bash
tail -f decoder.log | grep -E "Progress|Batch|Error|Warning"
```

## License

MIT -- see [LICENSE](LICENSE).

---

Built by [RBW-Tech](https://rbwtech.io).
