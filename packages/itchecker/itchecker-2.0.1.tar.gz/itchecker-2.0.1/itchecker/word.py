import contextlib
import os
from typing import Dict, List, Any

import pythoncom
import win32com.client as win32
from xlwings import Sheet

from itchecker.base_checker import Checker


class WordInteractor:
    def __init__(self, document: 'Document'):
        self._document = document
        self._OBJECT_SETUP = {
            'поле вводу': {'name_field': 'Tag', 'object_field': 'ContentControls'},
            'таблиця': {
                'name_field': 'Title',
                'object_field': 'Tables',
                'selector': lambda obj, path: obj.Cell(int(path[2]), int(path[3]))
            },
            'закладка': {'name_field': 'Name', 'object_field': 'Bookmarks'},
            'абзац': {'name_field': 'id', 'object_field': 'Paragraphs'},
            'документ': {'object_field': 'Content'},
        }
        self._DATA_SETUP = {
            'Значення': {'field': 'Text', 'scope': 'whole'},
            'Курсив': {'field': 'Font.Italic', 'scope': 'word'},
            'Жирність': {'field': 'Font.Bold', 'scope': 'word'},
            'Колір тексту': {'field': 'Font.Color', 'scope': 'word'},
            'Назва шрифту': {'field': 'Font.Name', 'scope': 'word'},
            'Розмір шрифту': {'field': 'Font.Size', 'scope': 'word'},
            'Підрядковий': {'field': 'Font.Subscript', 'scope': 'word'},
            'Надрядковий': {'field': 'Font.Superscript', 'scope': 'word'},
            'Підкреслений': {'field': 'Font.Underline', 'scope': 'word'},
        }

    def _get_objects(self, reference: str) -> List:
        self._document.Fields.Update()
        path = reference.split(':')
        object_type = path[0]

        if object_type not in self._OBJECT_SETUP:
            raise Exception(
                f'Нерозпізнаний тип об\'єкту: {object_type}. Доступні типи: {", ".join(self._OBJECT_SETUP.keys())}.'
            )

        name_field = self._OBJECT_SETUP[object_type].get('name_field')
        object_field = self._OBJECT_SETUP[object_type].get('object_field')
        selector = self._OBJECT_SETUP[object_type].get('selector', lambda obj, _: obj)

        if not name_field:
            return [getattr(self._document, object_field)]

        objects = []
        for i, control in enumerate(getattr(self._document, object_field)):
            if name_field == 'id':
                if i + 1 == int(path[1]):
                    objects.append(selector(control, path).Range)
            elif getattr(control, name_field) == path[1]:
                objects.append(selector(control, path).Range)

        return objects

    def update(self):
        self._document.Fields.Update()

    def save_as(self, *args, **kwargs):
        self._document.SaveAs(*args, **kwargs)

    def _get_value(self, obj, data_type: str):
        if not obj:
            return None

        setup = self._DATA_SETUP[data_type]
        if setup['scope'] == 'whole':
            return Checker.getattr(obj, setup['field'])
        elif setup['scope'] == 'word':
            return [Checker.getattr(word, setup['field']) for word in obj.Words]
        else:
            raise Exception(f'Некоректний масштаб пошуку значення {setup["scope"]}. Доступні: whole, word')

    def read(self, reference: str, data_type: str):
        objects = self._get_objects(reference)
        return self._get_value(objects[0], data_type) if objects else None

    def write(self, reference: str, value: str):
        for control in self._get_objects(reference):
            control.Text = value


class WordChecker(Checker):
    REPORT_TEMPLATE_NAME = 'word_report.html'
    SUPPORTED_EXTENSIONS = {'doc', 'docx', 'docm'}

    @classmethod
    @contextlib.contextmanager
    def get_connection(cls, path):
        pythoncom.CoInitialize()
        word = win32.Dispatch('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(path)
        try:
            yield WordInteractor(document=doc)
        except Exception as e:
            doc.Close(SaveChanges=False)
            raise e
        doc.Close(SaveChanges=False)

    @classmethod
    def insert_data(cls, connection: WordInteractor, inputs: Dict[str, Any]):
        for reference, value in inputs.items():
            connection.write(reference, value)

    @classmethod
    def acquire_data(cls, connection: WordInteractor, query: str, outputs: List[str]) -> Dict[str, Any]:
        connection.update()
        data: Dict[str, Any] = {}
        for reference in outputs:
            data[reference] = connection.read(reference, query)
        return data

    @classmethod
    def save_test(cls, path: str, connection: WordInteractor, output_path: str):
        connection.save_as(output_path)

    @classmethod
    def load_inputs(cls, inputs_setup_sheet: Sheet, test_no: int) -> Dict[str, Any]:
        inputs = {}
        num_cells = inputs_setup_sheet['B1'].current_region.last_cell.row - 1
        for cell_no in range(num_cells):
            cell_address = inputs_setup_sheet[cell_no + 1, 0].value
            value = inputs_setup_sheet[cell_no + 1, test_no + 1].value
            inputs[cell_address] = value
        return inputs
