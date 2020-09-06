import requests
from bs4 import BeautifulSoup
import xlsxwriter

workbook = xlsxwriter.Workbook('MedicalBotTest.xlsx')
worksheet = workbook.add_worksheet()

checkworkbook = xlsxwriter.Workbook('PresenceCheck.xlsx')
checkworksheet1 = checkworkbook.add_worksheet()
checkworksheet2 = checkworkbook.add_worksheet()


pres_row1 = 1
pres_column = 0
pres_row2 = 1

row = 1
column = 0

def pres_check(query, feedback):
    global pres_row1, pres_row2, pres_column
    print("Validating Presence")
    # print(query)
    # print(feedback)

    if feedback == "No results found!.":
        checkworksheet1.write(pres_row1, pres_column, query)
        checkworksheet1.write(pres_row1, 1, "NO")
        pres_row1 += 1
        print('Its not there')
    else:
        checkworksheet2.write(pres_row2, pres_column, query)
        checkworksheet2.write(pres_row2, 1, "YES")
        pres_row2 += 1
        print('Its there')


def final_scrape(final_url):
    global row, column
    print('Beginning final scrape procedures....')
    r = requests.get(final_url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(r.text, 'html.parser')
    med_detail_table = soup.find('table', class_ = 'namePanelin')
    # print(med_detail_table)
    temp_storage = []
    for field in med_detail_table.find_all('tr'):
        data = field.find_all('td')[1]
        # print(data.text.strip())
        data.text.strip()
        new_data = data.text
        new_data = new_data.strip('\n')
        new_data = new_data.strip('\t')
        new_data = new_data.strip('\t\t\t\t\t\n')
        temp_storage.append(new_data)
    # print(temp_storage)
    print('Data scraped packing into excel sheet now')
    for item in temp_storage:
        worksheet.write(row, column, item)
        column += 1
    temp_storage.clear()
    row += 1
    column = 0
    print('One row successfully transferred into the excel sheet')
    # print(len(temp_storage))
    # print(med_detail_table.text.strip())


def get_search_result(query):
    url = 'https://nmra.gov.lk/index.php?option=com_drugs&view=drugs&Itemid=221&limit=0&search=' + query + '&manufacturer=&importer=&country=&lang=en'
    r = requests.get(url, headers={"User-Agent": "XY"})
    # print(r.status_code)
    print('Getting the Search List Ready....')
    soup = BeautifulSoup(r.text, 'html.parser')
    med_dir_table = soup.find('table', class_ ='mtable phrmaciesdir')
    # print(med_dir_table)
    pres_check(query, med_dir_table.text)
    # print(med_dir_table.text)

    # for med in med_dir_table.find_all('a', href=True):
    #     # print(med['href'])
    #     scrape_url = 'https://nmra.gov.lk/' + med['href']
    #     # print(scrape_url)
    #     print('Finished creating the URL for the varied medicines......')
    #     final_scrape(scrape_url)

def begin_scrape():
    f = open("data.txt", "r")
    for q in f:
        print(q)
        get_search_result(q)
    f.close()
    print("All Data successfully transferred...")
    workbook.close()
    checkworkbook.close()


begin_scrape()

