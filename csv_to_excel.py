import argparse
import csv
import sys

def get_reader(csv_path, encoding, delimiter):
    f = open(csv_path, "r", newline="", encoding=encoding)
    if delimiter:
        return f, csv.reader(f, delimiter=delimiter)
    sample = f.read(65536)
    f.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample)
        return f, csv.reader(f, dialect=dialect)
    except Exception:
        return f, csv.reader(f)

def write_with_xlsxwriter(reader, xlsx_path, sheet_name):
    import xlsxwriter
    wb = xlsxwriter.Workbook(xlsx_path, {"constant_memory": True})
    ws = wb.add_worksheet(sheet_name)
    fmt = wb.add_format({"num_format": "@"})
    r = 0
    for row in reader:
        c = 0
        for val in row:
            ws.write_string(r, c, val if val is not None else "", fmt)
            c += 1
        r += 1
    wb.close()

def write_with_openpyxl(reader, xlsx_path, sheet_name):
    from openpyxl import Workbook
    from openpyxl.cell import WriteOnlyCell
    wb = Workbook(write_only=True)
    ws = wb.active
    ws.title = sheet_name
    for row in reader:
        cells = []
        for val in row:
            cell = WriteOnlyCell(ws, val if val is not None else "")
            cell.number_format = "@"
            cells.append(cell)
        ws.append(cells)
    wb.save(xlsx_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("xlsx_path")
    parser.add_argument("--delimiter")
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--sheet", default="Sheet1")
    parser.add_argument("--engine", choices=["xlsxwriter", "openpyxl"], default=None)
    args = parser.parse_args()

    try:
        f, reader = get_reader(args.csv_path, args.encoding, args.delimiter)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    chosen = args.engine
    if chosen == "xlsxwriter":
        try:
            write_with_xlsxwriter(reader, args.xlsx_path, args.sheet)
        except Exception as e:
            f.close()
            print(str(e), file=sys.stderr)
            sys.exit(1)
    elif chosen == "openpyxl":
        try:
            write_with_openpyxl(reader, args.xlsx_path, args.sheet)
        except Exception as e:
            f.close()
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        try:
            import xlsxwriter  # noqa: F401
            write_with_xlsxwriter(reader, args.xlsx_path, args.sheet)
        except Exception:
            try:
                write_with_openpyxl(reader, args.xlsx_path, args.sheet)
            except Exception as e:
                f.close()
                print(str(e), file=sys.stderr)
                sys.exit(1)
    f.close()

if __name__ == "__main__":
    main()

