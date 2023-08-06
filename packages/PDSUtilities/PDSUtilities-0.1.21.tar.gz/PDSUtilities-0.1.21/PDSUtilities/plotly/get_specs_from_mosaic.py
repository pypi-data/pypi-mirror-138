def get_specs_from_mosaic(mosaic):
    def get_spec_from_mosaic(mosaic, row, col):
        rows, cols = [], []
        for r in range(len(mosaic)):
            for c in range(len(mosaic[r])):
                if mosaic[r][c] == mosaic[row][col]:
                    rows.append(r)
                    cols.append(c)
        min_of_rows, max_of_rows = min(rows), max(rows)
        min_of_cols, max_of_cols = min(cols), max(cols)
        #
        if row == min_of_rows and col == min_of_cols:
            spec = {}
            if min_of_rows < max_of_rows:
                spec['rowspan'] = max_of_rows - min_of_rows + 1
            if min_of_cols < max_of_cols:
                spec['colspan'] = max_of_cols - min_of_cols + 1
            return spec
        return None

    if isinstance(mosaic, str):
        mosaic = [line.strip() for line in mosaic.splitlines()]
    mosaic = [[c for c in line] for line in mosaic if line]
    return [
        [
            get_spec_from_mosaic(mosaic, r, c)
            for c in range(len(mosaic[r]))
        ] for r in range(len(mosaic))
    ]
