import math
from fractions import Fraction
from FA.LLL.myio import *
from FA.LLL.lattice import *

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


def my_create_matrix_from_knapsack(knap, the_sum):
    n = len(knap)
    m = int(0.5 * math.sqrt(n))+1
    matrix = [[0 for _ in range(n+1)] for _ in range(n+1)] # square matrix (n+1)*(n+1)

    for i in range(n):
        matrix[i][i] = 1
        matrix[i][n-1] = m*knap[i]
    for i in range(n):
        matrix[n][i] = Fraction(1, 2)
    matrix[n][n] = m*the_sum

    return matrix



def round(num):
    if num > 0:
        return int(num + Fraction(1, 2))
    else:
        return int(num - Fraction(1, 2))

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


def reduce(g, mu, k, l):
    row = len(g)

    if math.fabs(mu[k][l]) > Fraction(1, 2):
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


def lll_reduction(n, lc=Fraction(3, 4)):
    row = len(n)
    col = len(n[0])

    m = [[0 for _ in range(col)] for _ in range(row)]
    mu = [[0 for _ in range(col)] for _ in range(col)]
    g = [[n[i][j] for j in range(col)] for i in range(row)]
    B = [0 for _ in range(col)]

    gram_schmidt(g, m, mu, B)

    # k = 2
    k = 1

    while True:

        # 1 - perform (*) for l = k - 1
        reduce(g, mu, k, k - 1)

        # lovasz condition
        if B[k] < ((lc - mu[k][k - 1] * mu[k][k - 1]) * B[k - 1]):
            # 2
            # u = u[k][k-1]
            u = mu[k][k - 1]

            # B = Bk + u^2*Bk-1
            big_B = B[k] + (u * u) * B[k - 1]

            # mu[k][k-1] = u * B[k-1] / B
            mu[k][k - 1] = u * Fraction(B[k - 1], big_B)

            # Bk = Bk-1 * Bk / B
            B[k] = Fraction((B[k - 1] * B[k]), big_B)

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


def islll(n, lc=Fraction(3, 4)):
    row = len(n)
    col = len(n[0])

    m = [[0 for _ in range(col)] for _ in range(row)]
    mu = [[0 for _ in range(col)] for _ in range(col)]
    B = [0 for _ in range(col)]

    gram_schmidt(n, m, mu, B)

    for i in range(col):
        for j in range(i):
            if mu[i][j] > Fraction(1, 2) or mu[i][j] < -1 * Fraction(1, 2):
                return False

    for k in range(1, col):
        if B[k] < (lc - mu[k][k - 1] * mu[k][k - 1]) * B[k - 1]:
            return False
    return True


def other_solution():
    pubkey = [3780, 1337, 2902, 2101, 4410, 3629, 449, 2600, 4978, 4627]
    the_sum = 12266

    mat = create_matrix_from_knapsack(pubkey, the_sum)
    mat_reduced = lll_reduction(mat)
    best_vect = best_vect_knapsack(mat_reduced)
    apply_complementary = True
    for i in range(len(best_vect)):
        if best_vect[i] != 0:
            apply_complementary = False

    if apply_complementary:
        print("try complementary lattice")
        total_sum = 0
        for i in range(len(pubkey)):
            total_sum += pubkey[i]

        mat = create_matrix_from_knapsack(pubkey, total_sum-the_sum)
        mat_reduced = lll_reduction(mat)

        best_vect = best_vect_knapsack(mat_reduced)

        my_sum = 0
        for i in range(len(pubkey)):
            if best_vect[i] == 0:
                my_sum += pubkey[i]

        print("Verification :")
        print("my_sum = %ld, the_sum = %ld" % (my_sum, the_sum))

    else:
        my_sum = 0
        for i in range(len(pubkey)):
            if best_vect[i] == 1:
                my_sum += pubkey[i]

        print("Verification :")
        print("my_sum = %ld, the_sum = %ld" % (my_sum, the_sum))

    print("best_vect = ", best_vect)

if __name__ == '__main__':
    pubkey = [3780, 1337, 2902, 2101, 4410, 3629, 449, 2600, 4978, 4627]
    the_sum = 12266

    n = len(pubkey)

    matrix = my_create_matrix_from_knapsack(pubkey, the_sum)
    reduction = lll_reduction(matrix)
    result = [0] * n
    mysum = 0
    for b in reduction:
        flag = True
        for i in range(n):
            if math.fabs(b[i]) != Fraction(1, 2):
                flag = False
                break
        if flag:
            if b[n] != 0:
                flag = False
                continue
        if flag:
            for i in range(n):
                result[i] = b[i] + Fraction(1, 2)
                mysum += result[i] * pubkey[i]
            if mysum == the_sum:
                print(F"Result: {result}")
                break
            mysum = 0
            for i in range(n):
                result[i] = -b[i] + Fraction(1, 2)
                mysum += result[i] * pubkey[i]
            if mysum == the_sum:
                print(F"Result: {result}")
                break

    print("There is no result")
    print("Try other solution")
    other_solution()



