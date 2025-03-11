from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from tqdm import tqdm  # Progress bar
# //div[contains(@class, 'PromoRTE-media')]//a[contains(@class, 'Link')]
# Set up Chrome options (disable notifications)
# //div[contains(@class, 'PromoRTE-title')]
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Set up the Chrome WebDriver
service = Service(executable_path=r"C:\Users\HP\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the JPT page
driver.get("https://jpt.spe.org/jpt-january-2025-issue")
time.sleep(5)

# Find all divs containing class "PromoA-title", "PromoB-title", "PromoC-title"
updates = driver.find_elements(By.XPATH, '//div[contains(@class, "PromoA-title")] | //div[contains(@class, "PromoB-title")] | //div[contains(@class, "PromoC-title")]')

titles = []
links = []
information = []

for item in updates:
    try:
        # Find the anchor tag within each div and get text + href
        link_element = item.find_element(By.XPATH, './/a[contains(@class, "Link")]')
        title = link_element.text.strip()
        link = link_element.get_attribute("href")

        titles.append(title)
        links.append(link)
    except Exception as e:
        print("Error extracting link:", e)

# Loop through all links to extract article text
print("\nExtracting article content...\n")
for i, link in enumerate(tqdm(links, desc="Progress", unit="link")):
    driver.get(link)
    time.sleep(5)  # Wait for page to load

    try:
        # Extract text from paragraphs inside the RichTextBody div
        paragraphs = driver.find_elements(By.XPATH, '//div[contains(@class, "RichTextBody")]//p')
        article_text = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

        information.append(article_text)
        tqdm.write(f"✅ {i+1}/{len(links)}: Successfully extracted content from {link}")

    except Exception as e:
        print(f"❌ {i+1}/{len(links)}: Error extracting information from {link}: {e}")
        information.append("")

# Create DataFrame
jpt_updates = pd.DataFrame({'titles': titles, 'links': links, 'information': information})

# Print DataFrame
print("\nExtraction Completed! Here is the data:")
print(jpt_updates)

jpt_updates.to_csv("jpt_articles_Jan_2025.csv", index=False)
# Quit the driver
driver.quit()
