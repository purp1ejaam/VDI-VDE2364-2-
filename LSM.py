import numpy as np
from scipy.optimize import minimize

class LSM:
    def calculate_best_sphere(self, points, radii):
        """
        Находит координаты центра и радиус сферы по методу наименьших квадратов.

        Параметры:
            points (ndarray): Массив точек на поверхности сферы (форма (N, 3)).
            radii (ndarray): Массив радиусов для каждой точки (форма (N,)).

        Возвращает:
            best_center (ndarray): Координаты центра сферы (форма (3,)).
            best_radius (float): Наиболее подходящий радиус.
        """
        # Начальное приближение: среднее значение точек как центр, среднее значение радиусов как радиус
        initial_center = np.mean(points, axis=0)
        initial_radius = np.mean(radii)

        # Целевая функция для минимизации
        def objective(params):
            center = params[:3]  # Первые три параметра — координаты центра
            radius = params[3]   # Четвертый параметр — радиус
            # Вычисляем теоретические радиусы для каждой точки
            theoretical_radii = np.linalg.norm(points - center, axis=1)
            # Сумма квадратов отклонений
            return np.sum((theoretical_radii - radius) ** 2)

        # Минимизация целевой функции
        result = minimize(objective, np.append(initial_center, initial_radius))

        # Возвращаем оптимальные значения
        best_center = result.x[:3]
        best_radius = result.x[3]
        return best_center, best_radius