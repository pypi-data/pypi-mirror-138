import numpy as np


def fixedstepsize(f, x, step = 0.001, visual = False):
    '''
    Minimization of unimodal function

    This method requires a random initial point and a step, it consists of comparing f1 = f(xs) and f2 = f(xstep) = xs + step, based on the unimodality of the function, if f1 > f2, we pass to the other iteration with xs = xstep and xstep += step, until f1 < f2. But, if f2 > f1, the iteration continues as previous, but step = -step, until f2 < f1.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    step : float
        the quantity used to determine the next point after each iteration
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''
    xStep = x + step
    x_list = [x]
    reverse = False
    f1, f2 = f(x), f(xStep)
    while(f2<=f1 or not reverse):
        if f2>f1 and (not reverse):
            step = -step
            reverse = True
        xStep += step
        x_list.append(xStep-step)
        f1, f2 = f2, f(xStep)
    return xStep-step if not visual else x_list

def accstepsize(f, x, step = 0.001, visual = False):
    '''
    Minimization of unimodal function
    
    This method requires a random initial point and a step, it consists of comparing f1 = f(xs) and f2 = f(xstep) = xs + step, based on the unimodality of the function, if f1 > f2, we pass to the other iteration with xs = xstep and xstep += 2*step, until f1 < f2. But, if f2 > f1, the iteration continues as previous, but step = -step/2, until f2 < f1.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    step : float
        the quantity used to determine the next point after each iteration
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''
    xStep = x + step
    x_list = [x]
    reverse = False
    f1, f2 = f(x), f(xStep)
    _step = step
    while(f2<=f1 or not reverse) and abs(step) >= _step:
        if f2>f1 and (not reverse):
            step = -step
            reverse = True
        step = step /2 if reverse else step * 2
        xStep += step
        x_list.append(xStep-step)
        f1, f2 = f2, f(xStep)
    return xStep-step if not visual else x_list

def exhaustive(f, xs, xf, n = 1000, visual = False):
    '''
    Minimization of unimodal function

    This method requires the initial and the last point of the interval to be known (xs, xf), it consists of dividing the interval into n even parts. Based on the unimodality of the function, once f(xk)< f(xk+1) the minimun resides between xk and xk+1.
    
    Parameters,
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    xf : float
        last point
    n : int
        number of subdivisions in the interval
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''
    L = np.linspace(xs, xf, n)
    Lf = f(L)
    index = 0
    for i in range(1,n-1):
        if Lf[i] < Lf[i+1]:
            return L[i] if not visual else L[:i]

def dichotomous(f, xs, xf, delta = .001, epsilon = .01, visual = False):
    '''
    Minimization of unimodal function

    This method requires the initial and the final point of the interval to be known (xs, xf), it consists of testing two close points (separated by a small quantity delta), after that it compares both images in order to minimize the concerned interval by almost half. The process continues replacing xs with x1 if f(x1)> f(x2) and xf with x2 if f(x1)< f(x2), and then changing values of x1 and x2 to the half of the new interval.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    xf : float
        last point
    delta : float
        small positive number chosen such that the two xs and xf give significantly different results.
    eps : float
        minimun value between two consecutive points
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''
    x_list = []
    while xf-xs > epsilon:
        x1 = (xs + (xf-xs)/2) - delta/2
        x2 = (xs + (xf-xs)/2) + delta/2
        x_list.append((xs, xf))
        if f(x1) > f(x2):
            xs = x1
        else :
            xf = x2
    return (xs+xf)/2 if not visual else x_list

def intervalhalving(f,xs,xf, eps = 0.01, visual=False):
    '''
    Minimization of unimodal function

    It consists of comparing f (x1 =  (𝑥𝑠+𝐿0)/4 ), f (x0 =  (𝑥𝑠+𝐿0)/2 ) and f (x2 =  (𝑥𝑓−𝐿0)/4 ), and then it changes xs and xf, based on this test.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    eps : float
        minimun length of the interval [xs,xf]
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''

    x_list = [(xs,(xs+xf)/2, xf)]
    L0 = xf-xs
    while L0>eps:
        x1, x0, x2 = xs + L0 /4, xs+L0/2, xf-L0/4
        x_list.append((x1,x0,x2))
        f1, f0, f2 = f(x1), f(x0), f(x2)
        if f1 < f0 < f2:
            x0, xf = x1, x0
        if f1 > f0 > f2:
            xs, x0 = x0, x2
        if f1 > f0 and f2 > f0:
            xs, xf = x1, x2
        L0 = xf-xs
    return x0 if not visual else x_list

def _fibonacci(n):
    fib0, fib1 = 1,1
    for i in range(2,n+1):
        fib = fib0 + fib1
        fib0 = fib1
        fib1 = fib
    return fib1
def fibonacci(f, xs, xf, n = 10, visual=False):
    '''
    Minimization of unimodal function

    This method uses the fibonacci sequence to divide the interval (which has to be known, xs and xf), it takes n as an argument (to calculate Fibn), so that the returned value would be within an interval of length  (𝑥𝑓−𝑥𝑠)/𝐹𝑖𝑏𝑛 . Basically, for each iteration  (1≤𝑖≤𝑛)  it takes two point x1 and x2 (x1 = xs + L and x2 = xf - L) (with L = Fibn-2*((𝑥𝑓−𝑥𝑠)/𝐹𝑖𝑏𝑛)  ) then it tests their images, and eliminate a part of the interval, which is [x2, xf] if f(x1) < f(x2) and [xs,x1] if not.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    n : int
        number of fibonacci terms
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''

    x_list = []
    while n > 1:
        L = _fibonacci(n-2)*(xf - xs)/_fibonacci(n)
        x1, x2 = xs + L, xf - L
        if f(x1) < f(x2):
            xf = x2
        else:
            xs = x1
        x_list.append((xs,xf))
        n-=1
    return xs if not visual else x_list

