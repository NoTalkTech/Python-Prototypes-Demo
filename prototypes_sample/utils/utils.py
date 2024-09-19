import numpy as np
import pandas as pd


def js_divergence(p, q):
    p = np.array(p)
    q = np.array(q)
    m = (p + q) / 2
    js = 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q/m))
    return round(float(js), 6)


if __name__ == '__main__':
    print('JS divergence_1 -> {}'.format(js_divergence([0.23, 0.31, 0.46], [0.43, 0.37, 0.20])))
    print('JS divergence_2 -> {}'.format(js_divergence([0.23, 0.31, 0.46], [0.43, 0.21, 0.36])))
