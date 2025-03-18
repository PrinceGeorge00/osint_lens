# OSINT-Lens

**OSINT-Lens** is an advanced OSINT (Open Source Intelligence) automation tool designed for cybersecurity professionals, ethical hackers, and researchers. It integrates multiple OSINT techniques, including reverse image search, metadata extraction, website fingerprinting, and bulk URL analysis.

## Features
- **Bulk Website Analysis**: Reads URLs from a file and performs OSINT checks.
- **Screenshot Capture**: Takes screenshots of target websites.
- **Technology Fingerprinting**: Uses WhatWeb to identify technologies used by websites.
- **Hidden Pages Extraction**: Fetches `robots.txt` to discover restricted pages.
- **Metadata Extraction**: Extracts EXIF data from images to identify location, camera details, and more.
- **Geolocation Mapping**: Extracts GPS coordinates and maps them.
- **Automated PDF Reporting**: Generates detailed reports including screenshots, metadata, and findings.

## Installation
### Prerequisites
- **Kali Linux** (or any Linux with necessary dependencies)
- **Python 3**
- **pip**
- **Google Chrome & ChromeDriver**
- **WhatWeb** (for website fingerprinting)
- **Tesseract-OCR** (for image text recognition)

### Install Required Packages
```bash
sudo apt update && sudo apt install -y python3-pip tesseract-ocr whatweb google-chrome-stable
pip install -r requirements.txt
```

## Usage
### Running OSINT-Lens
```bash
python osint_lens.py <url_list.txt>
```
- Replace `<url_list.txt>` with the file containing target URLs.
- Results will be saved in the `/reports/` folder.

### Example
```bash
python osint_lens.py targets.txt
```

## Output
- **Screenshots:** Saved in `/screenshots/`
- **Hidden Pages Report:** Saved as `reports/hidden_pages.json`
- **Technology Fingerprinting:** Saved as `reports/tech_fingerprints.json`
- **Full Report:** Saved as `reports/osint_report.pdf`

## Contributing
Feel free to fork, improve, and submit pull requests.

## License
MIT License

## Disclaimer
**OSINT-Lens** is for educational and ethical hacking purposes only. Do not use it on unauthorized systems.
