# Dealing with excel files

import jpype
import asposecells

#jpype.startJVM()
from asposecells.api import FileFormatType, Workbook, BorderType, CellBorderType


# Write to a specified file
def write_to_file(file: Workbook, cell: str, value=None, borders=False, tab=0):
    worksheet = file.getWorksheets().get(tab)
    current_cell = worksheet.getCells().get(cell)
    style = current_cell.getStyle()
    if borders:
        # Setting the line style of the top border
        style.getBorders().getByBorderType(BorderType.TOP_BORDER).setLineStyle(CellBorderType.MEDIUM)
        # Setting the line style of the bottom border
        style.getBorders().getByBorderType(BorderType.BOTTOM_BORDER).setLineStyle(CellBorderType.MEDIUM)
        # Setting the line style of the left border
        style.getBorders().getByBorderType(BorderType.LEFT_BORDER).setLineStyle(CellBorderType.MEDIUM)
        # Setting the line style of the right border
        style.getBorders().getByBorderType(BorderType.RIGHT_BORDER).setLineStyle(CellBorderType.MEDIUM)
    # Set style object to cell
    current_cell.setStyle(style)
    return file.getWorksheets().get(tab).getCells().get(cell).putValue(value)


def create_file(path: str, name: str, data):
    wb = Workbook(FileFormatType.XLSX)
    cells = wb.getWorksheets().get(0).getCells()
    headers = ['Departing day', 'Depart airport', 'Outbound duration', 'Arriving time', 'Arrive airport', 'Return time',
               'Return airport', 'Return Duration', 'Return Arrive', 'Return Airport', 'Price', 'Link']
    cell = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = 0
    cell_index = 2
    # Handles the creation of columns with desired size.
    # Iterate over all headers and add the header to each cell[index]
    for header in range(len(headers)):
        write_to_file(wb, cell=f'{cell[index]}' + '1', value=f'{headers[header]}', borders=True)
        cells.setColumnWidth(index, len(headers[header]))
        index += 1
    for fi in range(len(data)):
        for di in range(len(data[fi])):
            write_to_file(wb, cell=f'{cell[di]}'+f'{cell_index}', value=f'{data[fi][di]}', borders=True)
        cell_index += 1
    return wb.save(f"./{path}/{name}.xlsx")


def save_file(file):
    return Workbook(FileFormatType.XLSX).save(file)


def open_file(path: str):
    load_file = jpype.JClass("com.aspose.cells.LoadOptions")
    print("opened")
    return Workbook(path, load_file(FileFormatType.XLSX))


class Export:

    def __init__(self):
        pass

    def main(self):
        pass


if __name__ == '__main__':
    Export()
#jpype.shutdownJVM()
