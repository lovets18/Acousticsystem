import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import scipy.io as sio
from scipy.interpolate import interp1d

def my_trend(x,k):
    trend = np.zeros(len(x))
    for i in range(1 + k, len(x) - k):
        trend[i] = np.mean(x[i-k:i+k]);
    trend[1:]       = np.mean(x[1:]);
    trend[-k:] = np.mean(x[-k:])
    return trend

def my_detrend_mean(x,k):
    return x - my_trend(x,k)

def move_x_by_n(x,n):
    n = int(n)
    if n > 0:
        x[n+1:] = x[1:-n]
        x[1:n] = 0
    elif n < 0:
        x[1:n] = x[1-n:]
        x[n+1:] = 0
    return x


def plot_diagram(data, K):
    K = int(K)
    amp = np.zeros(2 * K + 1)
    for i in range(1, 2 * K + 1):
        Y = data
        for j in range(1, 8):
            Y[:, j] = move_x_by_n(Y[:, j], (K + 1 - i) * (j - 5));

        mat = np.zeros((8, 8))
        for ii in range(1, 8):
            for jj in range(ii, 8):
                mat[ii, jj] = np.mean(Y[:, ii].T * Y[:, jj])
        amp[i] = sum(sum(mat))
    return amp


def get_polar_data(file):
    # pi = 3.1415
    c = 340                  # скорость звука
    dl = 8.5e-2               # расстояние между микрофонами
    Fs = 20000                # частота дискретизации
    T = 1 / Fs               # период дискретизации
    del_cos = T * c / dl           # шаг по косинусу
    K = np.floor(1 / del_cos)   # количество отступов угла от 90 градусов
    cosines = np.array(range(int(K), -int(K+1), -1)) * del_cos  # вектор косинусов от 1 до -1

    phi = np.array(list(map(math.acos, cosines)))        # вектор углов в радианах от 0 до pi
    amp = np.zeros(len(phi))     # вектор амплитуд

    delta_phi = math.pi/2
    phi_q = np.linspace(math.pi/2 - delta_phi, math.pi/2 + delta_phi, 200) # вектор углов для интерполяции

    # phi_q = np.linspace(start * math.pi / 180., stop * math.pi / 180., 200)  # вектор углов для интерполяции

    dur     = 0.02                 # длительность 20 мс
    n = 3

    # file_name = r'C:\Users\Вова\Desktop\Работа\Решетки\new_file'
    data = sio.loadmat(file)
    data['DATA'].shape

    num_of_seconds = 3

    N, _ = data['DATA'].shape
    N = 2000

    t = np.arange(0, (N - 1), T) * T

    df = pd.DataFrame(columns=['phi', 'r', 'iter'])
    cur_iter = 1
    for strt_t in np.arange(0, num_of_seconds - dur, 5 * dur):
        #     print(strt_t)
        end_t = strt_t + 5 * dur
        strt_p = int(np.round(strt_t * Fs) + 1)
        end_p = int(np.round(end_t * Fs))
        #     print('phases start - end')
        #     print(strt_p)
        #     print(end_p)

        part_of_data = data['DATA'][strt_p:end_p]
        for i in range(1, 15):
            part_of_data[:, i] = my_detrend_mean(part_of_data[:, i], 10)

        part_of_t = t[strt_p:end_p]

        # diagram
        amp = plot_diagram(part_of_data, K)
        #     print(amp)
        amp_q = interp1d(phi, amp, kind='nearest')(phi_q)
        curr_df = pd.DataFrame({'phi': phi_q, 'r': amp_q, 'iter': cur_iter})
        df = pd.concat([df, curr_df])
        cur_iter += 1
        #     print(amp_q)
        # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        # ax.plot(phi_q, amp_q)
        # #     ax.set_rmax(2)
        # #     ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
        # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        # ax.grid(True)
        #
        # ax.set_title("A line plot on a polar axis", va='bottom')
        # plt.show()

    df.phi = df.phi * 180. / np.pi

    return df



