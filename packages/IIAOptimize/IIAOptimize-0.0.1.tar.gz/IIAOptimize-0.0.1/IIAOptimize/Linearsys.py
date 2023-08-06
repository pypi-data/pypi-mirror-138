import numpy as np

def gaussjordanInv(A):
    '''
    Inverse a matrix using elimination Gauss Jordan method

    This method takes a matrix as parameter, then it returns the inverse of the given matrix. 
    
    Parameters
    -------
    
    A : matrix
        a numpy matrix (vector of vectors) of any dimension
    '''
    B = A.copy()
    n,m = len(B), len(B[0])
    I = np.eye(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                ratio = B[j,i]/B[i,i]
                for k in range(m):
                    B[j,k] = B[j,k] - ratio * B[i,k]
                    I[j,k] = I[j,k] - ratio * I[i,k]
    for i in range(len(B)):
        divisor = B[i,i]
        for j in range(len(B)):
            B[i,j] = B[i,j]/divisor
            I[i,j] = I[i,j]/divisor
    return I

def linearGauss(A,b):
    '''
    Solve a linear system

    This method takes a matrix and a vector as parameter, then it returns the vector solution of the given matrix using gauss jordan method. 
    
    Parameters
    -------
    
    A : matrix
        a numpy matrix (vector of vectors) of any dimension
    b : list
        a list or a numpy vector
    '''
    n=len(A)
    for i in range(n):
        for j in range(n):
            if i!=j:
                ratio =A[j,i]/A[i,i]
                for k in range(n):
                    A[j,k]=A[j,k]-ratio *A[i,k]
                b[j]=b[j]-ratio *b[i]
    x=b
    for i in range(n-1,-1,-1):
        x[i]=x[i]/A[i,i]
        A[i,i] /= A[i,i]
    return x

def _decompositionLU(A):
    n=len(A)
    L=np.identity(n)
    U=A
    for i in range(n):
        for j in range(n):
            s=0
            for k in range(i):
                s+=(L[i,k]*U[k,j])
            U[i,j]=A[i,j]-s
        for j in range(i,n):
            if i==j:
                L[i,i]=1
            else:
                s=0
                for k in range(i):
                    s+=(L[j,k]*U[k,i])
                L[j,i]=(A[j,i]-s)/U[i,i]
    return (L,U)

def _choleski(A):
    n=len(A)
    L=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1):
            s=0
            if j==i:
                for k in range(j):
                    s+=pow(L[j,k],2)
                L[j,j]=np.sqrt(A[j,j]-s)
            else:
                for k in range(j):
                    s+=L[i,k]*L[j,k]
                L[i,j]=(A[i,j]-s)/L[j,j]
    return L

def LUdecomp(A,b):
    '''
    Solve a linear system

    This method takes a matrix and a vector as parameter, then it returns the vector solution of the given matrix using Choleski
    Parameters
    -------
    
    A : matrix
        a numpy matrix (vector of vectors) of any dimension
    b : list
        a list or a numpy vector
    '''
    L, U = _decompositionLU(A)
    y = linearGauss(L,b)
    x = linearGauss(U,y)
    return x
def cholsekidecomp(A,b):
    A = _choleski(A)
    B = A.T
    y = linearGauss(A,b)
    x = linearGauss(B,y)
    return x