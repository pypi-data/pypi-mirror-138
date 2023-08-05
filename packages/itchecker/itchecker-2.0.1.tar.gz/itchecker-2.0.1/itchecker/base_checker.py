import traceback
from abc import ABC, abstractmethod
from os.path import join, basename, dirname, abspath, splitext
from typing import Dict, Any, List, Optional

import xlwings as xw
from jinja2 import Template
from xlwings import Sheet


class Checker(ABC):
    REPORT_TEMPLATE_NAME = None
    SUPPORTED_EXTENSIONS = None

    @classmethod
    def getattr(cls, obj, attr: str):
        path = attr.split('.')
        for el in path:
            obj = getattr(obj, el)
        return obj

    @classmethod
    def pre_process(cls, path: str):
        pass

    @classmethod
    def post_process(cls):
        pass

    @classmethod
    @abstractmethod
    def insert_data(cls, connection: Any, inputs: Any):
        pass

    @classmethod
    @abstractmethod
    def acquire_data(cls, connection: Any, query: Optional[str], outputs: List[str]) -> Any:
        pass

    @classmethod
    @abstractmethod
    def save_test(cls, path: str, connection: Any, output_path: str):
        pass

    @classmethod
    @abstractmethod
    def load_inputs(cls, inputs_setup_sheet: Sheet, test_no: int) -> List[str]:
        pass

    @classmethod
    def load_query(cls, outputs_setup_sheet: Sheet, test_no: int) -> List[str]:
        return outputs_setup_sheet[1, test_no + 1].value

    @classmethod
    def get_extension(cls, path: str) -> str:
        _, file_extension = splitext(path)
        return file_extension

    @classmethod
    def load_tests(cls, test_file_path, correct_file_path, output_folder_path) -> List[Dict[str, Any]]:
        with cls.get_connection(correct_file_path) as correct_file_connection:
            with xw.App(visible=False) as app:
                setup_wb = app.books.open(test_file_path)
                inputs_setup_sheet = setup_wb.sheets['input']
                outputs_setup_sheet = setup_wb.sheets['output']
                num_tests = inputs_setup_sheet['B1'].current_region.last_cell.column - 1
                print(f'Кількість тестів: {num_tests}')

                tests: List[Dict[str, Any]] = []
                for test_no in range(num_tests):
                    current_test = {
                        'score': inputs_setup_sheet[0, test_no + 1].value,
                        'query': cls.load_query(outputs_setup_sheet, test_no),
                        'inputs': cls.load_inputs(inputs_setup_sheet, test_no),
                        'outputs': list(filter(
                            lambda val: val is not None,
                            outputs_setup_sheet.range(
                                (3, test_no + 2),
                                outputs_setup_sheet.range((3, test_no + 2)).end('down')
                            ).value
                        )),
                        'results': [],
                    }

                    cls.insert_data(correct_file_connection, current_test['inputs'])
                    cls.save_test(correct_file_path, correct_file_connection,
                                  join(output_folder_path, 'tests',
                                       f'test{test_no + 1}{cls.get_extension(correct_file_path)}'))

                    current_test['results'] = cls.acquire_data(correct_file_connection, current_test['query'],
                                                               current_test['outputs'])
                    tests.append(current_test)

                setup_wb.close()
        return tests

    @classmethod
    @abstractmethod
    def get_connection(cls, path):
        pass

    @classmethod
    def test_file(cls, path: str, tests, output_folder_path: str):
        file_name = basename(path)
        score: float = 0.0
        max_score: float = 0.0
        results: List[float] = []
        details = []

        try:
            with cls.get_connection(path) as conn:
                print(f'Початок тестування роботи: {path}')

                for test in tests:
                    test_score = 0.0
                    try:
                        cls.insert_data(conn, test['inputs'])
                        file_data = cls.acquire_data(conn, test['query'], test['outputs'])
                        test_score = int(file_data == test['results']) * test['score']
                        score += test_score
                        test_details = {
                            'score': test_score,
                            'results': file_data
                        }
                    except Exception as e:
                        # print(f'Помилка виконання тесту: {path}. Деталі: {e}')
                        test_details = {
                            'score': 0.0,
                            'results': ([], []),
                            'error': str(e)
                        }
                    max_score += test['score']
                    results.append(test_score)
                    details.append(test_details)

            print(f'Кінець тестування роботи: {path}. Кількість балів: {score}')
            return {
                'file': file_name,
                'scores': results,
                'total_score': score
            }
        except Exception as e:
            print(f'Помилка тестування роботи: {path}. Деталі: {e}')
            print(f'Кінець тестування роботи: {path}. Кількість балів: {score}')

            remaining_items = len(tests) - len(results)
            results += [0.0] * remaining_items
            details += [{
                'score': 0.0,
                'results': ([], []),
                'error': str(e)
            }] * remaining_items

            return {
                'file': file_name,
                'scores': results,
                'total_score': score,
                'error': str(e)
            }
        finally:
            with open(join(dirname(abspath(__file__)), 'templates', cls.REPORT_TEMPLATE_NAME), encoding='utf-8') as f:
                template = Template(f.read())
            with open(join(output_folder_path, f'{file_name}.html'), 'w', encoding='utf-8') as f:
                f.write(template.render(details=details, tests=tests, file_name=file_name, total_score=score,
                                        max_score=max_score))

    @classmethod
    def create_report(cls, tests, results, output_folder_path):
        with xw.App(visible=False) as app:
            wb = app.books.add()
            sheet = wb.sheets.add('results')

            sheet[0, 1].value = 'Сума'
            sheet[1, 0].value = 'Максимум'

            total_score = 0.0
            for i, test in enumerate(tests):
                sheet[0, i + 2].value = f'Тест №{i + 1}'
                sheet[1, i + 2].value = test['score']
                total_score += test['score']
            sheet[1, 1].value = total_score

            for i, result in enumerate(results):
                sheet[i + 2, 0].value = result['file']
                sheet[i + 2, 1].value = result['total_score']
                for j, score in enumerate(result['scores']):
                    sheet[i + 2, j + 2].value = score

                if 'error' in result:
                    sheet[i + 2, 1].api.AddComment(Text=f'Помилка тестування роботи: {result["error"]}')
            try:
                wb.save(join(output_folder_path, 'results.xlsx'))
            except:
                input('Помилка запису результатів. Переконайтеся, що файл результатів не відкритий в Excel та введіть Yes.')
                wb.save(join(output_folder_path, 'results.xlsx'))
            wb.close()
