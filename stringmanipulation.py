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
            page_meadows = f'https://meadowcreekhs.gcpsk12.org/fs/elements/55800?const_page={str(page)}&is_draft=false&is_load_more=true&page_id=7498&parent_id=55800&_={str(page)}'
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


def format_full_name(name_str):
    """Extract first name, middle names, last name, and optional titles from a string."""
    # List of common titles (you can expand this)
    titles_list = ["Jr.", "Sr.", "PhD", "MD", "Dr.", "Prof.", "II", "III", "IV"]

    words = name_str.split()

    if len(words) < 2:
        return {"full_name": name_str}  # Return as-is if there's only one word

    # Identify titles (words at the end that match known titles)
    titles = []
    while words and words[-1] in titles_list:
        titles.insert(0, words.pop())  # Remove and store titles from the end

    first_name = words[0]
    last_name = words[-1] if len(words) > 1 else ""
    middle_names = " ".join(words[1:-1]) if len(words) > 2 else ""

    return {
        "first_name": first_name,
        "middle_names": middle_names,
        "last_name": last_name,
        "titles": " ".join(titles) if titles else "",
        "full_name": f"{first_name} {middle_names} {last_name}".strip() + (" " + " ".join(titles) if titles else "")
    }

# Regular expressions
phone_pattern = r"\d{3}-\d{3}-\d{4}"  # Matches XXX-XXX-XXXX
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Matches emails

def find_phone(text):
    # Find matches
    phone = re.search(phone_pattern, text)

    # Extract values
    phone_number = phone.group() if phone else None
    return phone_number

def find_email(text):
    email = re.search(email_pattern, text)
    email_address = email.group() if email else None
    return email_address