import argparse
from concurrent.futures.thread import ThreadPoolExecutor
from os import listdir, makedirs
from os.path import join, exists

# python console_tool.py --works-folder ./works --test-file ./tests.xlsx --correct-file ./etalon.xlsx --output-folder ./output
from itchecker.access import AccessChecker
from itchecker.excel import ExcelChecker
from itchecker.word import WordChecker


__version__ = "2.0.2"


def main():
    parser = argparse.ArgumentParser()

    checkers = {
        'excel': ExcelChecker,
        'access': AccessChecker,
        'word': WordChecker,
    }

    parser.add_argument('--checker', required=True, choices=checkers.keys())
    parser.add_argument('--works-folder', required=True)
    parser.add_argument('--test-file', required=True)
    parser.add_argument('--correct-file', required=True)
    parser.add_argument('--output-folder', required=True)

    args = parser.parse_args()

    if not exists(args.output_folder):
        print(f'Створення каталогу {args.output_folder}')
        makedirs(args.output_folder)

    if not exists(join(args.output_folder, 'tests')):
        makedirs(join(args.output_folder, 'tests'))

    Checker = checkers[args.checker]

    Checker.pre_process(args.correct_file)
    tests = Checker.load_tests(args.test_file, args.correct_file, args.output_folder)
    files = [
        join(args.works_folder, f)
        for f in listdir(args.works_folder)
        if any([f.endswith(f'.{ext}') for ext in Checker.SUPPORTED_EXTENSIONS]) and not f.startswith('~')
    ]

    for file in files:
        Checker.pre_process(file)

    def test_file_job(file):
        return Checker.test_file(file, tests, args.output_folder)

    with ThreadPoolExecutor(3) as executor:
        results = executor.map(test_file_job, files)

    results = list(results)
    Checker.create_report(tests, results, args.output_folder)


if __name__ == '__main__':
    main()
