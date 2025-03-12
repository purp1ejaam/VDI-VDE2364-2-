import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_sphere_points(n=100, L0=1.0):
    """
    Генерирует точки на сфере с использованием золотого сечения.

    Параметры:
        n (int): Количество точек. По умолчанию 50.
        L0 (float): Параметр, используемый для вычисления радиуса сферы. По умолчанию 1.0.

    Возвращает:
        x, y, z (ndarray): Координаты точек на сфере.
    """
    radius = 0.02 * L0  # Радиус сферы
    i = np.arange(0, n, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    golden_ratio = (1 + 5**0.5) / 2
    theta = 2 * np.pi * i / golden_ratio
    x, y, z = radius * np.cos(theta) * np.sin(phi), radius * np.sin(theta) * np.sin(phi), radius * np.cos(phi)
    return x, y, z

def generate_spheres_in_parallelepiped(big_width, big_length, big_height, small_width, small_length, small_height, sphere_radius, num_points):
    """
    Генерирует сферы внутри большого параллелепипеда, заполненного маленькими параллелепипедами.

    Параметры:
        big_width (float): Ширина большого параллелепипеда.
        big_length (float): Длина большого параллелепипеда.
        big_height (float): Высота большого параллелепипеда.
        small_width (float): Ширина маленького параллелепипеда.
        small_length (float): Длина маленького параллелепипеда.
        small_height (float): Высота маленького параллелепипеда.
        sphere_radius (float): Радиус сфер.
        num_points (int): Количество точек на поверхности сферы.

    Возвращает:
        spheres_data (list of dict): Список словарей с данными о сферах.
                                    Каждый словарь содержит:
                                    - "points": массив точек на поверхности сферы (форма (N, 3)).
                                    - "center": координаты центра сферы (форма (3,)).
    """
    spheres_data = []

    # Количество маленьких параллелепипедов по каждой оси
    num_cubes_x = int(big_width // small_width)
    num_cubes_y = int(big_length // small_length)
    num_cubes_z = int(big_height // small_height)

    # Начальные координаты большого параллелепипеда (с учетом смещения по z)
    start_x = -big_width / 2
    start_y = -big_length / 2
    start_z = 720 - big_height / 2  # Центр большого параллелепипеда в z = 720

    # Генерация данных для каждой сферы
    for i in range(num_cubes_x):
        for j in range(num_cubes_y):
            for k in range(num_cubes_z):
                # Координаты центра маленького параллелепипеда (с учетом смещения по z)
                center_x = start_x + (i + 0.5) * small_width
                center_y = start_y + (j + 0.5) * small_length
                center_z = start_z + (k + 0.5) * small_height
                center = np.array([center_x, center_y, center_z])

                # Генерация точек на поверхности сферы
                x_points, y_points, z_points = generate_sphere_points(num_points, L0=np.sqrt(big_width**2 + big_length**2 + big_height**2))
                points = np.column_stack((x_points, y_points, z_points)) + center

                # Добавляем данные сферы в список
                spheres_data.append({
                    "points": points,
                    "center": center
                })

    return spheres_data

def plot_parallelepiped_with_spheres(big_width, big_length, big_height, small_width, small_length, small_height, spheres_data):
    """
    Визуализирует большой параллелепипед и сферы с точками.

    Параметры:
        big_width (float): Ширина большого параллелепипеда.
        big_length (float): Длина большого параллелепипеда.
        big_height (float): Высота большого параллелепипеда.
        small_width (float): Ширина маленького параллелепипеда.
        small_length (float): Длина маленького параллелепипеда.
        small_height (float): Высота маленького параллелепипеда.
        spheres_data (list of dict): Список словарей с данными о сферах.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Визуализация большого параллелепипеда (с учетом смещения по z)
    big_cube_edges = create_cube((-big_width / 2, -big_length / 2, 720 - big_height / 2), (big_width, big_length, big_height))
    for edge in big_cube_edges:
        ax.plot3D(*zip(*edge), color='black', linewidth=2)

    # Визуализация сфер с точками
    for sphere in spheres_data:
        points = sphere["points"]
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='red', s=10)

    # Настройка осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-big_width / 2, big_width / 2)
    ax.set_ylim(-big_length / 2, big_length / 2)
    ax.set_zlim(720 - big_height / 2, 720 + big_height / 2)  # Центр в z = 720

    plt.show()

def create_cube(origin, size):
    """
    Создает вершины и рёбра куба.

    Параметры:
        origin (tuple): Координаты начала куба (x, y, z).
        size (tuple): Размеры куба (dx, dy, dz).

    Возвращает:
        edges (list): Список рёбер куба.
    """
    x, y, z = origin
    dx, dy, dz = size
    vertices = [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz],
    ]
    edges = [
        [vertices[0], vertices[1]],
        [vertices[1], vertices[2]],
        [vertices[2], vertices[3]],
        [vertices[3], vertices[0]],
        [vertices[4], vertices[5]],
        [vertices[5], vertices[6]],
        [vertices[6], vertices[7]],
        [vertices[7], vertices[4]],
        [vertices[0], vertices[4]],
        [vertices[1], vertices[5]],
        [vertices[2], vertices[6]],
        [vertices[3], vertices[7]],
    ]
    return edges