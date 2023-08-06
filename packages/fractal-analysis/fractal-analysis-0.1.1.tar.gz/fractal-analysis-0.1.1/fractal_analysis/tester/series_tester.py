import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Union, List

from fractal_analysis.tester.critical_surface import CriticalSurfaceFBM, CriticalSurfaceMFBM
from fractal_analysis.tester.estimate_sigma import EstimateSigma


class SeriesTester:
    """
    series: series to test
    alpha: significance level (look at quantiles of order alpha/2 and 1 − alpha/2)
    """

    def __init__(self, x: Union[List, np.ndarray, pd.Series], alpha: float = 0.05):
        self.series = np.array(x)
        self.alpha = alpha

    def is_mbm(self, h: Union[List, np.ndarray, pd.Series], sig2: float = None):
        """
            Source paper: Balcerek, Michał, and Krzysztof Burnecki. (2020) Testing of Multifractional Brownian Motion.
                          Entropy 22, no. 12: 1403.
                          https://doi.org/10.3390/e22121403
            h: holder exponents
            sig2: sigma square, cannot be 0, if None, use auto-estimated sigma
        """
        h = np.array(h)
        cla = CriticalSurfaceMFBM(N=len(h),
                                  H=h.T.tolist(),
                                  alpha=self.alpha,
                                  k=1)
        stat = np.dot(self.series.T.dot(cla._matrix_A_k), self.series)
        if sig2 is None:
            clas = EstimateSigma(series=self.series, h_series=h)
            sig2 = clas.theta_hat_square
        if sig2 == 0:
            print(f"Bad estimated sigma square: {sig2}. Suggest to give sigma square and rerun.")
        ret = False
        quantile = cla.quantile(sig2=sig2)
        low = quantile[0]
        up = quantile[1]
        if low <= stat <= up:
            #             print("no rej", sig, quantile, stat)
            ret = True
        #             print("rej", sig, quantile, stat)
        return ret, sig2

    def is_fbm(self, h: Union[float, List, np.ndarray, pd.Series] = None, sig2: float = None):
        """
            Source paper: Michał Balcerek, Krzysztof Burnecki. (2020) Testing of fractional Brownian motion in a noisy environment.
                          Chaos, Solitons & Fractals, Volume 140, 110097.
                          https://doi.org/10.1016/j.chaos.2020.110097
            Note: this class implements Algorithm 1 of the paper.
                  can use an auto-estimated sigma.
            h: holder exponent; if None, try all from 0.1 to 1 with step 0.1; if list-like, try all in the list
            sig2: sigma square, if None, use auto-estimated sigma
        """
        if h is None:
            all_h = np.arange(0.1, 1.1, 0.1)
        elif isinstance(h, (float, int)):
            if h > 1 or h < 0:
                raise ValueError('h needs to be in [0,1].')
            all_h = [h]
        else:
            all_h = h
        for h in tqdm(all_h):
            cla = CriticalSurfaceFBM(N=len(self.series),
                                     H=h,
                                     alpha=self.alpha,
                                     k=1)
            stat = np.dot(self.series.T.dot(cla._matrix_A_k), self.series)
            if sig2 is None:
                clas = EstimateSigma(series=self.series, h_series=np.ones(len(self.series)) * h)
                sig2 = clas.theta_hat_square
            quantile = cla.quantile(sig2=sig2)
            low = quantile[0]
            up = quantile[1]
            if low <= stat <= up:
                # not reject
                return True, sig2, h
        return False, None, None
