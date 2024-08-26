import sys
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


logging.basicConfig(stream=sys.stdout,
                    format='[%(asctime)s]{%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    level=logging.INFO)


def stardard_scaler(data):
    """
    stardard_scaler
    Args:
        data (_type_): data to be standardized
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pd.DataFrame(data))
    logging.info("raw data: {}".format(data))
    logging.info("scaled data: {}".format(scaled_data))
    return scaled_data


if __name__ == 'main':
    mock_data = {
        'Feature1': [2, 4, 6, 8, 10],
        'Feature2': [1, 3, 5, 7, 9],
        'Feature3': [2, 4, 6, 8, 10]
    }
    stardard_scaler(mock_data)
