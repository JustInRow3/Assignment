import requests
from bs4 import BeautifulSoup
import stringmanipulation as sm
import json


def httprequesturlhome(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Send an HTTP request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content
        # print(soup.prettify())  # Print formatted HTML for debugging
        script_content = soup.find("script").string
        print(sm.get_email(script_content))


    else:
        print("Error: Failed to retrieve the page. Status Code:", response.status_code)

# httprequesturlhome(r'https://meadowcreekhs.gcpsk12.org/fs/elements/55800?const_id=13164&show_profile=true')

def use_id(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    # Send an HTTP request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content
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

        data = {
            "firstname": first_name,
            "lastname": last_name,
            "title": title,
            "department": department,
            "email" : email
        }

        # Convert to JSON format
        json_output = json.dumps(data, indent=4)
        return json_output

    else:
        print("Error: Failed to retrieve the page. Status Code:", response.status_code)
# httprequesturl(r'https://meadowcreekhs.gcpsk12.org/directory?')

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
# get_id(r'https://meadowcreekhs.gcpsk12.org/directory')
use_id(r'https://meadowcreekhs.gcpsk12.org/fs/elements/55800?const_id=9847&show_profile=true')