import numpy as np


def labels_to_colors_crown(labels: np.array)->np.array:
    r = [0.8, 0.0, 0.0]
    r2 = [0.6, 0.0, 0.2]
    g = [0.0, 0.8, 0.0]
    g2 = [0.4, 0.6, 0.0]
    b = [0.0, 0.0, 0.8]
    b2 = [0.0, 0.4, 0.6]
    o = [0.9, 0.9, 0.9]
    rgbs = [r, g, b, r, g, r, g, b,
            b2, g2, r2, g2, r2, b2, g2, r2]
    #  o,o,o,o,o,o,o,o]

    rgbs.insert(0, [0.7, 0.7, 0.7])  # 0
    rgbs.insert(0, [0.2, 0.2, 0.2])  # -1
    rgbs = np.array(rgbs)
    return rgbs[labels+1]  # -1 0 ... 所以要 +1
