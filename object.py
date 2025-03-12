import numpy as np

class Object:
    def CenterCoordinate(self, type, a, b, c):
        L1 = 720
        return self.Points(type, a, b, c, L1)
    
    def Dp1(self, a, b, c):
        return 0.02 * np.sqrt(a * a + b * b + c * c)
    
    def func(self, first, second, Lp):
        return (np.sqrt(first * first + second * second) - Lp) / 2
    
    def Points(self, type, a, b, c, L1):
        L0 = np.sqrt(a * a + b * b + c * c)
        Dp = 0.02 * L0  # диаметр окружности
        Lp = 0.4 * L0  # Расстояние между сферами

        # Каждая point содержит координаты центров двух сфер, расположенных на "штанге" - всего 14 сфер(координат).
        # Координаты записаны последовательно Z,X,Y.
        # Сама штанга расположена в объеме согласно стандарту (7 положений = 7 point),
        # а её положение на определенной стороне\диагонали объема всегда в центре стороны\диагонали.
        point1 = np.array([[L1 - a / 2, b / 2, Lp / 2], [L1 - a / 2, b / 2, -Lp / 2]])
        point2 = np.array([[L1 - Lp / 2, -b / 2, c / 2], [L1 + Lp / 2, -b / 2, c / 2]])
        point3 = np.array([[L1 + a / 2 - self.func(a, b, Lp) * a / np.sqrt(a * a + b * b),
                           -b / 2 + self.func(a, b, Lp) * b / np.sqrt(a * a + b * b), -c / 2],
                          [L1 + a / 2 - (self.func(a, b, Lp) + Lp) * a / np.sqrt(a * a + b * b),
                           -b / 2 + (self.func(a, b, Lp) + Lp) * b / np.sqrt(a * a + b * b), -c / 2]])
        point4 = np.array([[L1 + a / 2 - ((self.func(a, c, Lp) + Lp) * a / np.sqrt(a * a + c * c)),
                           b / 2, -c / 2 + self.func(a, c, Lp) * c / np.sqrt(a * a + c * c)],
                          [L1 + a / 2 - self.func(a, c, Lp) * a / np.sqrt(a * a + c * c),
                           b / 2, -c / 2 + ((self.func(a, c, Lp) + Lp) * c / np.sqrt(a * a + c * c))]])
        point5 = np.array([[L1 + a / 2 - ((self.func(a, c, Lp) + Lp) * a / np.sqrt(a * a + c * c)),
                           -b / 2, -c / 2 + self.func(a, c, Lp) * c / np.sqrt(a * a + c * c)],
                          [L1 + a / 2 - self.func(a, c, Lp) * a / np.sqrt(a * a + c * c),
                           -b / 2, -c / 2 + ((self.func(a, c, Lp) + Lp) * c / np.sqrt(a * a + c * c))]])
        point6 = np.array([[L1 + a / 2, -b / 2 + ((self.func(a, c, Lp) + Lp) * a / np.sqrt(a * a + c * c)),
                           -c / 2 + self.func(a, c, Lp) * c / np.sqrt(a * a + c * c)],
                          [L1 + a / 2, -b / 2 + self.func(a, c, Lp) * a / np.sqrt(a * a + c * c),
                           -c / 2 + ((self.func(a, c, Lp) + Lp) * c / np.sqrt(a * a + c * c))]])
        
        n = np.sqrt(a * a + b * b) - ((self.func(L0, 0, Lp) + Lp) * np.sqrt(a * a + b * b)) / L0
        m = np.sqrt(a * a + b * b) - self.func(L0, 0, Lp) * np.sqrt(a * a + b * b) / L0
        point7 = np.array([[L1 - a / 2 + a * n / np.sqrt(a * a + b * b),
                            b / 2 - b * n / np.sqrt(a * a + b * b), -c / 2 + self.func(L0, 0, Lp) * c / L0],
                           [L1 - a / 2 + a * m / np.sqrt(a * a + b * b),
                            b / 2 - b * m / np.sqrt(a * a + b * b), -c / 2 + (self.func(L0, 0, Lp) + Lp) * c / L0]])
        
        if type == 1:
            return point1
        elif type == 2:
            return point2
        elif type == 3:
            return point3
        elif type == 4:
            return point4
        elif type == 5:
            return point5
        elif type == 6:
            return point6
        elif type == 7:
            return point7
        else:
            return point7