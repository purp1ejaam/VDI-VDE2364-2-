import numpy as np
import matplotlib.pyplot as plt
from sol import Sol
from influenceOneParameter import calculate_influence
from SphereModels import generate_spheres_in_parallelepiped, plot_parallelepiped_with_spheres
from ProbingErrorPF import ProbingErrorPF

def run_influence_one_parameter():
    """
    Функция для работы с модулем InfluenceOneParameter.
    Строит графики зависимости SD от параметров Cx, Cy, Fx, Fy.
    """
    # Инициализация объекта Sol
    calc = Sol()

    # Параметры для цикла
    variations = ["Cx", "Cy", "Fx", "Fy"]
    ranges = {
        "Cx": (-100, 100, 1),  # Cx: от -100 до 100 с шагом 1
        "Cy": (-100, 100, 1),  # Cy: от -100 до 100 с шагом 1
        "Fx": (0.85, 1.15, 0.01),  # Fx: от 0.85 до 1.15 с шагом 0.01
        "Fy": (0.85, 1.15, 0.01),  # Fy: от 0.85 до 1.15 с шагом 0.01
    }
    colors = {
        "Cx": "blue",
        "Cy": "green",
        "Fx": "red",
        "Fy": "purple",
    }

    # Создаем фигуру для графиков
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Зависимость SD от различных параметров')

    # Перебираем все значения variation
    for i, variation in enumerate(variations):
        left, right, step = ranges[variation]
        values, sd_values = calculate_influence(calc, i + 1, 0, 0, 0, 0, left, right, step, variation)

        # Определяем позицию графика
        row = i // 2
        col = i % 2

        # Строим график
        axs[row, col].scatter(values, sd_values, c=colors[variation], marker='o', alpha=0.5, label=variation)
        axs[row, col].set_title(f'Зависимость SD от {variation}')
        axs[row, col].set_xlabel(variation)
        axs[row, col].set_ylabel('SD')
        axs[row, col].grid(True)
        axs[row, col].legend()

    # Отображаем графики
    plt.tight_layout()
    plt.show()

def run_probing_error_pf():
    """
    Функция для работы с модулем ProbingErrorPF.
    Строит график зависимости probingError от расстояния до начала координат.
    """
    # Параметры большого параллелепипеда
    big_width = 300
    big_length = 300
    big_height = 400

    # Параметры маленького параллелепипеда
    small_width = 100
    small_length = 100
    small_height = 100

    # Параметры сфер
    sphere_radius = 10

    # Создаем списки для накопления данных
    all_distances = []
    all_probingErrors = []
    all_num_points = []

    # Цикл по количеству точек на поверхности сферы
    for num_points in range(100, 2001, 100):  # От 100 до 2000 с шагом 100
        # Генерация данных для сфер
        spheres_data = generate_spheres_in_parallelepiped(big_width, big_length, big_height, small_width, small_length, small_height, sphere_radius, num_points)

        # Создаем экземпляр ProbingErrorPF и рассчитываем ошибки
        probing_error_pf = ProbingErrorPF()
        probingError, distance = probing_error_pf.calculate_errors(spheres_data)

        # Добавляем данные в общие списки
        all_distances.extend(distance)
        all_probingErrors.extend(probingError)
        all_num_points.extend([num_points] * len(distance))

    # Построение графика зависимости probingError от расстояния до начала координат
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(all_distances, all_probingErrors, c=all_num_points, cmap='viridis', marker='o', alpha=0.7)
    plt.title('Зависимость probingError от y')
    plt.xlabel('y')
    plt.ylabel('probingError (разница между R и оптимальным радиусом)')
    plt.grid(True)

    # Добавляем цветовую шкалу (legend)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Количество точек (num_points)')

    plt.show()

def main():
    """
    Основная функция, которая последовательно вызывает функции для работы с модулями.
    """
    # Сначала работаем с InfluenceOneParameter
    run_influence_one_parameter()

    # Затем работаем с ProbingErrorPF
    run_probing_error_pf()

if __name__ == "__main__":
    main()