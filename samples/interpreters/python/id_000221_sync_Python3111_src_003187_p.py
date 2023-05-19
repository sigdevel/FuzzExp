from scipy import *
from weave import converters
from pylab import *

def norm(x):
    return sqrt(abs(sum(x * conjugate(x))))

def rotmat(a, b):
    
    if (b==0.0):
        c, s = 1.0, 0.0
    elif (abs(b) > abs(a)):
        
        temp = -a/b
        s = 1.0 / sqrt(1.0 + temp**2)
        c = temp * s
    else:
        
        temp = -b/a
        c = 1.0 / sqrt(1.0 + temp**2)
        s = temp * c
    return c, s

def myGmresPython( A, x, b, M, restrt, max_it, tol ):

    iter = 0                                         
    flag = 0

    bnrm2 = norm(b)
    if  ( bnrm2 == 0.0 ):
        bnrm2 = 1.0

    
    r = b - matrixmultiply(A, x)
    error = norm( r ) / bnrm2
    if ( error < tol ):
        return x, error, iter, flag

    n = A.shape[0]                                  
    m = restrt
    V = zeros((n,m+1), Complex)
    H = zeros((m+1, m), Complex)
    cs, sn = zeros(m, Complex), zeros(m, Complex)
    e1 = zeros(m+1, Complex)
    e1[0] = 1.0

    for iter in range(max_it):
        
        r = b - matrixmultiply(A, x)
        V[:, 0] = r / norm( r )
        
        s = norm( r )*e1
        
        for i in range(m):
            
            w = matrixmultiply(A, V[:, i])
            for k in range(i+1):
                H[k, i] = sum(w * conjugate(V[:, k]))
                w = w - H[k, i] * V[:, k]
            "sum(w) =", sum(w)
            H[i+1, i] = norm( w )
            V[:, i+1] = w / H[i+1, i]
            "sum(V[:, i+1]) =", sum(V[:, i+1])
            
            for k in range(i):
                
                
                temp = conjugate(cs[k]) * H[k, i] - conjugate(sn[k]) * H[k+1, i]
                H[k+1,i] = sn[k] * H[k, i] + cs[k] * H[k+1, i]
                H[k,i] = temp
            
            cs[i], sn[i] = rotmat( H[i, i], H[i+1, i] )
            
            H[i, i] = conjugate(cs[i])*H[i, i] - conjugate(sn[i])*H[i+1, i]
            H[i+1,i] = 0.0
            "sum(sum(H)) =", sum(sum(H))
            
            
            temp = conjugate(cs[i]) * s[i] - conjugate(sn[i]) * s[i+1]
            
            s[i+1] = sn[i] * s[i] + cs[i] * s[i+1]
            s[i] = temp;
            error = abs(s[i+1]) / bnrm2
            "error =", error
            
            if ( error <= tol ):
                y = linalg.solve( H[:i+1, :i+1], s[:i+1] )
                x = x + matrixmultiply(V[:, :i+1], y)
                return x, error, iter, flag

        if ( error <= tol ):
            return x, error, iter, flag
        y = linalg.solve( H[:m, :m], s[:m] )
        "sum(y) =", sum(y)
        x = x + matrixmultiply(V[:, :m], y)          
        "sum(x) =", sum(x)
        
        r = b - matrixmultiply(A, x)
        error = abs(s[i+1]) / bnrm2                      
        "error =", error
        if ( error <= tol ):
            return x, error, iter, flag

    if ( error > tol ):
        flag = 1
    return x, error, iter, flag


def myGmresC( A, x, b, M, restrt, max_it, tol ):
    error = zeros(1, Float)
    flag = zeros(1, Int)
    iter = zeros(1, Int)
    wrapping_code = """gmres(x, error(0), iter(0), flag(0), A, b, tol, restrt, max_it);"""

    weave.inline(wrapping_code,
                 ['x', 'error', 'iter', 'flag', 'A', 'b', 'tol', 'restrt', 'max_it'],
                 type_converters = converters.blitz,
                 include_dirs = ['./MoM/iterative/'],
                 library_dirs = ['./MoM/iterative/'],
                 libraries = ['ITERATIVE'],
                 headers = ['<iostream>','<complex>','"gmres.h"'],
                 compiler = 'gcc')
    return x, error[0], iter[0], flag[0]



if __name__=="__main__":
    ff = open('Z.txt', 'r')
    Z = pickle.load(ff)
    ff.close()
    ff = open('V.txt', 'r')
    V = pickle.load(ff)
    ff.close()

    N = V.shape[0]
    Y = zeros(N, Complex)
    X0 = zeros(N, Complex)
    M = ones((N,N),Complex64)
    restart = 3
    tol = 1.e-3
    maxiter = 50
    
    I = matrixmultiply(linalg.inv(Z),V)
    
    I2, error2, iteration2, info2 = myGmresPython( Z, X0, V, M, restart, maxiter, tol )
    print "error2, iteration2, info2 =", error2, iteration2, info2
    
    X0 = zeros(N, Complex)
    I3, error3, iteration3, info3 = myGmresC( Z, X0, V, M, restart, maxiter, tol )
    print "error3, iteration3, info3 =", error3, iteration3, info3

    print sum(I), sum(I2), sum(I3)



