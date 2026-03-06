# 🛡️ File Malware Scanner

A simple Python script that detects malicious files by comparing their MD5 hash against a local database of known malware signatures.

---

## Requirements
- Python 3.x (no external libraries needed)

## Usage

1. Set the target file in `main()`:
```python
File = "YourFile.txt"
```
2. Run the script:
```bash
python scanner.py
```

## Example Output
```
md5 : 44d88612fea8a8f36de82e1278abb02f
Test.txt is Malicious
```

Note:The scanner only computes MD5 hashes. SHA1/SHA256/SHA512 entries in the database will not match until multi-algorithm support is added.

> **This tool is for educational purposes only.**
