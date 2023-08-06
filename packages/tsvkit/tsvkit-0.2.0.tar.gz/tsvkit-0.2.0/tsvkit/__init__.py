import argparse
import math
import re
import sys
from collections import defaultdict

__version__ = "0.2.0"

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


def get_stats(file, header: bool, column: int):
    row = next(file).strip().split("\t")
    if header:
        samples = [row[column - 1]] if column else row
    else:
        samples = [str(column)] if column else [str(_) for _ in range(1, len(row) + 1)]
    array2D = [[] for _ in range(len(samples))]
    if not header:
        if column:
            value = row[column - 1]
            if is_float(value):
                array2D[0].append(float(value))
        else:
            for i, value in enumerate(row):
                if is_float(value):
                    array2D[i].append(float(value))
    for line in file:
        row = line.strip().split("\t")
        if column:
            value = row[column - 1]
            if is_float(value):
                array2D[0].append(float(value))
        else:
            for i, value in enumerate(row):
                if is_float(value):
                    array2D[i].append(float(value))
    stats = defaultdict(list)
    for i, array in enumerate(array2D):
        if array:
            count = len(array)
            min_value = min(array)
            max_value = max(array)
            mean = sum(array) / count
            array.sort()
            median = array[count // 2] if count % 2 else (array[count // 2] + array[count // 2 - 1]) / 2
            std = math.sqrt(sum((_ - mean)**2 for _ in array) / count)
            stats[samples[i]] = [count, round(min_value, 4), round(max_value, 4), round(mean, 4), round(median, 4), round(std, 4)]
        else:
            stats[samples[i]] = ["NA", "NA", "NA", "NA", "NA", "NA"]
    yield "column\t" + "\t".join(samples)
    yield "count \t" + "\t".join(map(str, [stats[sample][0] for sample in samples]))
    yield "min   \t" + "\t".join(map(str, [stats[sample][1] for sample in samples]))
    yield "max   \t" + "\t".join(map(str, [stats[sample][2] for sample in samples]))
    yield "mean  \t" + "\t".join(map(str, [stats[sample][3] for sample in samples]))
    yield "median\t" + "\t".join(map(str, [stats[sample][4] for sample in samples]))
    yield "std   \t" + "\t".join(map(str, [stats[sample][5] for sample in samples]))


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
        if i == nlines:
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


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="TSV toolkit {}".format(__version__))
    parser.add_argument("input", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="file to parse, tab-delimited, default: stdin")
    parser.add_argument("-H", "--header", action="store_true", help="print header or include header in the output")
    parser.add_argument("-v", "--view", action="store_true", help="aligned display of each column")
    parser.add_argument("-s", "--stat", action="store_true", help="descriptive statistics")
    parser.add_argument("-p", "--pattern", type=str, help="pattern to match, wrap in single quotes")
    parser.add_argument("-a", "--add", type=str, help="add a new column with pattern, wrap in single quotes")
    parser.add_argument("-l", "--limit", type=int, default=100, help="limit of column width, used with -v, default: 100")
    parser.add_argument("-n", "--nlines", type=int, default=100, help="max number of lines to view, used with -v, default: 100")
    parser.add_argument("-c", "--column", type=int, default=0, help="column number to match (1-based), used with -s, default: 0, means all columns")
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args()
    file = args.input
    if args.pattern:
        file = get_pattern(file, args.pattern, args.header)
    if args.add:
        file = add_column(file, args.add, args.header)
    if args.stat:
        file = get_stats(file, args.header, args.column)
    if args.view:
        file = get_view(file, args.limit, args.nlines)
    if not (args.stat or args.view or args.pattern or args.add):
        if args.header:
            file = get_header(file)
        else:
            sys.exit(parser.print_help())
    for line in file:
        print(line.strip())


if __name__ == "__main__":
    main()
