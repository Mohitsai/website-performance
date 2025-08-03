import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from openpyxl import load_workbook

input_excel = 'INPUT_URLS_SHEET'
output_excel = 'OUTPUT_URLS_SHEET'

input_df = pd.read_excel(input_excel)
urls = input_df['webpages'].dropna().tolist()

results = []

for url in urls:
    print(f"Processing: {url}")

    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        # === IMAGES ===
        img_tags = soup.find_all("img")
        image_sizes = []

        for img in img_tags:
            img_url = img.get("src")
            if not img_url:
                continue
            img_url = urljoin(url, img_url)

            size_bytes = None

            try:
                head = requests.head(img_url, timeout=10)
                head.raise_for_status()
                size_header = head.headers.get("Content-Length")
                if size_header:
                    size_bytes = int(size_header)
                else:
                    img_response = requests.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    size_bytes = len(img_response.content)

            except Exception as e:
                print(f"  [Image Error] {img_url}: {e}")

            if size_bytes:
                image_sizes.append(size_bytes)

        num_images = len(image_sizes)
        max_image_size = max(image_sizes) if image_sizes else 0
        total_image_size = sum(image_sizes)

        video_tags = soup.find_all("video")
        video_urls = []

        for video in video_tags:
            src = video.get("src")
            if src:
                video_urls.append(urljoin(url, src))
            for source in video.find_all("source"):
                src = source.get("src")
                if src:
                    video_urls.append(urljoin(url, src))

        video_sizes = []
        for video_url in video_urls:
            size_bytes = None
            try:
                head = requests.head(video_url, timeout=15)
                head.raise_for_status()
                size_header = head.headers.get("Content-Length")
                if size_header:
                    size_bytes = int(size_header)
                else:
                    print(f"  [Video Missing Content-Length] {video_url}")

            except Exception as e:
                print(f"  [Video Error] {video_url}: {e}")

            if size_bytes:
                video_sizes.append(size_bytes)

        num_videos = len(video_sizes)
        max_video_size = max(video_sizes) if video_sizes else 0
        total_video_size = sum(video_sizes)

        total_media_size = total_image_size + total_video_size

        results.append({
            "Webpage URL": url,
            "Number of Images": num_images,
            "Max Image Size (KB)": max_image_size / 1024,
            "Total Image Size (KB)": total_image_size / 1024,
            "Number of Videos": num_videos,
            "Max Video Size (MB)": max_video_size / (1024 * 1024),
            "Total Video Size (MB)": total_video_size / (1024 * 1024),
            "Total Media Size (MB)": total_media_size / (1024 * 1024)
        })

        temp_df = pd.DataFrame(results)
        temp_df.to_excel(output_excel, index=False)

    except KeyboardInterrupt:
        print("Interrupted by user. Saving intermediate results.")
        break

    except Exception as e:
        print(f"  [Page Error] {url}: {e}")

output_df = pd.DataFrame(results)
output_df.to_excel(output_excel, index=False)

print(f"\nDone! Results saved to {output_excel}")