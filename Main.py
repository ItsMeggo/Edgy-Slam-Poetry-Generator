from openpyexcel import load_workbook

book = load_workbook(r'C:\Users\megan\OneDrive - University of Limerick\disposable\OneDrive - University of Limerick\Desktop\Python_Projects\Shadow-the-Hedgehog-Engings-List.xlsx')
sheet = book.active

rows = sheet.rows

headers = [cell.value for cell in next(rows)]

all_rows = []

for row in rows:
    data = {}
    for cell in (row):
        #making a list rather than a dictionary.
        all_rows.append(cell.value)
        

poem_line_1_input = input('Pick your favourite number between 1 and 326.\n')   #\n --> new line
poem_line_2_input = input('Pick your least favourite number between 1 and 326.\n')
poem_line_3_input = input('Pick the number you least care about between 1 and 326.\n')

#convert answers from strings to integers
poem_line_1 = int(poem_line_1_input)-1
poem_line_2 = int(poem_line_2_input)-1
poem_line_3 = int(poem_line_3_input)-1

#write the poem!
poem = []
poem.append(all_rows[poem_line_1])
poem.append(all_rows[poem_line_2])
poem.append(all_rows[poem_line_3])

print(poem)
