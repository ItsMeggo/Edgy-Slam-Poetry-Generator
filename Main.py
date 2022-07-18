from openpyexcel import load_workbook

book = load_workbook(r'C:\Users\megan\OneDrive - University of Limerick\disposable\OneDrive - University of Limerick\Desktop\Python_Projects\Shadow-the-Hedgehog-Engings-List.xlsx')
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
