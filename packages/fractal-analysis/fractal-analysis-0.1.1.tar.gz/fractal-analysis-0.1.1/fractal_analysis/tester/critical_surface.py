import math
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Union, List

import numpy as np
from numpy import linalg
from scipy.linalg import sqrtm


class CriticalSurfaceBrownianMotion(ABC):
    def __init__(self,
                 N: int,
                 H: Union[List[float], float],
                 alpha: float,
                 k: int,
                 trials: int = 100000):
        self.N = N
        self.H = H
        self.alpha = alpha
        self.k = k
        self.trials = trials
        np.random.seed(6)
        self.chi2 = np.random.chisquare(df=1, size=(self.N, self.trials))

    @property
    def _matrix_A_k(self):
        A_k = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                if abs(i - j) == self.k:
                    A_k[i, j] = 0.5 / (self.N - self.k)
                # elif i == j:
                #     A_k[i, j] = 1 / self.N
        return A_k

    @abstractmethod
    def _autocovariance_matrix(self, sig2):
        pass

    def _eigenvalues(self, sig2):
        Sigma = self._autocovariance_matrix(sig2=sig2)
        square_root_Sigma = sqrtm(Sigma)
        A_k = self._matrix_A_k
        mat = square_root_Sigma.dot(A_k)
        mat = mat.dot(square_root_Sigma)
        eigenvalues, _ = linalg.eig(mat)
        return eigenvalues

    def _generalized_chi2(self, sig2):
        eigenvalues = self._eigenvalues(sig2=sig2)
        stat = np.array(eigenvalues.dot(self.chi2))
        return stat

    def quantile(self, sig2):
        dist = self._generalized_chi2(sig2=sig2)
        quantile = [0, 0]
        quantile[0] = np.percentile(a=dist, q=100 * self.alpha / 2)
        quantile[1] = np.percentile(a=dist, q=100 - 100 * self.alpha / 2)
        return quantile


class CriticalSurfaceFBM(CriticalSurfaceBrownianMotion):

    def _r_k(self, k):
        twoH = 2 * self.H
        return 0.5 * ((k + 1) ** twoH + abs(k - 1) ** twoH - 2 * k ** twoH)

    def _r_M_k(self, k, sig2):
        r_k = self._r_k(k=k)
        if k == 0:
            r_M_k = r_k + 2 * sig2
        elif k == 1:
            r_M_k = r_k - sig2
        else:
            r_M_k = r_k
        return r_M_k

    def _autocovariance_matrix(self, sig2):
        Sigma = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                k = abs(i - j)
                Sigma[i, j] = self._r_M_k(k=k, sig2=sig2)
        return Sigma


class CriticalSurfaceMFBM(CriticalSurfaceBrownianMotion):
    @lru_cache(maxsize=128)
    def _D(self, alpha):
        gam_ = math.gamma(alpha + 1)
        sin_ = math.sin(math.pi * alpha / 2)
        return math.pi / gam_ / sin_

    def _autocovariance_matrix(self, sig2):
        Sigma = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                D = self._D(alpha=self.H[i] + self.H[j])
                h = self.H[i] + self.H[j]
                Sigma[i, j] = sig2 * D * ((i + 1) ** h + (j + 1) ** h - abs(i - j) ** h)
        return Sigma

