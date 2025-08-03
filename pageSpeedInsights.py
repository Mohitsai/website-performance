import requests
import pandas as pd
import time

API_KEY = "PAGE_SPEED_INSIGHTS_API_KEY"
INPUT_FILE = "INPUT_URLS_SHEET"
COLUMN_NAME = " "

try:
    urls_df = pd.read_excel(INPUT_FILE)
    urls = urls_df[COLUMN_NAME].dropna().tolist()
except Exception as e:
    print(f"Error reading input file: {e}")
    urls = []

mobile_results = []
desktop_results = []

try:
    for url in urls:
        for strategy in ["mobile", "desktop"]:
            print(f"Analyzing {url} ({strategy})...")
            endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            params = {
                "url": url,
                "strategy": strategy,
                "category": ["performance", "accessibility", "seo"],
                "key": API_KEY
            }

            try:
                response = requests.get(endpoint, params=params, timeout=60)
            except requests.exceptions.ReadTimeout:
                print(f"Timeout for {url} ({strategy})")
                continue
            except requests.exceptions.RequestException as e:
                print(f"Request failed for {url} ({strategy}): {e}")
                continue

            if response.status_code == 429:
                print("Hit rate limit. Waiting 60 seconds...")
                time.sleep(60)
                try:
                    response = requests.get(endpoint, params=params, timeout=60)
                except requests.exceptions.RequestException as e:
                    print(f"Retry failed for {url} ({strategy}): {e}")
                    continue

            if response.status_code != 200:
                print(f"Error {response.status_code} for {url} ({strategy}). Skipping.")
                continue

            data = response.json()
            categories = data.get("lighthouseResult", {}).get("categories", {})
            audits = data.get("lighthouseResult", {}).get("audits", {})

            perf_score = categories.get("performance", {}).get("score")
            acc_score  = categories.get("accessibility", {}).get("score")
            seo_score  = categories.get("seo", {}).get("score")

            if perf_score is not None:
                perf_score *= 100
            if acc_score is not None:
                acc_score *= 100
            if seo_score is not None:
                seo_score *= 100

            speed_index = audits.get("speed-index", {}).get("numericValue")
            lcp         = audits.get("largest-contentful-paint", {}).get("numericValue")
            tti         = audits.get("interactive", {}).get("numericValue")
            tbt         = audits.get("total-blocking-time", {}).get("numericValue")
            cls         = audits.get("cumulative-layout-shift", {}).get("numericValue")

            result = {
                "URL": url,
                "Performance_Score": perf_score,
                "Accessibility_Score": acc_score,
                "SEO_Score": seo_score,
                "Speed_Index(ms)": speed_index,
                "LCP(ms)": lcp,
                "TTI(ms)": tti,
                "TBT(ms)": tbt,
                "CLS": cls
            }

            if strategy == "mobile":
                mobile_results.append(result)
            else:
                desktop_results.append(result)

except KeyboardInterrupt:
    print("\nInterrupted by user. Saving current results...")

finally:
    df_mobile = pd.DataFrame(mobile_results)
    df_desktop = pd.DataFrame(desktop_results)

    output_file = "pagespeed_results.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_mobile.to_excel(writer, sheet_name="Mobile", index=False)
        df_desktop.to_excel(writer, sheet_name="Desktop", index=False)

    print(f"Done! Partial results saved to {output_file}")