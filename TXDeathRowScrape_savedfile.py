from bs4 import BeautifulSoup
import csv

# Open the html page
page = open('/Users/Stacy/Documents/WebDevelopment/projects/scraping/DeathRowInformation.html')
# Parse with BS into py
soup = BeautifulSoup(page, 'html.parser')
# close html page
page.close()

# Empty list
list_of_rows = []
# Find table
table = soup.find('table')

# Loop rows
for row in table.find_all('tr'):
    # Create empty list to hold cell data
    list_of_cells = []
    # Loop through each cell in the TR
    for cell in row.find_all('td'):
        # Grab text from the cell
        text = cell.text.strip()
        # Append to list
        list_of_cells.append(text)
    # Append each tr to list of rows
    list_of_rows.append(list_of_cells)

# Create output file
outfile = open('tx_death_row.csv', 'w')
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
outfile.close()