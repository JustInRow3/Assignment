This is an scrapping assignment sent to me.
The task is to scrape this 2 urls (https://calbaptist.edu/faculty-directory/ , https://meadowcreekhs.gcpsk12.org/directory) and containing below details:
Extract the following fields of all contacts from the webpages (all that are available)
* First Name
* Last Name
* Title
* Department
* Phone Number
* Email Address


Format fields accordingly:
If only Full Name is extracted, parse into separate First Name and Last Name columns Also remove any prefixes (e.g. “Dr.” or “Mrs.”), middle initials (e.g. John T. Smith), or academic suffixes (e.g., "Ph.D.").


Store all the scraped contacts in a new Output tab in the excel file (sample provided) and ensure each extracted field is a separate column. Also include these columns for each row:
* School Type (High School or College)
* School Name
* Scraped At (datetime in YYYY-MM-DD HH:MM:SS format)
---------------------------------------------------------------------------------------------------------------------------------
Basic Instructions on how to run:
1. Install first all requirements:
   Open a terminal or command prompt in the working directory and type:
     pip install -r requirements.txt
2. After requirements are successfully installed, run the script by typing in the terminal or command prompt:
     python .
   
   
