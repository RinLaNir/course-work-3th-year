class Curve:
    """
    Клас еліптичної кривої, який містить її опис
    """
    def __init__(self, p, n, b, equation='y**2 - x**3 - self.b'):
        self.b = b
        self.n = n
        self.p = p
        self.equation = equation

    def eq(self, point):
        """
        Обчислює рівняння кривої для заданої точки.
        Використовується в перевірці чи належить точка кривій

        :param point: точка із координатами (x,y)
        :return: значення self.equation на ції точці
        """
        x, y = point
        return eval(self.equation)

    def __contains__(self, point):
        """
        Перевірка нележности точки кривій.
        Якщо точка нейтральний елемент або рівняння на її координатах
        дорівнює нулю, то вона належить еліптичній кривій, інакше
        не належить.

        :param point: точка, яку ми збираємось перевірити
        :return: True якщо належить, інакше False
        """
        if isinstance(point, Point):
            return True if point.identity or \
                           self.eq((point.x, point.y)) % self.p == 0 else False
        else:
            return False

    def new_point(self, x, y):
        """
        Створення нової точки на кривій

        :param x: х координата точки
        :param y: у координата точки
        :return: Клас Point
        """
        return Point((x, y), self)


class Point:
    """
    Клас, що описує точки еліптичної кривої та дії над ними
    """
    def __init__(self, point, curve):
        self.curve = curve
        self.x, self.y = point
        if point == (0, 0):
            self.identity = True
        else:
            self.identity = False

        assert self in self.curve

    def __neg__(self):
        """
        Взяття оберненого елемента точки
        """
        assert self in self.curve

        if self.identity:
            return self

        self.y = -self.y % self.curve.p
        assert self in self.curve

        return self

    def __add__(self, other):
        """
        Обчислення суми двох точок
        """
        assert self in self.curve
        assert other in self.curve
        assert self.curve is other.curve

        if self.identity:
            return other.__copy__()
        if other.identity:
            return self.__copy__()

        if self.x == other.x and self.y != other.y:
            return Point((0, 0), self.curve)

        if self.x == other.x:
            m = (3 * self.x ** 2) * inverse_mod(2 * self.y, self.curve.p)
        else:
            m = (self.y - other.y) * inverse_mod(self.x - other.x, self.curve.p)

        x = m ** 2 - self.x - other.x
        y = self.y + m * (x - self.x)

        new_point = Point((x % self.curve.p, -y % self.curve.p), self.curve)
        assert new_point in self.curve
        return new_point

    def __str__(self):
        return f'{self.x, self.y}'

    def __copy__(self):
        return Point((self.x, self.y), self.curve)

    def __mul__(self, other: int):
        """
        Множення точки на ціле число
        """
        assert isinstance(other, int)
        assert self in self.curve

        if other < 0:
            return (-self).__mul__(-other)

        result = Point((0, 0), self.curve)
        addend = self

        while other:
            if other & 1:
                result = result + addend

            addend = addend + addend
            other >>= 1

        assert result in self.curve
        return result

    def __rmul__(self, other):
        return self.__mul__(other)


def egcd(a, b):
    """
    Алгоритм Евкліда. Використовується в inverse_mod
    """
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x, y


def inverse_mod(k, p):
    """
    Взяття оберненого елемента за модулем p
    """
    if k == 0: raise ZeroDivisionError('division by zero')
    if k < 0 : return p - inverse_mod(-k, p)
    gcd, x, y = egcd(k, p)

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


def get_test_curve():
    p = 1461501624496790265145448589920785493717258890819
    n = 1461501624496790265145447380994971188499300027613
    b = 3
    return Curve(p, n, b)


if __name__ == '__main__':
    ec = get_test_curve()
    G = ec.new_point(1, 2)
    print(f'Point G: {G}')
    print(f'G + G: {G + G}')
    print(f'nG: {ec.n * G}')
