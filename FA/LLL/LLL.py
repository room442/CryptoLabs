## Main task:
## TODO:   1. Написать программу, которая реализует LLL-алгоритм

# TODO:   2. На простых примерах убедиться в корректности реализации.
#   Проверить результаты работы в известных математических пакетах,
#   например, Mathematica, Sage и др.

## TODO:   3. Реализовать алгоритм решения аддитивной задачи об укладке
#   ранца на базе LLL-алгоритма. Проанализировать, при каких входных
#   данных алгоритм с наибольшей вероятностью успешно завершается
#   в условиях существования решения.

## TODO:   4. Обосновать полученные результаты.


# my plan
# TODO:
#   - Lattice arithmetic (matrix?)
#   - Output in human way
#   - Vector arithmetic
#   -


def matrix_mult(a, b):
    m = len(a)
    n = len(b[0])
    p = len(a[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            cell = 0
            for k in range(p):
                cell += a[i][k] * b[k][j]
            result[i][j] = cell

    return result


def scalar_prod(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]

    return result


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


def get_vector(n, j):
    return [n[i][j] for i in range(len(n))]


def vector_add(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def vector_sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def vector_mult_const(v, k):
    return [v[i] * k for i in range(len(v))]


def set_matrix_vector(a, k, v):
    for i in range(len(a)):
        a[i][k] = v[i]


def norml2(a):
    return scalar_prod(a, a)


def create_matrix_from_knapsack(knap, the_sum):
    n = len(knap)
    result = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(n):
        for j in range(n):
            if i == j:
                result[i][j] = 1

    i = i + 1
    for k in range(n):
        result[i][k] = knap[k]

    result[i][k + 1] = -the_sum

    return result


def round(num):
    if num > 0:
        return int(num + 1 / 2)
    else:
        return int(num - 1 / 2)


def create_matrix(n):
    return [[n[i][j] for j in range(len(n))] for i in range(len(n[0]))]


def heuristic_u_plus_v(n):
    row = len(n)
    col = len(n[0])
    # negative vectors
    minus_1_tab = []
    # positive vectors
    plus_1_tab = []

    # this vector finishes with -1
    minus_1_vect = [0] * row
    # this vector finishes with 1
    plus_1_vect = [0] * row

    for i in range(col):
        if n[row - 1][i] == 1:
            for j in range(row):
                plus_1_vect[j] = int(n[j][i])

            if plus_1_vect not in plus_1_tab:
                plus_1_tab.append(plus_1_vect)

        elif n[row - 1][i] == -1:
            for j in range(row):
                minus_1_vect[j] = int(n[j][i])

            if minus_1_vect not in minus_1_tab:
                minus_1_tab.append(minus_1_vect)
    return vector_add(minus_1_vect, plus_1_vect)[:-1]


def best_vect_knapsack(n):
    row = len(n)
    col = len(n[0])

    best_vect = [0] * row
    solution = [0] * (row - 1)

    for i in range(col):
        if n[row - 1][i] == 0:
            take_it = True

            for j in range(row):
                if n[j][i] != 1:
                    if n[j][i] != 0:
                        take_it = False

            if take_it:
                for j in range(row):
                    if n[j][i] == 1:
                        best_vect[j] = 1
                    elif n[j][i] == 0:
                        best_vect[j] = 0
                break;

    apply_heuristic = True
    for i in range(row):
        if best_vect[i] != 0:
            apply_heuristic = False

    if apply_heuristic:
        print("No direct solution found, apply heuristic")
        solution = heuristic_u_plus_v(n)
        for i in range(len(solution)):
            if solution[i] != 1:
                if solution[i] != 0:
                    # apply complement
                    print("no solution found with heuristics")
                    return [0] * row
    else:
        for i in range(row - 1):
            solution[i] = best_vect[i]
    return solution


# gram schmidt algorithm
def gram_schmidt(g, m, mu, B):
    col = len(g[0])

    for i in range(col):
        # bi* = bi
        b_i = get_vector(g, i)
        b_i_star = b_i
        set_matrix_vector(m, i, b_i_star)

        for j in range(i):
            # u[i][j] = (bi, bj*)/Bj
            b_j_star = get_vector(m, j)
            b_i = get_vector(g, i)
            B[j] = norml2(b_j_star)
            mu[i][j] = scalar_prod(b_i, b_j_star), B[j]
            # bi* = bi* - u[i][j]* bj*
            b_i_star = vector_sub(b_i_star, vector_mult_const(b_j_star, mu[i][j]))
            set_matrix_vector(m, i, b_i_star)

        b_i_star = get_vector(m, i)
        # B[i] = (bi*, bi*)
        B[i] = scalar_prod(b_i_star, b_i_star)


def reduce(g, mu, k, l):
    row = len(g)

    if mu[k][l] > 1 / 2 or mu[k][l] < -(1 / 2):
        r = round(mu[k][l])
        b_k = get_vector(g, k)
        b_l = get_vector(g, l)
        # bk = bk - r*bl
        set_matrix_vector(g, k, vector_sub(b_k, vector_mult_const(b_l, r)))

        for j in range(l):
            # u[k][j] = u[k][j] - r*u[l][j]
            mu[k][j] = mu[k][j] - r * mu[l][j]

        # u[k][l] = u[k][l] - r
        mu[k][l] = mu[k][l] - r


def lll_reduction(n, lc=3/4):
    row = len(n)
    col = len(n[0])

    m = [[0 for _ in range(col)] for _ in range(row)]
    mu = [[0 for _ in range(col)] for _ in range(col)]
    g = [[n[i][j] for j in range(col)] for i in range(row)]
    B = [0 for _ in range(col)]

    gram_schmidt(g, m, mu, B)

    # k = 2
    k = 1

    while 1:

        # 1 - perform (*) for l = k - 1
        reduce(g, mu, k, k - 1)

        # lovasz condition
        if B[k] < (lc - mu[k][k - 1] * mu[k][k - 1]) * B[k - 1]:
            # 2
            # u = u[k][k-1]
            u = mu[k][k - 1]

            # B = Bk + u^2*Bk-1
            big_B = B[k] + (u * u) * B[k - 1]

            # mu[k][k-1] = u * B[k-1] / B
            mu[k][k - 1] = u * (B[k - 1] / big_B)

            # Bk = Bk-1 * Bk / B
            B[k] = (B[k - 1] * B[k]) / big_B

            # Bk-1 = B
            B[k - 1] = big_B

            # exchange bk and bk-1
            b_k = get_vector(g, k)
            b_k_minus_1 = get_vector(g, k - 1)
            set_matrix_vector(g, k, b_k_minus_1)
            set_matrix_vector(g, k - 1, b_k)

            # for j = 0 .. k-2
            for j in range(k - 1):
                save = mu[k - 1][j]
                mu[k - 1][j] = mu[k][j]
                mu[k][j] = save

            for i in range(k + 1, col):
                save = mu[i][k - 1]
                mu[i][k - 1] = mu[k][k - 1] * mu[i][k - 1] + mu[i][k] - u * mu[i][k] * mu[k][k - 1]
                mu[i][k] = save - u * mu[i][k]

            # if k > 2
            if k > 1:
                k = k - 1

        else:
            for l in range(k - 2, -1, -1):
                reduce(g, mu, k, l)

            if k == col - 1:
                return g

            k = k + 1


def islll(n, lc=3 / 4):
    row = len(n)
    col = len(n[0])

    m = [[0 for _ in range(col)] for _ in range(row)]
    mu = [[0 for _ in range(col)] for _ in range(col)]
    B = [0 for _ in range(col)]

    gram_schmidt(n, m, mu, B)

    for i in range(col):
        for j in range(i):
            if mu[i][j] > 1 / 2 or mu[i][j] < -1 / 2:
                return False

    for k in range(1, col):
        if B[k] < (lc - mu[k][k - 1] * mu[k][k - 1]) * B[k - 1]:
            return False
    return True


if __name__ == '__main__':
    print("hello")
