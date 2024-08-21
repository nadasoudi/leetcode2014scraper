from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import time
import logging
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import requests
import re

# Setup WebDriver
# make sure to download webdriver -chech the uploaded files 
service = Service(r'chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=service, options=chrome_options)

logging.basicConfig(filename='leetcode_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of URLs to scrape
urls = [
    "https://web.archive.org/web/20141217123003/http://leetcode.com/"
]

# List to hold the scraped data
questions_and_answers = []

# Iterate over each URL in the list
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the problem links
    problems = []
    for post in soup.find_all('div', class_='post'):
        entry = post.find('div', class_='entry')
        if entry:
            link = entry.find('a')['href']
            problems.append(link)

    print(problems)  # List of problem URLs

    for problem_url in problems:
        # Define the URL to be processed
        full_url = requests.compat.urljoin(url, problem_url)
        driver.get(full_url)
        time.sleep(10)  # Give the page time to load

        # Extract the question title
        title_element = driver.find_element(By.CSS_SELECTOR, "h2.posttitle")
        title = title_element.text.strip() if title_element else "Title not found"

        # Extract the problem statement
        blockquote = driver.find_element(By.CSS_SELECTOR, "blockquote")

        # Find all <p> tags within the blockquote
        paragraphs = blockquote.find_elements(By.TAG_NAME, "p")

        # Extract the text from each <p> tag and combine them into one paragraph
        problem_statement = " ".join([para.text for para in paragraphs])

        # Extract the date text
        date_paragraph = driver.find_element(By.CSS_SELECTOR, "p.date")
        date_text = date_paragraph.text.strip() if date_paragraph else "Date not found"

        # Extract the code from the div with class "crayon-pre"
        code_div = driver.find_element(By.CSS_SELECTOR, "div.crayon-pre")
        code = code_div.text.strip() if code_div else "No code found"
        cleaned_code = re.sub(r'^\d+', '', code, flags=re.MULTILINE)

        # Save the data to the list
        questions_and_answers.append({
            'Title': title,
            'Problem Statement': problem_statement,
            'Code': cleaned_code,
            'Date': date_text
        })

        print('Title:', title)
        print('Problem Statement:', problem_statement)
        print('Code:', cleaned_code)
        print('Date:', date_text)

# Save the data to a JSON file
with open('problems_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(questions_and_answers, json_file, ensure_ascii=False, indent=4)

driver.quit()