def goldensection(f, xs, xf, eps= .001, visual=False):
    '''
    Minimization of unimodal function

    This method is totally inspired by the fibonacci method (check onedimension.fibonnaciSearch), but instead of calculating  𝐹𝑖𝑏(𝑛−2)/𝐹𝑖𝑏𝑛  for each iteration, it fixes a ratio  𝛾  = 1.618.
    
    Parameters
    -------
    
    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    eps : float
        minimum length of interval [xf;xs]
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''

    x_list = [(xs,xf)]
    gamma = 1.618
    L0 = xf - xs
    while L0 > eps:
        x1,x2 = xs + L0/(1+gamma), xf - L0/(1+gamma)
        f1,f2 = f(x1), f(x2)
        if f2 > f1:
            xf = x2
        else:
            xs = x1
        x_list.append((xs,xf))
        L0 = xf - xs
    return (xs+xf)/2 if not visual else x_list

def newton(f, df, ddf, xs, eps = 0.01, visual=False):
    '''
    Minimization of unimodal function

    This method takes a function, its derivatives and a random initial point as arguments( f, df, ddf and xs), it consists of determines the tangent of the function at xs, and then takes the intersection point between the tangent and the abscess axe. The process is repeated until the image of the tested point by the first derivative is almost equal to zero (|df(x)| < eps).

    Parameters
    -------
    
    f : callable
        function to find its minimum/maximum
    df : callable
        first derivative of f
    ddf : callable
        second derivative of f
    xs : float
        starting point of the process
    eps : float
        a small quantity to check convergence ( |f'(λ)| < eps)
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''

    x_list = [xs]
    x = xs
    while abs(df(x)) > eps:
        x0 = x
        x = x0 - df(x0)/ddf(x0)
        x_list.append(x)
    return x if not visual else x_list

def quasinewton(f, xs, delta = .01, eps = .01, visual=False):
    '''
    Minimization of unimodal function

    This method takes a function and a random initial point ( f, xs), it consists of determines the tangent of the function at xs, and then takes the intersection point between the tangent and the abscess axe. The process is repeated until the image of the tested point by the first derivative is almost equal to zero (|df(x)| < eps). The derivatives are calculated approximately.
    
    Parameters
    -------
    
    f : callable
        function to find its minimum/maximum
    xs : float
        starting point of the process
    delta : float
        small step size to calculate df and ddf
    eps : float
        a small quantity to check convergence ( |f'(λ)| < eps)
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses
    '''

    x_list = [xs]
    dfx = 1
    x = xs
    while abs(dfx) > eps:
        x0 = x
        x = x0-(delta*(f(x0+delta)-f(x0-delta)))/(2*(f(x0+delta)-2*f(x0) + f(x0-delta)))
        x_list.append(x)
        dfx = (f(x+delta) - f(x-delta))/(2*delta)
    return x if not visual else x_list

def secant(df, A, t1 = .1, eps = .01, visual=False):
    '''
    Minimization of unimodal function

    This method works with two points, draw a line between them and then acquire its intersection with the abscisse axe. it tests (df(t1)| < 0), if the test is true, it multiplies t1 by 2 until the test is uncorrect, which then leads to create the second point B (B = t1) and affects a new value to A (A = A - (𝑑𝑓(𝐴)(𝐵−𝐴))/(𝑑𝑓(𝐵)−𝑑𝑓(𝐴)) ) the loop then goes on and on until the convergence test is satisfied (|df(A)| < eps).
    
    Parameters
    -------
    
    df : callable
        first derivative of the function to test
    A : float
        starting point of the process
    t1 : float
        small step size
    eps : a small quantity to check convergence ( |f'(λ)| < eps )
    visual : boolean
        if the value is False, the function will only returns the optimum. But, if the value is True the function will return a list of tested abscisses, visual=False
    '''
    x_list = []
    while abs(df(A)) > eps:
        if df(t1) < 0:
            A = t1
            t1 *= 2
        else:
            B = t1
            A = A - df(A)/((df(B)-df(A))/(B-A))
            x_list.append(A)
    return A if not visual else x_list