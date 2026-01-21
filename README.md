# Web Scraping Projects 🕸️

A collection of Python-based web scraping projects covering **static pages, semi-dynamic sites, browser automation**, and **API-driven extraction**. These projects reflect real-world data extraction workflows: collecting structured data, downloading media, handling pagination, and exporting clean outputs for analysis.

---

## What’s Inside

This repo demonstrates how to:

* Extract structured data from real websites (tables, listings, detail pages)
* Work with complex HTML (nested elements, inconsistent markup)
* Handle pagination, filtering, and multi-page crawling
* Download images/media and store them cleanly
* Save outputs to CSV / JSON (and other useful formats)
* Use browser automation for JS-heavy pages when needed

---

## Tools & Technologies

* **Python**
* **Poetry** (dependency & environment management)
* **Requests**
* **BeautifulSoup (bs4)**
* **lxml / html.parser**
* **CSV / JSON**
* **pathlib / os** (file handling)

Also used in some projects:

* **Scrapy**
* **Selenium**
* **Splash**
* **Pandas**
* **Jupyter**

---

## Repository Structure

* `api_projects/` – API-based extraction (REST/JSON workflows)
* `bs4_scraping/` – Requests + BeautifulSoup scrapers (static/semi-static sites)
* `selenium_scraping/` – Browser automation scrapers (JS-heavy sites)
* `splash_project/` – Scrapy + Splash rendering projects
* `spider_start/` – Scrapy spiders / crawling foundations
* `packages_data/` – Experiments using Python scraping/data packages
* `jupyter_notebooks/` – Prototypes and analysis notebooks
* `data_files/` – Sample outputs / exports (CSV/JSON/etc.)
* `resources/` – Notes, helper references, and materials

---

## Using This Repo (Poetry)

### 1. Clone the repository

```bash
git clone https://github.com/Iyanuvicky22/Web_scraping_projects.git
cd Web_scraping_projects
```

### 2. Install Poetry

If Poetry is not installed:

```bash
pip install poetry
```

Verify installation:

```bash
poetry --version
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Activate the virtual environment

```bash
poetry shell
```

Alternatively, run commands without activating the shell:

```bash
poetry run python --version
```

---

## Running Projects

### Option A – Run scripts from the repo root (recommended)

```bash
poetry run python bs4_scraping/main.py
```

```bash
poetry run python selenium_scraping/main.py
```

If a folder contains multiple scripts:

```bash
poetry run python bs4_scraping/movies_main.py
poetry run python api_projects/example_api_script.py
```

### Option B – Navigate into a folder and run

```bash
cd bs4_scraping
poetry run python main.py
```

Script entry filenames may vary by folder. Check the directory to confirm the correct file.

---

## Common Poetry Commands

Update dependencies:

```bash
poetry update
```

Add a dependency:

```bash
poetry add requests
```

Add a development dependency:

```bash
poetry add --group dev black
```

View environment details:

```bash
poetry env info
```

List installed packages:

```bash
poetry show
```

---

## Environment Variables

Some projects (especially API-based ones) require secrets or tokens.

Create a `.env` file in the project root:

```bash
touch .env
```

Example:

```env
API_KEY=your_key_here
BASE_URL=https://example.com
```

Load it in your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

Ensure `.env` is included in `.gitignore` and never committed.

---

## Notes & Best Practices

* Always respect **robots.txt** and website **Terms of Service**
* Use delays and retry logic to avoid rate limits or IP bans
* Set request headers (e.g., `User-Agent`) for stability
* Prefer official APIs when available
* Avoid collecting personal data without a lawful basis or consent

---

## Roadmap

* Additional Scrapy crawlers for large-scale extraction
* Playwright support for modern JS-heavy websites
* Centralized logging and standardized error handling
* Config-driven scrapers (YAML/JSON)
* Dockerized scraping environments

---

## Author

**Victor (Iyanuvicky22)**
* Data & Python Engineer – Web Scraping • Data Extraction • Automation
* GitHub: [https://github.com/Iyanuvicky22](https://github.com/Iyanuvicky22)
