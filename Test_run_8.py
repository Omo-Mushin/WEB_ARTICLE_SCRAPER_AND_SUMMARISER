from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from tqdm import tqdm

# Set up Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
service = Service(executable_path=r"C:\Users\HP\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)  # Explicit wait for elements

def scrape_articles(url):
    # Navigate to the issue page
    driver.get(url)
    try:
        # Wait until at least one article block is present
        wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[contains(@class, "PromoA-title")] | //div[contains(@class, "PromoB-title")] | //div[contains(@class, "PromoC-title")]'
        )))
    except Exception as e:
        print(f"⚠ Issue page did not load articles: {url} ({e})")
        return pd.DataFrame()  # Return empty DataFrame if nothing is found

    # Find article blocks
    updates = driver.find_elements(By.XPATH,
        '//div[contains(@class, "PromoA-title")] | //div[contains(@class, "PromoB-title")] | //div[contains(@class, "PromoC-title")]'
    )

    titles = []
    links = []
    information = []

    # Extract article links from each block
    for item in updates:
        try:
            link_element = item.find_element(By.XPATH, './/a[contains(@class, "Link")]')
            title = link_element.text.strip()
            link = link_element.get_attribute("href")
            titles.append(title)
            links.append(link)
        except Exception as e:
            print("Error extracting article link:", e)

    # For each article link, navigate and extract article content
    print("\nExtracting article content...\n")
    for i, link in enumerate(tqdm(links, desc="Articles", unit="link")):
        try:
            driver.get(link)
            # Wait until the article content is present (adjust the wait criteria if needed)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "RichTextBody")]//p')))
            paragraphs = driver.find_elements(By.XPATH, '//div[contains(@class, "RichTextBody")]//p')
            article_text = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
            information.append(article_text)
            tqdm.write(f"✅ {i + 1}/{len(links)}: Successfully extracted content from {link}")
        except Exception as e:
            print(f"❌ {i + 1}/{len(links)}: Error extracting content from {link}: {e}")
            information.append("")
            continue

    # Create a DataFrame with the scraped article data
    df_issue = pd.DataFrame({
        'titles': titles,
        'links': links,
        'information': information
    })

    return df_issue

# 1. Navigate to the main JPT page
driver.get("https://jpt.spe.org/")
time.sleep(5)

# 2. Click on the Archive link to get the issues
try:
    archive_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Archive")]')))
    archive_url = archive_link.get_attribute("href")
    driver.get(archive_url)
    time.sleep(5)
except Exception as e:
    print("Error opening Archive page:", e)
    driver.quit()
    exit()

# 3. Extract issue links using the correct XPath for issue links
issue_links = []
try:
    # Use the XPath that gets the <a> elements inside PromoRTE-media
    issue_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "PromoRTE-media")]//a[contains(@class, "Link")]')
    issue_links = [issue.get_attribute("href") for issue in issue_elements if issue.get_attribute("href")]
    print(f"Found {len(issue_links)} issue links.")
except Exception as e:
    print("Error extracting issue links:", e)

# 4. For each issue, scrape the articles and accumulate DataFrames
all_dfs = []
for issue_link in tqdm(issue_links, desc="Scraping Issues", unit="issue"):
    df_issue = scrape_articles(issue_link)
    if not df_issue.empty:
        all_dfs.append(df_issue)

# 5. Concatenate all issue DataFrames and save to CSV
if all_dfs:
    df_all = pd.concat(all_dfs, ignore_index=True)
    df_all.to_csv("jpt_articles_4.csv", index=False)
    print("✅ Scraping complete! Data saved to 'jpt_articles.csv'.")
else:
    print("⚠ No data scraped. Check the XPaths and website structure.")

driver.quit()
