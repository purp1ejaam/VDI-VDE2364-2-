import numpy as np
import cv2
from object import Object

class Sol:
    def calc(self, type, a, b, c, devCx1, devCx2, devCy1, devCy2, devFx1, devFy1, devFx2, devFy2):
        # Матрицы для калибровки
        r0MtxMat = np.eye(3)
        t0MtxMat = np.zeros((3, 1))
        rt0MtxMat = np.hstack((r0MtxMat, t0MtxMat))
        
        rMtxMat = np.array([[0.995795942007291, -0.08267683970762237, -0.03943326080572061],
                            [0.046365547158160644, 0.8262244791799492, -0.5614297338407952],
                            [0.07899796148342211, 0.5572411059674096, 0.8265843404648324]])
        tMtxMat = np.array([[15.886730186679657], [403.9468824924481], [124.19305937214614]])
        rtMtxMat = np.hstack((rMtxMat, tMtxMat))
        
        distCam1Mat = np.array([[-0.01515378274477495], [-0.045893170047044025], [0.00038067776464809663], [0.00016247777657994083], [0.3395086736928184]])
        distCam2Mat = np.array([[-0.026020163652988537], [0.053310649891498425], [0.00021642537482354708], [0.0007239228166972647], [0.0152156912572223]])
        
        cam1MtxMat = np.array([[2325.14911420525, 0.0, 979.0],
                               [0.0, 2333.05934136334874, 789.0],
                               [0.0, 0.0, 1.0]])
        cam2MtxMat = np.array([[2328.4285337057236, 0.0, 1047.0],
                               [0.0, 2336.4812340999565, 814.02],
                               [0.0, 0.0, 1.0]])
        
        cam11MtxMat = np.array([[2325.14911420525 * devFx1, 0.0, 979.0 + devCx1],
                                [0.0, 2333.05934136334874 * devFy1, 789.0 + devCy1],
                                [0.0, 0.0, 1.0]])
        cam22MtxMat = np.array([[2328.4285337057236 * devFx2, 0.0, 1047.0 + devCx2],
                                [0.0, 2336.4812340999565 * devFy2, 814.02 + devCy2],
                                [0.0, 0.0, 1.0]])
        
        k = Object()
        firstMat3D = np.array([[k.CenterCoordinate(type, 400, 400, 300)[0, 1]],
                              [k.CenterCoordinate(type, 400, 400, 300)[0, 2]],
                              [k.CenterCoordinate(type, 400, 400, 300)[0, 0]]])
        secondMat3D = np.array([[k.CenterCoordinate(type, 400, 400, 300)[1, 1]],
                               [k.CenterCoordinate(type, 400, 400, 300)[1, 2]],
                               [k.CenterCoordinate(type, 400, 400, 300)[1, 0]]])
        
        # Рассчитываем 2D координаты
        firstFirstImgMat2D, _ = cv2.projectPoints(firstMat3D, rMtxMat, tMtxMat, cam2MtxMat, distCam2Mat)
        firstSecImgMat2D, _ = cv2.projectPoints(firstMat3D, r0MtxMat, t0MtxMat, cam1MtxMat, distCam1Mat)
        secondFirstImgMat2D, _ = cv2.projectPoints(secondMat3D, rMtxMat, tMtxMat, cam2MtxMat, distCam2Mat)
        secondSecImgMat2D, _ = cv2.projectPoints(secondMat3D, r0MtxMat, t0MtxMat, cam1MtxMat, distCam1Mat)
        
        # Рассчитываем триангуляцию точек (3D координату)
        triangPointsHomoMat1 = cv2.triangulatePoints(rt0MtxMat, rtMtxMat, firstSecImgMat2D, firstFirstImgMat2D)
        triangPointsHomoMat2 = cv2.triangulatePoints(rt0MtxMat, rtMtxMat, secondSecImgMat2D, secondFirstImgMat2D)
        
        # Переводим точки из однородных координат в обычные
        triangPointsMat1 = cv2.convertPointsFromHomogeneous(triangPointsHomoMat1.T)
        triangPointsMat2 = cv2.convertPointsFromHomogeneous(triangPointsHomoMat2.T)
        
        L0 = np.sqrt(a * a + b * b + c * c)
        Dp = 0.02 * L0  # диаметр окружности
        Lp = 0.4 * L0  # Расстояние между сферами
        
    #    m = triangPointsMat1[0][0] - triangPointsMat2[0][0]
     #   l = triangPointsMat1[0][1] - triangPointsMat2[0][1]
     #   n = triangPointsMat1[0][2] - triangPointsMat2[0][2]
        
        LpCalib = np.sqrt(np.abs(triangPointsMat1[0,0,0] - triangPointsMat2[0,0,0]) ** 2 +
                   np.abs(triangPointsMat1[0,0,1] - triangPointsMat2[0,0,1]) ** 2 +
                   np.abs(triangPointsMat1[0,0,2] - triangPointsMat2[0,0,2]) ** 2)
        
        return np.abs(LpCalib - Lp)