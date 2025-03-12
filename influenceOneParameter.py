import numpy as np
import matplotlib.pyplot as plt

def calculate_influence(calc, i, devCx, devCy, devFx, devFy, left, right, step, variation):
    values = []
    sd_values = []

    for val in np.arange(left, right + step, step):
        if variation == "Cx":
            SD2 = calc.calc(i, 400, 400, 300, val, val, devCy, devCy, devFy, devFx, devFx, devFy)
        elif variation == "Cy":
            SD2 = calc.calc(i, 400, 400, 300, devCx, devCx, val, val, devFy, devFx, devFx, devFy)
        elif variation == "Fy":
            SD2 = calc.calc(i, 400, 400, 300, devCx, devCx, devCy, devCy, val, devFx, devFx, val)
        elif variation == "Fx":
            SD2 = calc.calc(i, 400, 400, 300, devCx, devCx, devCy, devCy, devFy, val, val, devFy)
        else:
            raise ValueError("Неподдерживаемое значение variation. Допустимые значения: Cx, Cy, Fx, Fy.")

        values.append(val)
        sd_values.append(SD2)

    return values, sd_values

def plot_influence(values, sd_values, variation, color):
    plt.scatter(values, sd_values, c=color, marker='o', alpha=0.5, label=variation)
    plt.title(f'Зависимость SD от {variation}')
    plt.xlabel(variation)
    plt.ylabel('SD')
    plt.grid(True)
    plt.legend()