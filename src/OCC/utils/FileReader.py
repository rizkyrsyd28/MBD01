def read(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        divider = lines.index("---- BEGIN EXECUTION ----")

        operations = lines[divider + 1:]
        j = 0
        for i in range(len(operations)):
            if(len(operations[j])<5):
                operations.remove(operations[j])
                j -= 1
            j += 1

        f.close()
        return operations
