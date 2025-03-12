import numpy as np
import matplotlib.pyplot as plt
from sol import Sol

def calculate_and_plot_sd(calc):
    # Фиксированные значения параметров
    fixed_Cx = 0  # Фиксированное значение Cx
    fixed_Cy = 0  # Фиксированное значение Cy
    fixed_Fx = 1  # Фиксированное значение Fx
    fixed_Fy = 1  # Фиксированное значение Fy

    # Диапазоны для изменения параметров
    range_Cx = np.arange(-100, 101, 1)  # Для Cx
    range_Cy = np.arange(-100, 101, 1)  # Для Cy
    range_Fx = np.arange(0.85, 1.15, 0.01)  # Для Fx
    range_Fy = np.arange(0.85, 1.15, 0.01)  # Для Fy

    # Массивы для хранения значений SD
    all_sd_values = []
    labels = []

    # Варианты фиксации двух параметров и изменения двух других
    scenarios = [
        {"fixed": {"Cx": fixed_Cx, "Cy": fixed_Cy}, "vary": ["Fx", "Fy"], "label": "Фиксированные Cx, Cy"},
        {"fixed": {"Cx": fixed_Cx, "Fx": fixed_Fx}, "vary": ["Cy", "Fy"], "label": "Фиксированные Cx, Fx"},
        {"fixed": {"Cx": fixed_Cx, "Fy": fixed_Fy}, "vary": ["Cy", "Fx"], "label": "Фиксированные Cx, Fy"},
        {"fixed": {"Cy": fixed_Cy, "Fx": fixed_Fx}, "vary": ["Cx", "Fy"], "label": "Фиксированные Cy, Fx"},
        {"fixed": {"Cy": fixed_Cy, "Fy": fixed_Fy}, "vary": ["Cx", "Fx"], "label": "Фиксированные Cy, Fy"},
        {"fixed": {"Fx": fixed_Fx, "Fy": fixed_Fy}, "vary": ["Cx", "Cy"], "label": "Фиксированные Fx, Fy"},
    ]

    # Вычисление SD для каждого сценария
    for scenario in scenarios:
        fixed_params = scenario["fixed"]
        vary_params = scenario["vary"]
        label = scenario["label"]

        # Определяем диапазоны для изменяемых параметров
        if "Cx" in vary_params:
            range_var1 = range_Cx
        elif "Cy" in vary_params:
            range_var1 = range_Cy
        elif "Fx" in vary_params:
            range_var1 = range_Fx
        elif "Fy" in vary_params:
            range_var1 = range_Fy

        if "Cx" in vary_params and "Cy" in vary_params:
            range_var2 = range_Cy
        elif "Cx" in vary_params and "Fx" in vary_params:
            range_var2 = range_Fx
        elif "Cx" in vary_params and "Fy" in vary_params:
            range_var2 = range_Fy
        elif "Cy" in vary_params and "Fx" in vary_params:
            range_var2 = range_Fx
        elif "Cy" in vary_params and "Fy" in vary_params:
            range_var2 = range_Fy
        elif "Fx" in vary_params and "Fy" in vary_params:
            range_var2 = range_Fy

        # Вычисление SD для всех комбинаций изменяемых параметров
        sd_values = []
        for var1 in range_var1:
            for var2 in range_var2:
                # Формируем параметры для вызова calc.calc
                params = {
                    "Cx": fixed_params.get("Cx", var1 if "Cx" in vary_params else fixed_Cx),
                    "Cy": fixed_params.get("Cy", var1 if "Cy" in vary_params else fixed_Cy),
                    "Fx": fixed_params.get("Fx", var2 if "Fx" in vary_params else fixed_Fx),
                    "Fy": fixed_params.get("Fy", var2 if "Fy" in vary_params else fixed_Fy),
                }
                SD = calc.calc(1, 400, 400, 300, params["Cx"], params["Cx"], params["Cy"], params["Cy"], params["Fy"], params["Fx"], params["Fx"], params["Fy"])
                sd_values.append(SD)

        # Сохраняем результаты
        all_sd_values.append(sd_values)
        labels.append(label)

    # Построение графика
    plt.figure(figsize=(10, 6))
    for sd_values, label in zip(all_sd_values, labels):
        plt.plot(sd_values, label=label, alpha=0.7)

    plt.title('Зависимость SD от различных комбинаций параметров')
    plt.xlabel('Итерации')
    plt.ylabel('SD')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()