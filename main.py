from time import time
from math import log2, ceil
from sympy import isprime, is_quad_residue, sqrt_mod
from operations_over_EC import Curve, Point


def P(x):
    return 36 * x ** 4 + 36 * x ** 3 + 24 * x ** 2 + 6 * x + 1


def get_smallest_x(m):
    """
    :param m: бажана бінарна довжина p і n
    :return: найменше х
    """
    left = 2 ** (m // 4 - 2)
    right = 2 ** (m // 4 + 2)

    while left < right:
        x = (left + right) // 2
        c = ceil(log2(P(-x)))
        if c < m:
            left = x + 1
        else:
            right = x

    return left


def get_pair(m):
    """
    Пошук пари простих чисел p і n

    :param m: бінарна довжина m
    :return: p і n
    """
    x = get_smallest_x(m)

    while True:
        t = 6 * x ** 2 + 1
        p = P(-x)
        n = p + 1 - t
        if isprime(p) and isprime(n):
            return p, n, t
        p = P(x)
        n = p + 1 - t
        if isprime(p) and isprime(n):
            return p, n, t
        x += 1


def is_identity(point):
    return point.identity


def get_curve(n, p):
    """
    Знаходження кривої за параметрами n і p

    :return: параметр b у рівнянні кривої та породжуюча точка
    """
    b = 1
    while True:
        b += 1
        while not is_quad_residue(b + 1, p):
            b += 1
        y = sqrt_mod(b + 1, p)
        ec = Curve(p, n, b)
        G = ec.new_point(1, y)
        if G in ec and is_identity(n * G):
            break

    return b, Point((1, y), ec)


if __name__ == '__main__':
    m = int(input('m: '))
    start = time()
    p, n, t = get_pair(m)
    end1 = time()
    print(f'Час роботи get_pair: {end1 - start} с')
    print(f'p: {p} {len(bin(p)[2:])} біт')
    print(f'n: {n} {len(bin(n)[2:])} біт')
    print(f't: {t} {len(bin(t)[2:])} біт')
    start1 = time()
    b, point = get_curve(n, p)
    end = time()
    print(f'Час роботи get_curve: {end - start1} с')
    print(f'b: {b}')
    print(f'G(1,y): {point}')
    print(f'Загальний час роботи: {end - start} с')
    print()
