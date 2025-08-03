from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

INPUT_FILE = "INPUT_URLS_SHEET"
OUTPUT_FILE = "OUTPUT_REPORT_SHEET"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

links_df = pd.read_excel(INPUT_FILE)
urls = links_df.iloc[:, 0].dropna().tolist()

report_data = []

for url in urls:
    print(f"Checking {url}...")
    try:
        driver.get(url)
        time.sleep(3) 

        images = driver.find_elements("tag name", "img")
        total_images = len(images)

        missing_alt_images = []
        for img in images:
            alt_text = img.get_attribute("alt")
            src = img.get_attribute("src")
            if not alt_text or alt_text.strip() == "":
                missing_alt_images.append(src)

        meta_description = ""
        meta_tag = driver.find_elements("xpath", "//meta[@name='description']")
        if meta_tag:
            meta_description = meta_tag[0].get_attribute("content") or "Missing"
        else:
            meta_description = "Missing"

        report_data.append({
            "Page URL": url,
            "Total Images": total_images,
            "Images Missing ALT": len(missing_alt_images),
            "Missing ALT Image URLs": ", ".join(missing_alt_images),
            "Meta Description": meta_description,
            "Meta Description Length": len(meta_description) if meta_description != "Missing" else 0
        })

    except Exception as e:
        report_data.append({
            "Page URL": url,
            "Total Images": "Error",
            "Images Missing ALT": "Error",
            "Missing ALT Image URLs": str(e),
            "Meta Description": "Error",
            "Meta Description Length": 0
        })

driver.quit()

report_df = pd.DataFrame(report_data)
report_df.to_excel(OUTPUT_FILE, index=False)
print(f"Report saved as {OUTPUT_FILE}")
