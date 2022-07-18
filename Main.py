from openpyexcel import load_workbook

#download Shadow_the_Hedhehog_Engings_List and replace file location in next line
book = load_workbook(r'Shadow-the-Hedgehog-Engings-List.xlsx')
sheet = book.active

rows = sheet.rows

headers = [cell.value for cell in next(rows)]

all_rows = []

# ['number', 'ending_name']
# ['cell_1, cell_2]
for row in rows:
    data = {}
    for title, cell in zip(headers, row): #('number', cell_1)
        data[title] = cell.value

    all_rows.append(data)

print(all_rows)
