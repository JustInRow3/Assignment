import re
import math


def getpages(stringresult):

    # Regular expression to capture the number after "of"
    match = re.search(r"of (\d+)", stringresult)
    page_links = []
    if match:
        number = int(match.group(1))  # Convert extracted string to integer
        # print("Extracted Number:", number)
        pages = math.ceil(number/100)
        for page in range(1, pages + 1):
            page_meadows = f'https://meadowcreekhs.gcpsk12.org/directory?const_page={str(page)}&'
            page_links.append(page_meadows)
        return page_links
    else:
        print("Number not found")
        return None

def get_email(soup):

    # Use regex to extract the two quoted strings
    match = re.search(r'FS\.util\.insertEmail\("fsEmail-\d+-\d+",\s*"([^"]+)",\s*"([^"]+)"', soup)

    if match:
        domain = match.group(1)
        username = match.group(2)
        email = f"{username[::-1]}@{domain[::-1]}"
        return email
    else:
        print("Email not found")
        return None