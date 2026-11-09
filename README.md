# LeetCode 2014 Problem Scraper

Collects LeetCode's problem set as it looked in 2014 from the Internet Archive's Wayback Machine and saves it as structured JSON.

This is useful for building datasets of older, pre-LLM programming problems. Problems published before code-generation models existed are less likely to appear in their training data.

## How it works

1. Fetches the archived LeetCode homepage (December 2014 snapshot) with `requests` and parses the problem links with BeautifulSoup
2. Opens each problem page in Chrome (Selenium) and waits for the content to load
3. Extracts the **title, problem statement, solution code and date** for each problem, and strips line numbers from the code
4. Logs progress and errors to `leetcode_scraper.log` and writes the results to `problems_data.json`

## Tech stack

Python, Selenium, BeautifulSoup, requests

## How to run

```bash
pip install selenium beautifulsoup4 requests
python main.py
```

You need a ChromeDriver that matches your Chrome version, in the project folder or on your PATH.
