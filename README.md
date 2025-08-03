# Web Performance & Media Analysis Toolkit

## Project Overview

This project provides a complete toolkit for analyzing website media performance, accessibility, and page speed. It is designed to help web developers and digital marketers optimize their websites for faster load times, improved SEO, and better accessibility compliance.

The repository contains three main modules:

1. **Alt Text Automation** – Automatically generates and validates image alt text for accessibility.
2. **Media Analysis** – Evaluates media assets (images, videos) for optimization opportunities.
3. **Page Speed Insights** – Analyzes site performance using the Google PageSpeed Insights API.

This toolkit is particularly useful for small organizations and nonprofits managing content-heavy websites, enabling automated auditing and actionable insights.

---

## Key Features

### 1️⃣ Alt Text Automation (`alt-text.py`)

* **Extracts image URLs** from a target website or media folder.
* **Generates alt text** for images lacking accessibility descriptions.
* **Exports results** to CSV for easy content updates.

### 2️⃣ Media Asset Analysis (`mediaAnalysis.py`)

* **Scans website media** to collect file size, type, and dimensions.
* **Flags large or unoptimized files** for compression and resizing.
* **Provides exportable reports** to prioritize optimization efforts.

### 3️⃣ Page Speed Insights (`pageSpeedInsights.py`)

* **Integrates with Google PageSpeed Insights API** to fetch performance scores.
* **Analyzes key metrics** like Largest Contentful Paint (LCP), First Input Delay (FID), and Cumulative Layout Shift (CLS).
* **Generates actionable recommendations** for speed and Core Web Vitals improvements.

---

## System Architecture

```
Website URL / Media Folder
        │
        ├── alt-text.py ──> CSV report with missing & generated alt text
        │
        ├── mediaAnalysis.py ──> Media optimization report (size, type, recommendations)
        │
        └── pageSpeedInsights.py ──> PageSpeed performance report & actionable insights
```

---

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/web-performance-toolkit.git
cd web-performance-toolkit
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
bs4
openpyxl
pandas
requests
selenium
urllib
```

**Optional Packages**:

```
google-api-python-client  # For PageSpeed API
lxml                     # For better HTML parsing with bs4
```

### 3️⃣ Set Up Google PageSpeed API (Optional)

1. Create an API key from [Google Cloud Console](https://console.cloud.google.com/).
2. Replace `API_KEY` in `pageSpeedInsights.py` with your key.

---

## Usage

### 1. Generate Alt Text

```bash
python alt-text.py
```

* Outputs a CSV with missing or auto-generated alt text for each image.

### 2. Analyze Media Files

```bash
python mediaAnalysis.py
```

* Produces a CSV report with file size, dimensions, and optimization suggestions.

### 3. Evaluate Page Speed

```bash
python pageSpeedInsights.py
```

* Returns a JSON or CSV report with Core Web Vitals and improvement recommendations.

---

## Insights & Results

* **Accessibility Improvement**: Identify missing alt text across the site.
* **Faster Load Times**: Spot and fix oversized or unoptimized media.
* **SEO Boost**: Enhance search engine visibility with better page performance.
* **Actionable Reports**: Each script produces clear CSV/JSON outputs for follow-up tasks.

---

## Contributing & Usage

* Feel free to adapt scripts for your organization’s workflow.
* PRs and feature enhancements are welcome.
* ⭐ Star the repo if it helps you improve your website’s performance!

---

## Contact

For any questions or collaboration:

- **[LinkedIn](https://www.linkedin.com/in/mohitsaigutha/)**
- **[Email](mailto:mohit.sai6@gmail.com)**

© 2025 Mohit Sai Gutha | Web Performance & Media Optimization Toolkit
