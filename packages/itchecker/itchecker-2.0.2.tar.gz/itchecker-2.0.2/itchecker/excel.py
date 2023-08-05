import contextlib
from os.path import abspath
from typing import Dict, Any, List

import pythoncom
import xlwings as xw
from xlwings import Sheet

from itchecker.base_checker import Checker


class ExcelChecker(Checker):
    REPORT_TEMPLATE_NAME = 'excel_report.html'
    SUPPORTED_EXTENSIONS = {'xlsx', 'xls', 'xlsm'}
    _DATA_SETUP = {
        'Значення': {'field': 'value'},
        'Курсив': {'field': 'font.italic'},
        'Жирність': {'field': 'font.bold'},
        'Колір тексту': {'field': 'font.color'},
        'Назва шрифту': {'field': 'font.name'},
        'Розмір шрифту': {'field': 'font.size'},
        'Заливка': {'field': 'color'},
        'Числовий формат': {'field': 'number_format'},
    }

    @classmethod
    def insert_data(cls, connection: Sheet, inputs: Dict[str, Any]):
        for cell, value in inputs.items():
            connection.range(cell).value = value

    @classmethod
    def acquire_data(cls, connection: Sheet, query: str, outputs: List[str]) -> Dict[str, Any]:
        ERRORS = {-2146826281: '#DIV/0!', -2146826246: '#N/A', -2146826259: '#NAME?', -2146826288: '#NULL!',
                  -2146826252: '#NUM!', -2146826265: '#REF!', -2146826273: '#VALUE!'}

        data: Dict[str, Any] = {}
        for cell in outputs:
            # connection.charts.api._inner.ShapeRange.Chart.SeriesCollection(1)
            data[cell] = Checker.getattr(connection.range(cell), cls._DATA_SETUP[query]['field'])
            if data[cell] == '':
                data[cell] = None
            if connection.range(cell).raw_value in ERRORS:
                data[cell] = {'error': ERRORS[connection.range(cell).raw_value]}
        return data

    @classmethod
    def save_test(cls, path: str, connection: Sheet, output_path: str):
        connection.book.save(output_path)

    @classmethod
    def load_inputs(cls, inputs_setup_sheet: Sheet, test_no: int) -> Dict[str, Any]:
        inputs = {}
        num_cells = inputs_setup_sheet['B1'].current_region.last_cell.row - 1
        for cell_no in range(num_cells):
            cell_address = inputs_setup_sheet[cell_no + 1, 0].value
            value = inputs_setup_sheet[cell_no + 1, test_no + 1].value
            inputs[cell_address] = value
        return inputs

    @classmethod
    @contextlib.contextmanager
    def get_connection(cls, path):
        pythoncom.CoInitialize()
        with xw.App(visible=False) as app:
            wb = app.books.open(abspath(path))
            sheet = wb.sheets.active
            try:
                yield sheet
            finally:
                wb.close()
