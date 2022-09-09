def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        yield (col, line[col:col_end])
        col = find_col(line, col_end, lambda x: not x.isspace())         



def lex_file(file_path):
    with open(file_path, "r") as f:
        return [(file_path, row, col, token)
                for (row, line) in enumerate(f.readlines())
                for (col, token) in lex_line(line)]
