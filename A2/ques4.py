import numpy as np
np.set_printoptions(legacy='1.21')
def find_eigenvector(matrix, eigenvalue):
    n = matrix.shape[0]
    identity_matrix = np.eye(n)
    A_minus_lambda_I = matrix - eigenvalue * identity_matrix
    
    U, S, Vt = np.linalg.svd(A_minus_lambda_I)
    smallest_singular_value_index = np.argmin(S)
    eigenvector = Vt[smallest_singular_value_index]
    norm = sum(eigenvector)
    eigenvector=eigenvector.tolist()
    eigenvector=[round(e/norm, 8) for e in eigenvector]
    return eigenvector
def mult(m1, m2):
    r1=len(m1)
    r2=len(m2)
    c1=len(m1[0])
    c2=len(m2[0])
    mult=[[0 for i in range(c2)] for j in range(r1)]
    for i in range(r1):
        for j in range(c2):
            for k in range(r2):
                mult[i][j]+=m1[i][k]*m2[k][j]
    return mult

def inverse(matrix):
    n = len(matrix)
    
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    for i in range(n):
        # Find the pivot element
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            return
        
        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    
    inverse_matrix = [row[n:] for row in augmented_matrix]
    
    return inverse_matrix
def stationary_distribution(p, q, r, N):
    """
    Return a list of size N+1 containing the stationary distribution of the Markov chain.
    
    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    
    """
    b=[0 for i in range(N+1)]
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=r[0]
    p1[0][1]=p[0]
    for i in range(1, N):
        p1[i][i-1]=q[i]
        p1[i][i]=r[i]
        p1[i][i+1]=p[i]
    p1[N][N]=r[-1]
    p1[N][N-1]=q[-1]
    I = [[1 if i == j else 0 for j in range(N+1)] for i in range(N+1)]
    p_minus_i=[[I[j][i]-p1[j][i] for j in range(N+1)] for i in range(N+1)]
    p1=np.array(p1)
    p1_T=p1.transpose()
    x=find_eigenvector(p1_T, 1)
    return x
print(stationary_distribution([0.5,0.25,0.25,0],[0,0.25,0.25,0.5],[0.5,0.5,0.5,0.5],3))

def expected_wealth(p, q, r, N):
    """
    Return the expected wealth of the gambler in the long run.

    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    """
    pi=stationary_distribution(p, q, r, N)
    E_wealth = sum(pi[i] * i for i in range(N+1))
    
    return E_wealth

def expected_time(p, q, r, N, a, b):
    """
    Return the expected time for the price to reach b starting from a.

    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    a : int, the starting price
    b : int, the target price
    """
    col=[[1] for i in range(b)]
    
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=r[0]
    p1[0][1]=p[0]
    for i in range(1, N):
        p1[i][i-1]=q[i]
        p1[i][i]=r[i]
        p1[i][i+1]=p[i]
    p1[N][N]=r[-1]
    p1[N][N-1]=q[-1]
    P_T = [row[:b] for row in p1[:b]]
    I = [[1 if i == j else 0 for j in range(b)] for i in range(b)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(b)] for i in range(b)]
    A_inv=inverse(i_minus_p)
    res=mult(A_inv, col)
    return round(res[a][0], 8)
print(expected_time([0.5,0.25,0.25,0],[0,0.25,0.25,0.5],[0.5,0.5,0.5,0.5],3, 1, 2))