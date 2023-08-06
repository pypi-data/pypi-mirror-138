from numdifftools import Gradient
import numpy as np
import scipy.optimize as spo

def gradient(f, X0, delta = 0.01, visual=False):
    '''
    Minimization of multi-dimensional function

    This method takes a function f: Rn -> R, x = (x1,x2,...,xn) -> f(x) and an intial column vector X0. The algorithm calulate the funcion's gradient and then calculates the  𝛼k which represents the most optimized direction to complete in. Once it's calculated, the new coordinates Xk+1 (vector) are calculated. The program continue on and on, until || ∇ f(Xk)|| <  𝛿  and ||Xk - Xk-1|| <  𝛿.
    
    Parameters
    -------
    
    f : callable
        multi-dimensional function
    x0 : list
        intial point's coordinates (vector)
    delta : float
        small quantity to check convergence
    '''
    X0 = np.array([X0]).T
    x_list = [X0]
    X = X0
    z = 1
    while (np.linalg.norm(z) > delta or np.linalg.norm(X - X0) > delta):
        z = Gradient(f)(X0)
        phi = lambda alpha : f((X.T - alpha * z)[0])
        alphak = spo.minimize(phi, 0).x[0]
        X = (X0.T - alphak * z).T
        X0 = X
        x_list.append(X0)
    return X0 if not visual else x_list

def conjgradient(f,X0, visual=False):
    '''
    Minimization of multi-dimensional function
    
    Parameters
    -------
    
    f : callable
        multi-dimensional function
    x0 : list
        intial point's coordinates (vector)
    '''
    n = len(X0)
    X0 = np.array([X0]).T
    x_list = [X0]
    Q = Gradient(Gradient(f))(X0)
    d = np.array([-Gradient(f)(X0)]).T
    for i in range(n):
        dT = d.T
        alphak = (dT @ d)/(dT @ Q @ d)
        X = X0 + alphak * d
        grdX = Gradient(f)(X)
        B = ( grdX @ d) / (dT @ Q @ d)
        d = np.array([-grdX]).T + B*d
        X0 = X
        x_list.append(X0)
    return X if not visual else x_list

def newton(f, x0, delta = 0.01, visual=False):
    '''
    Minimization of multi-dimensional function
    
    Parameters
    -------
    
    f : callable
        multi-dimensional function
    x0 : list
        intial point's coordinates (vector)
    delta : float
        small quantity to check convergence
    '''
    X0 = np.array([x0]).T
    X = X0
    x_list = [X]
    d = -np.linalg.inv(Gradient(Gradient(f))(X0)) @ Gradient(f)(X0)
    while np.linalg.norm(d) > delta:
        grd1x, grd2x, = Gradient(f)(X), Gradient(Gradient(f))(X)
        _grd2x = np.linalg.inv(grd2x)
        phi = lambda alpha : f((X.T[0] - alpha * _grd2x @ grd1x))
        alphak = spo.minimize(phi, 0).x[0]
        X = (X0.T + 1 * d).T
        try:
            np.linalg.cholesky(grd2x)
        except:
            d = -np.linalg.inv(np.eye(len(grd2x)) + grd2x) @ grd1x
        else:
            d = -np.linalg.inv(grd2x) @ grd1x
            x0 = X
            x_list.append(X)
    return X if not visual else x_list

def _test(n, phi, eps, alpha):
    __phi = phi(alpha)
    dphi = Gradient(phi)(0)
    _phi = phi(0)
    return __phi <= _phi + eps * dphi if n == 1 else __phi > _phi + eps * dphi
def _armijo(phi, alpha0, eps = .01, mu = 2):
    if alpha0 == 0:
        alpha = .1
    else:
        alpha = alpha0
    if _test(1,phi, eps, alpha):
        while not(_test(2,phi,eps, mu*alpha)):
            alpha = mu * alpha
    else:
        while not(_test(1,phi, eps, alpha)):
            alpha = alpha / mu
    return alpha

def _DFP(H,alphak,d,grd0, grd1):
    y = grd1 - grd0 # y should be a column vector
    dT = d.T # d : column vector,dT : row vector
    A = (alphak * d @ dT) / (dT @ y) # shape(d,dT)
    B = (-H @ y @ (H @ y).T) / (y.T @ H @ y) # H @ y: column, shape(d,dT)
    return H + A + B

def quasinewton(f, X0, delta = .01, visual=False):
    '''
    Minimization of multi-dimensional function
    
    Parameters
    -------
    
    f : callable
        multi-dimensional function
    x0 : list
        intial point's coordinates (vector)
    delta : float
        small quantity to check convergence
    '''
    X0 = np.array([X0]).T
    global X
    X = X0
    x_list = [X0]
    grd1 = np.array([Gradient(f)(X0)]).T
    H = np.eye(len(X))
    while(np.linalg.norm(grd1) > delta):
        d = -H @ grd1
        phi = lambda alpha : f(X - alpha*grd1)
        alphak = _armijo(phi,1)
        X = X0 + alphak * d
        grd0 = grd1
        grd1 = np.array([Gradient(f)(X)]).T
        H = _DFP(H,alphak,d,grd0, grd1)
        X0 = X
        x_list.append(X0)
    return X0 if not visual else x_list