# Oil & Gas News Analytics

A pipeline for scraping, processing, and analyzing oil & gas industry news articles from SPE JPT.

## Features
- Web scraping of articles using Selenium
- Entity recognition with spaCy
- Text summarization using BART model
- Incremental CSV saving
- Custom entity patterns for oil/gas domain

## Installation

1. Clone repository:
```bash
git clone https://github.com/Omo-Mushin/oil-gas-news-analytics.git
cd oil-gas-news-analytics

Create a Virtual Environment (optional but recommended):

bash


python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Dependencies:

bash


pip install -r requirements.txt
Download spaCy Model:

The code uses the en_core_web_lg model. Download it with:

bash


python -m spacy download en_core_web_lg
Set Up Selenium WebDriver:

For local usage:
Download the appropriate Chromedriver version for your Chrome browser and operating system. Ensure the executable is in your system PATH or update the path in the code.

For Colab:
Use the Linux versions of Chromium and Chromedriver (the code above is for local Windows; for Colab see additional instructions in the Selenium documentation).
