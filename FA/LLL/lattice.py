from fractions import Fraction

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

def create_matrix(n):
    row = len(n)
    col = len(n[0])
    return [ [Fraction(n[i][j]) for j in range(col) ] for i in range(row)]

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
            mu[i][j] = Fraction(scalar_prod(b_i, b_j_star), B[j])
            # bi* = bi* - u[i][j]* bj*
            b_i_star = vector_sub(b_i_star, vector_mult_const(b_j_star, mu[i][j]))
            set_matrix_vector(m, i, b_i_star)

        b_i_star = get_vector(m, i)
        # B[i] = (bi*, bi*)
        B[i] = scalar_prod(b_i_star, b_i_star)