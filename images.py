class Long:
    letters = ('', 'k', 'B', 'T', 'q', 'Q', 's', 'S', 'O', 'n', 'd')
    limit = 10

    def __init__(self, num, e=None):
        if e is None:
            if isinstance(num, str):
                if 'e' in num:
                    num, e = num.split('e')
                else:
                    for i in range(1, len(self.letters)):
                        if num.endswith(self.letters[i]):
                            num, e = num.replace(self.letters[i], ''), i * 3
                            break
                    else:
                        num, e = float(num), 0
                num, e = float(num), int(e)
            elif isinstance(num, Long):
                num, e = num.num, num.e
            else:
                e = 0
        self.num = num
        self.e = e
        self.check()

    def check(self):
        if abs(self.num) >= 10:
            while self.num >= 10:
                self.num /= 10
                self.e += 1
            self.num = round(self.num, self.limit)
        elif abs(self.num) < 1 and self.num != 0:
            while self.num < 0.1:
                self.num *= 10
                self.e += 1

    def __neg__(self):
        return Long(-self.num, self.e)

    def __add__(self, other, ret=None):
        other = Long(other)
        if ret is None:
            ret = Long(self)
        m = ret.e - other.e
        if m >= ret.limit:
            return ret
        if -m >= other.limit:
            return other
        ret.num += other.num * 10 ** -m
        ret.check()
        return ret

    def __iadd__(self, other):
        return self.__add__(other, self)

    def __sub__(self, other):
        return self.__add__(-other)

    def __isub__(self, other):
        return self.__iadd__(-other)

    def __mul__(self, other, ret=None):
        other = Long(other)
        if ret is None:
            ret = Long(self)
        ret.e += other.e
        ret.num *= other.num
        ret.check()
        return ret

    def __imul__(self, other):
        return self.__mul__(other, self)

    def __radd__(self, other):
        pass

    def __truediv__(self, other, ret=None):  # why it is not "/" function?
        other = Long(other)
        if ret is None:
            ret = Long(self)
        ret.e -= other.e
        ret.num /= other.num
        ret.check()
        return ret

    def __idiv__(self, other):
        return self.__truediv__(other, self)

    def __pow__(self, power, modulo=None, ret=None):
        if ret is None:
            ret = Long(self)
        ret.e *= power
        ret.num **= power
        ret.check()
        return ret

    def __ipow__(self, other):
        return self.__pow__(other, ret=self)

    @staticmethod
    def _check_other(other):
        if not isinstance(other, Long):
            try:
                return Long(other)
            except ValueError:
                return False
        return other

    def __eq__(self, other):  # ==
        other = self._check_other(other)
        return False if other is False else (self.e == other.e and self.num == other.num)

    def __gt__(self, other):  # >
        other = self._check_other(other)
        return False if other is False else (self.e > other.e or self.e == other.e and self.num > other.num)

    def __ge__(self, other):  # >=
        other = self._check_other(other)
        return False if other is False else (self.e > other.e or self.e == other.e and self.num >= other.num)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):  # <
        return not self.__gt__(other)

    def __le__(self, other):  # <=
        return not self.__ge__(other)

    def __str__(self):
        if self.e >= len(self.letters) * 3 or self.e < 0:
            return str(round(self.num, 3)) + 'e' + str(self.e)
        letter = str(self.letters[abs(self.e) // 3])
        return str(round(self.num * 10 ** (self.e % 3), 3)) + letter

    def __repr__(self):
        return self.__str__()


class Point:
    def __init__(self, x, y=None):
        if y is None:
            x, y = x
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise KeyError('Wrong key')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value

    def __iter__(self):
        return self.as_tuple().__iter__()

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __iadd__(self, other):
        self.x, self.y = self.x + other[0], self.y + other[1]
        return self

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __isub__(self, other):
        self.x, self.y = self.x - other[0], self.y - other[1]
        return self

    def __mul__(self, other):
        return Point(self.x * other[0], self.y * other[1])

    def __imul__(self, other):
        self.x, self.y = self.x * other[0], self.y * other[1]
        return self

    def __truediv__(self, other):
        return Point(self.x / other[0], self.y / other[1])

    def __idiv__(self, other):
        self.x, self.y = self.x / other[0], self.y / other[1]
        return self

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1] if isinstance(other, (tuple, list, Point)) else False

    def __gt__(self, other):
        return self.x > other[0] and self.y > other[1] if isinstance(other, (tuple, list, Point)) else False

    def __ge__(self, other):
        return self.x >= other[0] and self.y >= other[1] if isinstance(other, (tuple, list, Point)) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.x < other[0] and self.y < other[1] if isinstance(other, (tuple, list, Point)) else False

    def __le__(self, other):
        return self.x <= other[0] and self.y <= other[1] if isinstance(other, (tuple, list, Point)) else False

    def __bool__(self):
        return True

    def __str__(self):
        return 'Point%s' % str((self.x, self.y))

    def __repr__(self):
        return self.__str__()
