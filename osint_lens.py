import os
import time
import sys
import pytesseract
import cv2
import numpy as np
import requests
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from weasyprint import HTML
from geopy.geocoders import Nominatim
from exif import Image as ExifImage
import re

# Generate ASCII banner using 'toilet'
def generate_banner():
    try:
        banner = subprocess.check_output("toilet -f big -F metal osint_lens", shell=True).decode()
        print(banner)
    except Exception as e:
        print("Error generating banner:", e)

# Display the banner
generate_banner()


def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def fetch_robots_txt(url):
    robots_url = f"{url.rstrip('/')}/robots.txt"
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            return [line.split()[1] for line in response.text.splitlines() if line.startswith("Disallow") and len(line.split()) > 1]
        return []
    except requests.RequestException as e:
        print(f"Error fetching robots.txt from {url}: {e}")
        return []

def extract_exif_data(img_file):
    try:
        with open(img_file, "rb") as img:
            image = ExifImage(img)
            if image.has_exif:
                return {tag: getattr(image, tag) for tag in image.list_all() if getattr(image, tag)}
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
    return {}

def capture_screenshot(url, output_folder="screenshots"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/local/bin/chromedriver")  # Path to Chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(output_folder, f"screenshot_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    finally:
        driver.quit()

def get_tech_fingerprint(url):
    try:
        result = subprocess.run(["whatweb", "-a", "3", "--log-json=-", url], capture_output=True, text=True)
        output = result.stdout.strip()
        
        # Extract only the valid JSON part
        json_start = output.find("[")
        json_end = output.rfind("]") + 1
        if json_start != -1 and json_end != -1:
            json_part = output[json_start:json_end]
            try:
                parsed_json = json.loads(json_part)
                return parsed_json[0] if isinstance(parsed_json, list) else parsed_json
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for {url}: {e}\nExtracted JSON: {json_part}")
                return {}
        else:
            print(f"Warning: Could not extract valid JSON from WhatWeb output for {url}. Raw Output:\n{output}")
            return {}
    except Exception as e:
        print(f"Error running WhatWeb for {url}: {e}")
        return {}

def generate_pdf_report(hidden_pages, tech_fingerprints, output_folder="reports"):
    html_content = "<h1>OSINT Report</h1>"
    html_content += "<h2>Hidden Pages</h2>"
    for url, pages in hidden_pages.items():
        html_content += f"<h3>{url}</h3><ul>"
        for page in pages:
            html_content += f"<li>{page}</li>"
        html_content += "</ul>"
    
    html_content += "<h2>Technology Fingerprinting</h2>"
    for url, tech in tech_fingerprints.items():
        html_content += f"<h3>{url}</h3><pre>{json.dumps(tech, indent=4)}</pre>"
    
    report_path = os.path.join(output_folder, "osint_report.pdf")
    HTML(string=html_content).write_pdf(report_path)
    print(f"Report saved: {report_path}")

def process_bulk_urls(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    urls = read_urls_from_file(file_path)
    output_folder = "reports"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    hidden_pages = {}
    tech_fingerprints = {}
    for url in urls:
        _ = capture_screenshot(url, output_folder)
        hidden_pages[url] = fetch_robots_txt(url)
        tech_fingerprints[url] = get_tech_fingerprint(url)
    
    with open("reports/hidden_pages.json", "w") as f:
        json.dump(hidden_pages, f, indent=4)
    print("Hidden pages extracted and saved to reports/hidden_pages.json")
    
    with open("reports/tech_fingerprints.json", "w") as f:
        json.dump(tech_fingerprints, f, indent=4)
    print("Technology fingerprints extracted and saved to reports/tech_fingerprints.json")
    
    generate_pdf_report(hidden_pages, tech_fingerprints, output_folder)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing URL list file.\nUsage: python osint_lens.py <url_list.txt>")
        sys.exit(1)
    
    process_bulk_urls(sys.argv[1])

