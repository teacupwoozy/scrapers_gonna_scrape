import requests
from bs4 import BeautifulSoup
import csv

# Define url to scrape
URL = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
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
table = soup.find('table', {'class': 'tdcj_table indent'})

# Loop through table rows
for row in table.find_all('tr'):
    # Empty list for cell data
    list_of_cells = []
    # Loop through each cell in tr
    for cell in row.find_all('td'):
        # Grab text from the cell
        text = cell.text.strip()
        # Append to list
        list_of_cells.append(text)
    # Append tr data to list_of_rows
    list_of_rows.append(list_of_cells)

# Create output file
outfile = open('tx_death_row_website.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
outfile.close()
