import random
from copy import deepcopy
from typing import TypedDict
import numpy as np
import matplotlib.pyplot as plt


class Particle(TypedDict):
    x1: float
    x2: float
    lbest_x1: float
    lbest_x2: float


# Инициализация частиц со случайными значениями в указанных пределах
def initialize_particles(bounds, n):
    return [
        Particle(
            x1=random.uniform(bounds[0], bounds[1]),
            x2=random.uniform(bounds[0], bounds[1]),
            lbest_x1=random.uniform(0, 1),
            lbest_x2=random.uniform(0, 1),
        )
        for _ in range(n)
    ]


# Вызов целевой функции
def func(fitness_func, x1, x2):
    return eval(fitness_func)


# Реализация алгоритма оптимизации на основе PSO
def algorithm(particles, generations, fitness_func):
    history = [
        deepcopy(sorted(particles, key=lambda x: func(fitness_func, x["x1"], x["x2"])))
    ]
    for _ in range(generations):
        gbest = (history[-1][0]["x1"], history[-1][0]["x2"])

        for particle in particles:
            f_was = func(fitness_func, particle["x1"], particle["x2"])

            # Случайное значение с распределением Гаусса
            particle["x1"] = np.random.normal(
                (gbest[0] + particle["lbest_x1"]) / 2,
                abs(gbest[0] - particle["lbest_x1"]),
            )
            particle["x2"] = np.random.normal(
                (gbest[1] + particle["lbest_x2"]) / 2,
                abs(gbest[1] - particle["lbest_x2"]),
            )

            f_now = func(fitness_func, particle["x1"], particle["x2"])

            if f_now < f_was:
                particle["lbest_x1"] = particle["x1"]
                particle["lbest_x2"] = particle["x2"]

        particles = sorted(
            particles, key=lambda x: func(fitness_func, x["x1"], x["x2"])
        )
        history.append(deepcopy(particles))

    return history


def plot_scatter(points, xlabel, ylabel, title, label):
    """
    Генерирует scatter-график для массива точек.

    Параметры:
    - points: Массив точек в формате list[tuple(float, float)].
    - xlabel: Подпись оси X (строка).
    - ylabel: Подпись оси Y (строка).
    - title: Название графика (строка).
    - label: Подпись для легенды (строка).

    Возвращает:
    - None (отображает график).
    """
    x, y = zip(*points)

    plt.plot(x, y, linestyle="-", label="Линия 1")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xlabel(xlabel, fontsize=8)
    plt.ylabel(ylabel, fontsize=8)
    plt.title(title, fontsize=8)
    plt.xscale("linear")
    plt.yscale("log")
    plt.text(x=0, y=0, s=label, fontsize=12, ha="center")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    data = []
    bounds = [0, 10]
    f = "(x1 - 2) ** 4 + (x1 - 2*x2) ** 2"

    for i in range(1, 100):
        generation = initialize_particles(bounds=bounds, n=i)
        bg = algorithm(deepcopy(generation), 50, f, bounds)[-1][0]
        data.append((i, func(f, bg["x1"], bg["x2"])))

    plot_scatter(
        data,
        "Количество частиц",
        "Значение целевой функции, меньше - лучше",
        "График зависимости точности работы алгоритма от количества частиц",
        "Начальные данные",
    )
