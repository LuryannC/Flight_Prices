# Dealing with excel files

import jpype
import asposecells

jpype.startJVM()
from asposecells.api import FileFormatType, Workbook


# Write to a specified file
def write_to_file(file: Workbook, tab=0, cell='A1', value=None):
    return file.getWorksheets().get(tab).getCells().get(cell).putValue(value)


class Import:

    def __init__(self):
        self.main()

    def main(self):
        self.create_file("data", "test")

    def create_file(self, path: str, name: str):
        wb = Workbook(FileFormatType.XLSX)
        cells = wb.getWorksheets().get(0).getCells()
        headers = ['Departing day', 'Arriving day', 'Departing time', 'Arriving time', 'Duration', 'Price']
        cell = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        index = 0
        # Iterate over all headers and add the header to each cell[index]
        for header in range(len(headers)):
            write_to_file(wb, cell=f'{cell[index]}'+'1', value=f'{headers[header]}')
            cells.setColumnWidth(index, len(headers[header]))
            print(len(headers[header]))
            index += 1
        return wb.save(f"./{path}/{name}.xlsx")


if __name__ == '__main__':
    Import()
jpype.shutdownJVM()
