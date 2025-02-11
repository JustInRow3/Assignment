from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests
import stringmanipulation as sm
import aiohttp
import asyncio
import json


def openbrowser(url):
    options = Options() #Chrome
    #options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    wd = webdriver.Chrome(service=service, options=options)  # Chrome
    wd.implicitly_wait(30)
    wd.maximize_window()
    wd.get(url)
    wait = WebDriverWait(wd, 40)
    wd.close()
    return wd, wait

def httprequesturlhome(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Send an HTTP request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content
        #print(soup.prettify())  # Print formatted HTML for debugging
        pages = soup.find('span', class_= 'fsPaginationLabel')
        if pages:
            page_link = sm.getpages(pages.text)
            return page_link

    else:
        print("Error: Failed to retrieve the page. Status Code:", response.status_code)


def get_id(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Send an HTTP request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content
        #print(soup.prettify())  # Print formatted HTML for debugging
        table = soup.find_all('div', class_= 'fsConstituentItem')
        id_ = [(cell.find('a', class_ = 'fsConstituentProfileLink')).get('data-constituent-id') for cell in table]
        return id_

    else:
        print("Error: Failed to retrieve the page. Status Code:", response.status_code)

def httprequestpages(urls):
    headers = {"User-Agent": "Mozilla/5.0"}

    async def fetch(session, id_):
        url = f'https://meadowcreekhs.gcpsk12.org/fs/elements/55800?const_id={id_}&show_profile=true&is_draft=false'
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            first_name = soup.find("span", class_="fsFullNameFirst").text.strip()
            last_name = soup.find("span", class_="fsFullNameLast").text.strip()

            # Find all "fsProfileSectionFieldValue" elements
            field_values = soup.find_all("div", class_="fsProfileSectionFieldValue")

            # Extract department and title
            department = field_values[1].text.strip() if len(field_values) > 1 else None
            title = field_values[2].text.strip() if len(field_values) > 2 else None

            data = {
                "firstname": first_name,
                "lastname": last_name,
                "title": title,
                "department": department
            }

            # Convert to JSON format
            json_output = json.dumps(data, indent=4)
            print(f"Scraped {url} successfully!")
            return json_output


    async def scrape_all():
        async with aiohttp.ClientSession() as session:
            for url in urls:
                await fetch(session, url)
                await asyncio.sleep(5)  # Respect crawl delay

    return asyncio.run(scrape_all())


