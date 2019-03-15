import requests
from bs4 import BeautifulSoup
import csv
import time

# Define url to scrape
URL = 'https://www.fda.gov/ICECI/EnforcementActions/WarningLetters/2018/default.htm'
# Define headers
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}

# Use requests to fetch url
page = requests.get(URL, headers=HEADERS)
# Page content into Python variable
html = page.content

# Parse with BS
soup = BeautifulSoup(html, 'html.parser')
# Make empty list of rows
list_of_rows = []
# Locate table in parsed html
table = soup.find('table')

# list_of_rows = []
# Monitor page number
page_num = 1
# Loop until told to stop
more_pages = True

# Start loop to scrape mult pages
while more_pages is True:
    # loop through rows, skipping first header row
    for row in table.find_all('tr')[1:]:
        # create empty list for each loop
        list_of_cells = []
        for cell in row.find_all('td'):
            # Grab cell text
            text = cell.text.strip()
            # Append to the list
            list_of_cells.append(text)
        # Append the row data to list of rows
        list_of_rows.append(list_of_cells)

    # Check for next page link
    if len(soup.find_all('a', href=True, text='Next')) > 0:
        # New page fetch and adjust url to scrape
        page_num += 1
        NEXT_URL = URL + '?Page=' + str(page_num)

        # Fetch new url
        page = requests.get(NEXT_URL, headers=HEADERS)

        # Get page content into Python
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        # Pause 1 second and make the server your friend
        time.sleep(1)

    # Exit loop is no more next pages
    else:
        more_pages = False

# Create output file
outfile = open('fda_warning_letters.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
outfile.close()
