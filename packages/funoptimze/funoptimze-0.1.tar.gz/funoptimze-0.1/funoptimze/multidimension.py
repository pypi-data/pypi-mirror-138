from numdifftools import Gradient
import numpy as np
import scipy.optimize as spo
import imageio
import os
import matplotlib.pyplot as plt

def conGradientMethod(f,X0, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using con gradient method

    f : callable
        multi-dimensional function
    x0 : list
        intial point's coordinates (vector)
    '''
    n = len(X0)
    X0 = np.array([X0]).T
    Xlist = [X0]
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
        Xlist.append(X0)
    if v and n <= 2:
        animate(f,Xlist,axis)
    return Xlist



def gradientMethod(f, X0, delta = 0.01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using gradient method

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
    if v and len(X0) <= 2:
        animate(f,x_list,axis)
    return X0
    

def newton(f, x0, delta = 0.01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using newton method
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
    if v and len(X0) <= 2:
        animate(f,x_list,axis)
    return X 
    
def test(n, phi, eps, alpha):
    __phi = phi(alpha)
    dphi = Gradient(phi)(0)
    _phi = phi(0)
    return __phi <= _phi + eps * dphi if n == 1 else __phi > _phi + eps * dphi

def armijo(phi, alpha0, eps = .01, mu = 2):
    if alpha0 == 0:
        alpha = .1
    else:
        alpha = alpha0
    if test(1,phi, eps, alpha):
        while not(test(2,phi,eps, mu*alpha)):
            alpha = mu * alpha
    else:
        while not(test(1,phi, eps, alpha)):
            alpha = alpha / mu
    return alpha

def DFP(H,alphak,d,grd0, grd1):
    y = grd1 - grd0 # y should be a column vector
    dT = d.T # d : column vector,dT : row vector
    A = (alphak * d @ dT) / (dT @ y) # shape(d,dT)
    B = (-H @ y @ (H @ y).T) / (y.T @ H @ y) # H @ y: column, shape(d,dT)
    return H + A + B

def quasiNewton(f, X0, delta = .01, v = False, axis = None):
    '''
    This function finds the minimum of a function (f) using quasi newton
    
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
        alphak = armijo(phi,1)
        X = X0 + alphak * d
        grd0 = grd1
        grd1 = np.array([Gradient(f)(X)]).T
        H = DFP(H,alphak,d,grd0, grd1)
        X0 = X
        x_list.append(X0)
    if v and len(X0) <= 2:
        animate(f,x_list,axis)
    return X0

def animate(f,Xlist,axis):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    a = axis[0]
    b = axis[1]
    X = np.arange(a, b, 0.05)
    X, Y = np.meshgrid(X, X)
    Z = f([X, Y])
    surf = ax.plot_surface(X, Y, Z, linewidth=0, antialiased=True,cmap= 'plasma', alpha=0.4)
    filenames = []
    for i in range(len(Xlist)):
        if i == len(Xlist)-1:
            x, y = Xlist[-1][0][0],Xlist[-1][1][0]
            ax.scatter([x], [y], [f([ x, y ])],color="red",s=25, label="Minimum")
            plt.legend()
        else:
            x, y = Xlist[i][0][0],Xlist[i][1][0]
            ax.scatter([x], [y], [f([ x, y ])],color="blue",s=20)
        filename = f'{i}.png'
        filenames.append(filename)
        plt.savefig(filename)
    with imageio.get_writer('3d_conjgradient.gif', mode='I', duration = 0.5 ) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    for filename in set(filenames):
        os.remove(filename)
    plt.close()
    filenames = []
    for i in range(len(Xlist)):
        plt.contour(X, Y, Z, 10, cmap="winter")
        if i == len(Xlist)-1:
            x, y = Xlist[-1][0][0],Xlist[-1][1][0]
            plt.plot(x,y, "o", color="red", label = "Minimum")
        else:
            x, y = Xlist[i][0][0],Xlist[i][1][0]
            plt.plot(x,y, "o", color="green")
        filename = f'{i}.png'
        filenames.append(filename)
        plt.savefig(filename)
    with imageio.get_writer('2dProj_conjgradient.gif', mode='I', duration = 0.5 ) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    for filename in set(filenames):
        os.remove(filename)