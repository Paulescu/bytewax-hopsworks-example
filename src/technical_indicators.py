from typing import Dict, Tuple

import numpy as np
import pandas as pd

def get_bb_bands_talib(close_prices: np.array, window_size: int) -> Tuple[float, float, float]:
    """_summary_

    Args:
        close_prices (np.array): _description_

    Returns:
        Tuple[float, float, float]: _description_
    """
    from talib import stream

    upper_band, mid_band, lower_band = \
            stream.BBANDS(close_prices, timeperiod=window_size)
    return upper_band, mid_band, lower_band

def get_bb_bands_ta(close_prices: np.array, window_size: int) -> Tuple[float, float, float]:
    """_summary_

    Args:
        close_prices (np.array): _description_

    Returns:
        Tuple[float, float, float]: _description_
    """
    from ta.volatility import BollingerBands

    indicator_bb = BollingerBands(close=pd.Series(close_prices), window=window_size, window_dev=2)

    mid_band = indicator_bb.bollinger_mavg().values[-1]
    upper_band = indicator_bb.bollinger_hband().values[-1]
    lower_band = indicator_bb.bollinger_lband().values[-1]

    return upper_band, mid_band, lower_band


class BollingerBands:

    def __init__(self, window_size: int):

        self.last_n = np.empty(0, dtype=np.double)
        self.n = window_size * 2
        self.window_size = window_size

    def _push(self, value: float):
        
        self.last_n = np.insert(self.last_n, 0, value)
        try:
            self.last_n = np.delete(self.last_n, self.n)
        except IndexError:
            pass

    def compute(self, data: Dict):
        
        self._push(data['close'])

        # compute technical indicator
        close_prices = self.last_n[::-1]

        upper_band, mid_band, lower_band = get_bb_bands_ta(
            close_prices, window_size=self.window_size)

        output = {
            'upper_band': upper_band,
            'mid_band': mid_band,
            'lower_band': lower_band,
            **data
        }
        return self, output

if __name__ == '__main__':

    # Test inputs for debugging
    inputs = [
        {'time': 1678450252.412037, 'open': 1385.42, 'high': 1385.42, 'low': 1385.32, 'close': 1385.32, 'volume': 3.9128633300000004},
        {'time': 1678450255.154885, 'open': 1385.32, 'high': 1385.45, 'low': 1385.32, 'close': 1385.36, 'volume': 4.51889748},
        {'time': 1678450261.314386, 'open': 1385.32, 'high': 1385.49, 'low': 1385.32, 'close': 1385.49, 'volume': 0.64300852},
        {'time': 1678450265.527894, 'open': 1385.49, 'high': 1385.49, 'low': 1385.32, 'close': 1385.39, 'volume': 5.140847330000001},
        {'time': 1678450270.373147, 'open': 1385.21, 'high': 1385.23, 'low': 1385.19, 'close': 1385.19, 'volume': 1.43794472}
    ]

    bb = BollingerBands(3)
    outputs = []
    for i in inputs:
        _, out = bb.compute(i)
        print(f'{out=}')