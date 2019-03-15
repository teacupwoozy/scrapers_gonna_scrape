import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

# Define today's date
today = date.today()
# Create date for url
url_date = today.strftime('%m/%d/%Y')

# Define url to scrape
URL = 'https://cp.spokanecounty.org/courtdocumentviewer/PublicViewer/SCHearingsByDate.aspx?d={}'.format(url_date)
# Define headers
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
# Use requests to fetch URL
page = requests.get(URL, headers=HEADERS)
# Page content into Python
html = page.content

# Parse with BS
soup = BeautifulSoup(html, 'html.parser')
# Empty list to hold data for CSV
list_of_rows = []
# Find table in parsed html with BS
table = soup.find(id='tblHearingsSCByDate')

# Loop through table rows
for row in table.find_all('tr', class_='detailrow'):
    # Empty list for each loop's cell data
    list_of_cells = []
    # Loop through each cell in tr
    for cell in row.find_all('td'):
        # remove cruft
        if cell.span:
            cell.span.clear()
        # Grab cell text
        text = cell.text.strip()
        # Append the text to list
        list_of_cells.append(text)
    # Append completed data row to list of rows
    list_of_rows.append(list_of_cells)

# Create output file
filename_date = today.strftime('%Y-%m-%d')
outfile = open('docket_{}.csv'.format(filename_date), 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
outfile.close()