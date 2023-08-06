import argparse
import csv
import math
import re
import sys
from collections import defaultdict

from openpyxl import load_workbook
from xlrd import open_workbook

__version__ = "0.4.2"

if sys.platform != "win32":
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def get_header(file):
    row = next(file).strip()
    for i, name in enumerate(row.split("\t"), start=1):
        yield f"{i}\t{name}"


def is_float(value) -> bool:
    try:
        value = float(value)
        if not math.isnan(value):
            return True
    except ValueError:
        return False


def get_stats(file, header: bool):
    row = next(file).strip().split("\t")
    dataframe = [[] for _ in range(len(row))]
    if header:
        columns = row
    else:
        columns = [str(_) for _ in range(1, len(row) + 1)]
        for i, value in enumerate(row):
            if is_float(value):
                dataframe[i].append(float(value))
    for line in file:
        row = line.strip().split("\t")
        for i, value in enumerate(row):
            if is_float(value):
                dataframe[i].append(float(value))
    stats = defaultdict(list)
    for i, array in enumerate(dataframe):
        if array:
            count = len(array)
            min_value = min(array)
            max_value = max(array)
            mean = sum(array) / count
            array.sort()
            median = array[count // 2] if count % 2 else (array[count // 2] + array[count // 2 - 1]) / 2
            std = math.sqrt(sum((_ - mean)**2 for _ in array) / count)
            n = max(min(4 - int(math.log10(median)), 4), 1)
            stats[columns[i]] = [count, round(min_value, n), round(max_value, n), round(mean, n), round(median, n), round(std, n)]
        else:
            stats[columns[i]] = ["NA", "NA", "NA", "NA", "NA", "NA"]
    yield "column\t" + "\t".join(columns)
    items = ["count", "min", "max", "mean", "median", "std"]
    for i, item in enumerate(items):
        out = "\t".join([str(stats[column][i]) for column in columns])
        yield f"{item:6s}\t{out}"


def get_view(file, limit: int, nlines: int):
    rows = []
    width = []
    for i, line in enumerate(file, start=1):
        row = line.strip().split("\t")
        for index, string in enumerate(row):
            if len(width) <= index:
                width.append(len(string))
            width[index] = min(limit, max(len(string), width[index]))
        rows.append(row)
        if nlines and i == nlines:
            break
    for row in rows:
        out_row = []
        for index, string in enumerate(row):
            if len(string) < width[index]:
                row[index] = string + " " * (width[index] - len(string))
            else:
                row[index] = string[:width[index]]
            out_row.append(row[index])
        yield "  ".join(out_row)


def get_pattern(file, pattern: str, header: bool):
    if header:
        yield next(file).strip()
    for line in file:
        row = line.strip().split("\t")
        p = re.findall("\$(\d+)", pattern)
        columns = [int(i) - 1 for i in p]
        exp = pattern
        try:
            for i in columns:
                exp = re.sub("\$\d+", f"row[{i}]", exp, 1)
            if eval(exp):
                yield line.strip()
        except ValueError:
            pass


def add_column(file, pattern: str, header: bool):
    if header:
        yield next(file).strip() + "\t" + pattern
    for line in file:
        row = line.strip().split("\t")
        p = re.findall("\$(\d+)", pattern)
        columns = [int(i) - 1 for i in p]
        exp = pattern
        try:
            for i in columns:
                exp = re.sub("\$\d+", f"row[{i}]", exp, 1)
            yield "\t".join(row) + "\t" + str(eval(exp))
        except ValueError:
            pass


def reorder_columns(file, columns: str):
    columns = columns.split(",")
    for line in file:
        row = line.strip().split("\t")
        out_row = []
        for index in columns:
            out_row.append(row[int(index) - 1])
        yield "\t".join(out_row)


def get_file(file):
    if not file:
        file = sys.stdin
    else:
        if file.endswith(".xlsx"):
            wb = load_workbook(file, read_only=True, data_only=True)
            ws = wb.active
            file = ("\t".join([str(_.value) for _ in row]) for row in ws.rows)
        elif file.endswith(".xls"):
            wb = open_workbook(file, on_demand=True)
            ws = wb.sheet_by_index(0)
            file = ("\t".join([str(_.value) for _ in row]) for row in ws.get_rows())
        elif file.endswith(".csv"):
            reader = csv.reader(open(file, "r"))
            file = ("\t".join(row) for row in reader)
        else:
            file = open(file, "r")
    return file


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="TSV toolkit {}".format(__version__))
    parser.add_argument("input", nargs="?", type=str, help="file to parse, tab-delimited, default: stdin")
    parser.add_argument("-H", "--header", action="store_true", help="print header or include header in the output")
    parser.add_argument("-v", "--view", action="store_true", help="aligned display of each column")
    parser.add_argument("-s", "--stat", action="store_true", help="descriptive statistics")
    parser.add_argument("-p", "--pattern", type=str, help="pattern to match, wrap in single quotes")
    parser.add_argument("-a", "--add", type=str, help="add a new column with pattern, wrap in single quotes")
    parser.add_argument("-r", "--reorder", type=str, help="reorder columns, comma separated list of column numbers")
    parser.add_argument("-l", "--limit", type=int, default=100, help="limit of column width, used with -v, 0 for unlimited, default: 100")
    parser.add_argument("-n", "--nlines", type=int, default=100, help="max number of lines to view, used with -v, default: 100")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args()
    file = get_file(args.input)
    if not (args.stat or args.view or args.pattern or args.add or args.reorder):
        if args.header:
            file = get_header(file)
        else:
            sys.exit(parser.print_help())
    if args.pattern:
        file = get_pattern(file, args.pattern, args.header)
    if args.add:
        file = add_column(file, args.add, args.header)
    if args.reorder:
        file = reorder_columns(file, args.reorder)
    if args.stat:
        file = get_stats(file, args.header)
    if args.view:
        file = get_view(file, args.limit, args.nlines)
    for line in file:
        print(line.strip())


if __name__ == "__main__":
    main()
