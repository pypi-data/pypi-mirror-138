import numpy as np
import matplotlib.pyplot as plt
from time import time
import imageio
import os
from math import sqrt

def fixedStepSize(f, x, step = 0.01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using the fixed step size search

    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    step : float
        the quantity used to determine the next point after each iteration
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    xStep = x + step
    X = [x]
    reverse = False
    f1, f2 = f(x), f(xStep)
    while(f2<=f1 or not reverse):
        if f2>f1 and (not reverse):
            step = -step
            reverse = True
        xStep += step
        X.append(xStep-step)
        f1, f2 = f2, f(xStep)
    if v:
        animate(f,X,axis)
    return xStep-step
def AcceleratedStepSize(f, x1, s = 0.001, v = False , axis = None):
    '''
    This function finds the minimum of a function (f) using the accelerated step size seach.

    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    step : float
        the quantity used to determine the next point after each iteration
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = []
    x2=x1+s
    f1,f2=f(x1),f(x2)
    i=1
    if f2<f1:
        while f2<f1:
            p=x2
            x2+=(2**i)*s
            f1,f2=f(p),f(x2)
            i+=1
            X.append(p)
    elif f1<f2:
        while f1<f2:
            p=x1
            x1-=(2**i)*s
            f1,f2=f(x1),f(p)
            i+=1
            X.append(p)
    if v:
        animate(f,X,axis)
    return p

def exhaustiveSearch(f, xs, xf, n = 100, v = False, axis = None):
    ''' 
    This function finds the minimum of a function (f) using exhaustive search.

    f : callable
        function we want to apply the method to, in order to get its minimum
    x : float
        intial point
    xf : float
        last point
    n : int
        number of subdivisions in the interval
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X =[]
    a = xs
    b = xf
    h=(b-a)/n
    x=a
    y=a+h
    f1,f2=f(x),f(y)
    if f2<f1:
        while y <= b and f2 <= f1:
            x+=h
            y+=h
            f1,f2=f(x),f(y)
            X.append(y)
            X.append(x)
        if v:
            animate(f,X,axis)
        return(x)
    elif f1<f2:
        if f(a) > f(b):
            X.append(b)
            if v:
                animate(f,X,axis)
            return(b)
        else:
            X.append(a)
            if v:
                animate(f,X,axis)
            return(a)
    else:
        X.append((x+y)/2)
        if v:
            animate((x+y)/2)
        return((x+y)/2)
    

def dichotomousSearch(f, xs, xf, delta = .001, epsilon = .01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using dichotomous seach

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
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    a = xs
    b = xf
    e = epsilon
    d = delta
    L=b-a
    x1,x2=(a+(L/2-d/2)),(b+(L/2+d/2))
    f1,f2=f(x1),f(x2)
    X = []
    while L>e:
        if f1<f2:
            b=x1
            L=b-a
            x1,x2=(a+(L/2-d/2)),(a+(L/2+d/2))
            f1,f2=f(x1),f(x2)
            X.append(x1)
            X.append(x2)
        else:
            a=x2
            L=b-a
            x1,x2=(a+(L/2-d/2)),(a+(L/2+d/2))
            f1,f2=f(x1),f(x2)
            X.append(x1)
            X.append(x2)
    if f1<f2:
        if v:
            animate(f,X,axis)
        return(x1)
    else:
        if v:
            animate(f,X,axis)
        return(x2)

def intervalHalving(f,xs,xf, eps = 0.01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using interval halving search

    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    eps : float
        minimun length of the interval [xs,xf]
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    a = xs
    b = xf
    e = eps
    X = []
    L=b-a
    x,x1,x2=(a+L/2),(a+L/4),(a+3*L/4)
    f0,f1,f2=f(x),f(x1),f(x2)
    while L>e:
        if f1<f0 and f0<f2:
            b=x
            x=x1
            L=b-a
            x1,x2=(a+L/4),(a+3*L/4)
            f0,f1,f2=f(x),f(x1),f(x2)
            X.append(x)
            X.append(x1)
            X.append(x2)
        elif f2<f0 and f0<f1:
            a=x
            x=x2
            L=b-a
            x1,x2=(a+L/4),(a+3*L/4)
            f0,f1,f2=f(x),f(x1),f(x2)
            X.append(x)
            X.append(x1)
            X.append(x2)
        else:
            a,b=x1,x2
            L=b-a
            x1,x2=(a+L/4),(a+3*L/4)
            f0,f1,f2=f(x),f(x1),f(x2)
            X.append(x)
            X.append(x1)
            X.append(x2)
    if v:
        animate(f,X,axis)
    return(x)

def _fibonacci(n):
    fib0, fib1 = 1,1
    for i in range(2,n+1):
        fib = fib0 + fib1
        fib0 = fib1
        fib1 = fib
    return fib1
def fibonacciSearch(f, xs, xf, n = 10, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using the fibonacci search

    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    n : int
        number of fibonacci terms
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = []
    while n > 1:
        L = _fibonacci(n-2)*(xf - xs)/_fibonacci(n)
        x1, x2 = xs + L, xf - L
        if f(x1) < f(x2):
            xf = x2
            X.append(xf)
        else:
            xs = x1
            X.append(xs)
        n-=1
    if v:
        animate(f,X,axis)
    return xs

def goldenSection(f, xs, xf, eps= .1, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using golden section search

    f : callable
        function we want to apply the method to, in order to get its minimum
    xs : float
        intial point
    xf : float
        last point
    eps : float
        minimum length of interval [xf;xs]
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = []
    a = xs
    b = xf
    e = eps
    L=b-a
    g=(1+sqrt(5))/2
    x1,x2=a+((b-a)/(1+g)),b-((b-a)/(1+g))
    f1,f2=f(x1),f(x2)
    while L>e:
        if f2>f1:
            b=x2
            L=b-a
            x1,x2=a+((b-a)/(1+g)),b-((b-a)/(1+g))
            f1,f2=f(x1),f(x2)
            m=x1
            X.append(m)
        elif f2<f1:
            a=x1
            L=b-a
            x1,x2=a+((b-a)/(1+g)),b-((b-a)/(1+g))
            f1,f2=f(x1),f(x2)
            m=x2
            X.append(m)
        else:
            m=(x2+x1)/2
            X.append(m)
    if v:
        animate(f,X,axis)
    return m

def newtonMethod(f, df, ddf, xs, eps = 0.01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using newton search

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
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = [xs]
    x = xs
    while abs(df(x)) > eps:
        x0 = x
        x = x0 - df(x0)/ddf(x0)
        X.append(x)
    if v:
        animate(f,X,axis)
    return x

def quasiNewtonMethod(f, xs, delta = .01, eps = .01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using quasi-newton search

    f : callable
        function to find its minimum/maximum
    xs : float
        starting point of the process
    delta : float
        small step size to calculate df and ddf
    eps : float
        a small quantity to check convergence ( |f'(λ)| < eps)
    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = [xs]
    dfx = 1
    x = xs
    while abs(dfx) > eps:
        x0 = x
        x = x0-(delta*(f(x0+delta)-f(x0-delta)))/(2*(f(x0+delta)-2*f(x0) + f(x0-delta)))
        X.append(x)
        dfx = (f(x+delta) - f(x-delta))/(2*delta)
    if v:
        animate(f,X,axis)
    return x

def secantMethod(f,df, A, t1 = .1, eps = .01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using secant seach

    df : callable
        first derivative of the function to test
    A : float
        starting point of the process
    t1 : float
        small step size
    eps : a small quantity to check convergence ( |f'(λ)| < eps )

    v : bool
        if true then the function will create a gif of the progress
    axis : List of length 2 
        the interval that will be ploted
    '''
    X = []
    while abs(df(A)) > eps:
        if df(t1) < 0:
            A = t1
            t1 *= 2
        else:
            B = t1
            A = A - df(A)/((df(B)-df(A))/(B-A))
            X.append(A)
    if v:
        animate(f,X,axis)
    return A

def animate(f,X,axis):
    L = np.linspace(axis[0], axis[1], 1000)
    F = f(L)
    plt.plot(L,F)
    _x = X[-1]
    _f = f(X[-1])
    plt.plot(_x, _f,"o",  color="r", label="optimum point")
    etiquita = "{:.2f}".format(_x)
    plt.annotate(etiquita, (_x,_f+0.03), ha="center")
    plt.legend()
    filenames = []
    for i in range(0,len(X) - 1) :
        pt1 = [X[i],X[i+1]]
        pt2 = [f(X[i]),f(X[i+1])]
        plt.plot(X[i],f(X[i]),"o",color = "g")
        plt.plot(pt1,pt2,color = "g")
        filename = f'{i}.png'
        filenames.append(filename)
        plt.savefig(filename)
    with imageio.get_writer('mygif.gif', mode='I', duration = 0.5 ) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    for filename in set(filenames):
        os.remove(filename)
    
