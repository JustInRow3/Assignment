from bs4 import BeautifulSoup
import requests
import stringmanipulation as sm
import aiohttp
import asyncio
import time
import pandas as pd
from datetime import datetime


def get_pages(url):
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

headers = {"User-Agent": "Mozilla/5.0"}

async def fetch(session, id_):
    url = f'https://meadowcreekhs.gcpsk12.org/fs/elements/55800?const_id={id_}&show_profile=true'
    async with session.get(url, headers=headers) as response:
        await asyncio.sleep(5)
        html = await response.text()
        # Check if request was successful
        if response.status == 200:
            soup = BeautifulSoup(html, "html.parser")  # Parse HTML content
            # print(soup.prettify())  # Print formatted HTML for debugging

            first_name = soup.find("span", class_="fsFullNameFirst").text.strip()
            last_name = soup.find("span", class_="fsFullNameLast").text.strip()
            script_content = soup.find("script").string
            email = sm.get_email(script_content)
            # Find all "fsProfileSectionFieldValue" elements
            field_values = soup.find_all("div", class_="fsProfileSectionFieldValue")

            # Extract department and title
            department = field_values[1].text.strip() if len(field_values) > 1 else None
            title = field_values[2].text.strip() if len(field_values) > 2 else None

            now = datetime.now()

            # Format the date and time
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

            data = {
                "First Name": first_name,
                "Last Name": last_name,
                "Title": title,
                "Department": department,
                "Phone Number": None,
                "Email Address": email,
                "School Type": 'Highschool',
                "School Name": 'Meadowcreek High School',
                "Scraped At": formatted_now
            }

            df = pd.DataFrame([data])
            print(f"Scraped {url} successfully!")
            # print(json_output)
            return df
        else:
            print("Error: Failed to retrieve the page. Status Code:", response.status_code)

async def scrape_all(id_all):
    async with aiohttp.ClientSession() as session:
        df = pd.DataFrame()
        for url in id_all:
            start_time = time.time()
            soup = await fetch(session, url)
            df = pd.concat([df, pd.DataFrame(soup)], ignore_index=True)
            elapsed_time = time.time() - start_time
            if elapsed_time < 5:
                await asyncio.sleep(5 - elapsed_time)  # Ensure minimum delay
        return df

async def run_meadows():
    all_pages = get_pages(r'https://meadowcreekhs.gcpsk12.org/directory')

    nested_id = []
    for page in all_pages: #compile ALL IDS
        nested_id.append(get_id(page))
        time.sleep(5)
    all_ids = list(set([item for sublist in nested_id for item in sublist]))
    loop = asyncio.get_running_loop()
    if loop.is_running():  # If loop is already running, create a task
        return await scrape_all(all_ids)
    else:
        return asyncio.run(scrape_all(all_ids))
