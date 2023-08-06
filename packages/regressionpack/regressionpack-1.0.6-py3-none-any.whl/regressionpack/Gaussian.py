import numpy as np
from typing import Tuple
from .GenericCurveFit import GenericCurveFit
from nptyping import NDArray

class Gaussian(GenericCurveFit):
    
    def FitFunc(self, x:NDArray, a:float, b:float, c:float, d:float) -> NDArray:
        """
        An exponantial function that goes like
        $$ y = a e^{-b*(x-c)^2} + d $$
        """
        return a * np.exp(-b * (x-c)**2) + d

    def Jacobian(self, x:NDArray, a:float, b:float, c:float, d:float) -> NDArray:
        """
        The jacobian of the exponential fit function. 
        Meant to return a matrix of shape [x.shape[0], 3], where
        every column contains the derivative of the function with 
        respect to the fit parameters in order. 
        """
        out = np.zeros((x.shape[0],4))
        out[:,0] = np.exp(-b * (x-c)**2)    # df/da
        out[:,1] = -a*(x-c)**2 * out[:,0]   # df/db
        out[:,2] = 2*a*b*(x-c) * out[:,0]   # df/dc
        out[:,3] = 1                        # df/dd

        return out

    def __init__(self, x:NDArray, y:NDArray, p0:NDArray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        super(Gaussian, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )