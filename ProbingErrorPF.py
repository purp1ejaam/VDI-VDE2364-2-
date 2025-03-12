import numpy as np
import cv2
from LSM import LSM

class ProbingErrorPF:
    def __init__(self):
        """
        Инициализация матриц для калибровки (взяты из модуля Sol).
        """
        # Матрицы вращения и трансляции для первой камеры
        self.r0MtxMat = np.eye(3)
        self.t0MtxMat = np.zeros((3, 1))
        self.rt0MtxMat = np.hstack((self.r0MtxMat, self.t0MtxMat))

        # Матрицы вращения и трансляции для второй камеры
        self.rMtxMat = np.array([[0.995795942007291, -0.08267683970762237, -0.03943326080572061],
                                 [0.046365547158160644, 0.8262244791799492, -0.5614297338407952],
                                 [0.07899796148342211, 0.5572411059674096, 0.8265843404648324]])
        self.tMtxMat = np.array([[15.886730186679657], [403.9468824924481], [124.19305937214614]])
        self.rtMtxMat = np.hstack((self.rMtxMat, self.tMtxMat))

        # Матрицы коэффициентов дисторсии
        self.distCam1Mat = np.array([[-0.01515378274477495], [-0.045893170047044025], 
                                     [0.00038067776464809663], [0.00016247777657994083], [0.3395086736928184]])
        self.distCam2Mat = np.array([[-0.026020163652988537], [0.053310649891498425], 
                                     [0.00021642537482354708], [0.0007239228166972647], [0.0152156912572223]])

        # Матрицы внутренних параметров камер
        self.cam1MtxMat = np.array([[2325.14911420525, 0.0, 979.0],
                                    [0.0, 2333.05934136334874, 789.0],
                                    [0.0, 0.0, 1.0]])
        self.cam2MtxMat = np.array([[2328.4285337057236, 0.0, 1047.0],
                                    [0.0, 2336.4812340999565, 814.02],
                                    [0.0, 0.0, 1.0]])

    def calculate_errors(self, spheres_data):
        """
        Рассчитывает разницу между средним радиусом и оптимальным радиусом для каждой сферы.

        Параметры:
            spheres_data (list of dict): Список словарей, где каждый словарь содержит:
                                         - "points": массив точек на поверхности сферы (форма (N, 3)).
                                         - "center": координаты центра сферы (форма (3,)).

        Возвращает:
            probingError (list of float): Список разниц между средним и оптимальным радиусом для каждой сферы.
            distance (list of float): Список z-координат центров сфер.
        """
        probingError = []  # Список разниц между средним и оптимальным радиусом
        distance = []      # Список z-координат центров сфер

        for sphere in spheres_data:
            points = sphere["points"]
            center = sphere["center"]

            # Возвращаем z-координату центра сферы
            z_coord = center[1]  # Индекс 2 соответствует z-координате
            distance.append(z_coord)

            # Преобразуем точки в формат (N, 1, 3) для cv2.projectPoints
            points_3d = points.reshape(-1, 1, 3)

            # Проекция точек на изображения с двух камер
            points_2d_cam1, _ = cv2.projectPoints(points_3d, self.r0MtxMat, self.t0MtxMat, self.cam1MtxMat, self.distCam1Mat)
            points_2d_cam2, _ = cv2.projectPoints(points_3d, self.rMtxMat, self.tMtxMat, self.cam2MtxMat, self.distCam2Mat)

            # Триангуляция точек
            points_homo = cv2.triangulatePoints(self.rt0MtxMat, self.rtMtxMat, points_2d_cam1, points_2d_cam2)

            # Преобразование однородных координат в декартовы
            points_3d_triang = cv2.convertPointsFromHomogeneous(points_homo.T)

            # Вычисление радиусов для каждой точки
            radii = np.linalg.norm(points_3d_triang - center, axis=1)

            # Вычисление среднего радиуса R
            R = np.mean(radii)

            # Вызов модуля LSM для расчета оптимального радиуса
            lsm = LSM()
            best_center, best_radius = lsm.calculate_best_sphere(points_3d_triang.reshape(-1, 3), radii)

            # Вычисление разницы между R и оптимальным радиусом
            error = np.abs(R - best_radius)
            probingError.append(error)

        return probingError, distance