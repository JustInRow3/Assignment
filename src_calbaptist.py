
from bs4 import BeautifulSoup
import requests
import stringmanipulation as sm
import aiohttp
import asyncio
import json
import time
from datetime import datetime
import pandas as pd


def get_pages(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Send an HTTP request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content
        # print(soup.prettify())  # Print formatted HTML for debugging
        all_ = soup.find('div', class_= "Faculty")
        # table = all_.find_all('div', class_= "Faculty__item filter--match")
        for cell in all_:
            fullname = cell.find('h2').get_text(strip=True)
            fullname_parsed = fullname.split(",")[0]
            title = cell.find('p', class_="Faculty__titles").get_text(strip=True)
            department = None
            phone = cell.find_all('p')[1].contents[0].get_text(strip=True).split(':')[1]
            email = cell.find_all('p')[1].contents[2].get_text(strip=True).split(':')[1]
            school = 'California Baptist University'
            now = datetime.now()

            # Format the date and time
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            scrapedate = formatted_now

            data = {
                "firstname": fullname_parsed.split()[:-1],
                "lastname": fullname_parsed.split()[-1],
                "title": title,
                "department": department,
                "phone": phone,
                "email": email,
                "schooltype": 'College',
                "schoolname": school,
                "scrapedate": formatted_now
            }

            json_output = json.dumps(data, indent=4)
            print(f"Scraped {url} successfully!")
            # print(json_output)
            return json_output
    else:
        print("Error: Failed to retrieve the page. Status Code:", response.status_code)

async def fetch(session, page_):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f'https://calbaptist.edu/faculty-directory/?page={page_}'
    async with session.get(url, headers=headers) as response:
        await asyncio.sleep(5)
        html = await response.text()
        df = pd.DataFrame()
        # Check if request was successful
        if response.status == 200:
            soup = BeautifulSoup(html, "html.parser")  # Parse HTML content
            # print(soup.prettify())  # Print formatted HTML for debugging
            all_ = soup.find('div', class_="Faculty")
            if len(all_) != 0:
                # table = all_.find_all('div', class_= "Faculty__item filter--match")
                for cell in all_:
                    fullname = cell.find('h2').get_text(strip=True)
                    fullname_parsed = fullname.split(",")[0]
                    if fullname_parsed.split()[-1] == 'Jr.':
                        fname = fullname_parsed.split()[:-2]
                        lname = fullname_parsed.split()[-2]
                    else:
                        fname = " ".join(fullname_parsed.split()[:-1])
                        lname = fullname_parsed.split()[-1]
                    title = cell.find('p', class_="Faculty__titles").get_text(strip=True)
                    department = None
                    phone = sm.find_phone(cell.find_all('p')[1].contents[0].get_text(strip=True))
                    email = sm.find_email(cell.find_all('p')[1].contents[2].get_text(strip=True))
                    school = 'California Baptist University'
                    now = datetime.now()

                    # Format the date and time
                    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
                    scrapedate = formatted_now

                    data = {
                        "First Name": fname,
                        "Last Name": lname,
                        "Title": title,
                        "Department": department,
                        "Phone Number": phone,
                        "Email Address": email,
                        "School Type": 'College',
                        "School Name": school,
                        "Scraped At": formatted_now
                    }

                    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                print(f"Scraped {url} successfully!")
                # print(json_output)

        else:
            print("Error: Failed to retrieve the page. Status Code:", response.status_code)
        return df
async def scrape_all():
    async with aiohttp.ClientSession() as session:
        df = pd.DataFrame()
        for url in range (1, 1000):
            start_time = time.time()
            soup = await fetch(session, url)
            if not soup.empty:
                df = pd.concat([df, pd.DataFrame(soup)], ignore_index=True)
                elapsed_time = time.time() - start_time
                if elapsed_time < 5:
                    await asyncio.sleep(5 - elapsed_time)  # Ensure minimum delay
            else:
                break
        return df



async def run_cbu():
    loop = asyncio.get_running_loop()
    if loop.is_running():  # If loop is already running, create a task
        return await scrape_all()
    else:
        return asyncio.run(scrape_all())
