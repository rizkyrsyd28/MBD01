def read(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        divider = lines.index("---- BEGIN EXECUTION ----")

        timestamps = lines[0:divider]

        operations = lines[divider + 1:]

        f.close()
        return timestamps, operations
