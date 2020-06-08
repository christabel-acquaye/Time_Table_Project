from openpyxl import Workbook, load_workbook


def create_sheet(size, headings):
    book = Workbook()
    sheet = book.active
    for i in range(size):
        book.create_sheet("Chromosome ", (i))
    book.save('test.xlsx')


def insert_into_excel(row, column, data):
    book = Workbook()
    sheet = book.active
    sheet.cell(row=row, column=column).value = data
    book.save('test.xlsx')


if __name__ == "__main__":
    row, column, data = 5, 5, 'CE 587'
    insert_into_excel(row=row, column=column, data=data)
