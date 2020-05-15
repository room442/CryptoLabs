def print_matrix(a):
    maxlen = 0
    for row in a:
        for elem in row:
            if len(str(elem)) > maxlen:
                maxlen = len(str(elem))

    for row in a:
        row_str = ""
        for elem in row:
            difflen = maxlen - len(str(elem))
            sep = " "
            for i in range(difflen):
                sep = sep + " "
            row_str = row_str + sep + str(elem)
        print(row_str)


def print_vector(v):
    print(" ".join(str(i) for i in v))