from openpyxl import Workbook

for i in range(0, 4):
    book = Workbook()
    sheet = book.active
    book.create_sheet("Chromosome ", i)