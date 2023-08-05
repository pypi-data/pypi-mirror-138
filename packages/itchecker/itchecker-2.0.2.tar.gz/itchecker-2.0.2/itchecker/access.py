import contextlib
import shutil
import threading
import time
from os.path import abspath
from typing import Dict, List, Tuple

import pyodbc
import win32com.client
from xlwings import Sheet

from itchecker.base_checker import Checker


class AccessChecker(Checker):
    REPORT_TEMPLATE_NAME = 'access_report.html'
    SUPPORTED_EXTENSIONS = {'accdb', 'mdb'}

    @classmethod
    def pre_process(cls, path: str):
        oApp = win32com.client.Dispatch("Access.Application")
        try:
            oApp.OpenCurrentDatabase(abspath(path))
            currentdb = oApp.CurrentDb()
            for query in currentdb.QueryDefs:
                query.SQL = query.SQL.replace('"', "'")
            currentdb = None
            oApp.DoCmd.CloseDatabase()

        except Exception as e:
            print(f'Помилка препоцесингу: {e}.')

        finally:
            currentdb = None
            oApp.Quit()

    @classmethod
    @contextlib.contextmanager
    def get_connection(cls, path):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            rf'DBQ={abspath(path)};'
        )
        with pyodbc.connect(conn_str) as conn:
            db_cursor = conn.cursor()
            try:
                yield db_cursor
            except Exception as e:
                db_cursor.close()
                conn.close()
                raise e
            db_cursor.close()

    @classmethod
    def insert_data(cls, connection: pyodbc.Cursor, queries: List[str]):
        for query in queries:
            connection.execute(query)

    @classmethod
    def acquire_data(cls, connection: pyodbc.Cursor, query: str, outputs: List[str]) -> Tuple[List[str], List[Dict]]:
        finished = False

        def watchdog():  # 464 204  # 460 464 562
            for i in range(360):
                time.sleep(0.1)
                if finished:
                    return
            try:
                connection.cancel()
            except:
                pass

        t = threading.Thread(target=watchdog)
        t.start()
        connection.execute(query)
        columns = [column[0] for column in connection.description]
        results = []
        for row in connection.fetchall():
            results.append(dict(zip(columns, row)))
        finished = True
        t.join()
        return outputs, [{column: result.get(column) for column in outputs} for result in results]

    @classmethod
    def save_test(cls, path: str, connection: pyodbc.Cursor, output_path: str):
        shutil.copyfile(path, output_path)

    @classmethod
    def load_inputs(cls, inputs_setup_sheet: Sheet, test_no: int) -> List[str]:
        return list(filter(
            lambda val: val is not None,
            inputs_setup_sheet.range(
                (2, test_no + 2),
                inputs_setup_sheet.range((2, test_no + 2)).end('down')
            ).value
        ))
