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
#   - Output in guman way
#   - Vector arithmetic
#   -


def matrix_mult(a, b):
    m = len(a)
    n = len(b[0])
    p = len(a[0])
    result = [[0] * n] * m
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




if __name__ == '__main__':
    print("hello")
