import numpy as np
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

def win_probability(p, q, k, N):
    """
    Return the probability of winning a game of chance.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    N : int, maximum wealth
    """
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=1
    p1[N][N]=1
    for i in range(1, N):
        p1[i][i-1]=q
        p1[i][i+1]=p
    
    P_T = [row[1:-1] for row in p1[1:-1]]
    A=[[row[0]]+[row[-1]] for row in p1[1:-1]]
    I = [[1 if i == j else 0 for j in range(N-1)] for i in range(N-1)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(N-1)] for i in range(N-1)]
    F=inverse(i_minus_p)
    res=mult(F, A)
    
    if p==q:
        prob=k/N
    else:
        prob=(1-(q/p)**k)/(1-(q/p)**N)
    return round(res[k-1][1], 12)
print(win_probability(0.35, 0.65, 3, 10))
def limit_win_probability(p, q, k):
    """
    Return the probability of winning when the maximum wealth is infinity.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    """
    
    return (1-(q/p)**k)

def game_duration(p, q, k, N):
    """
    Return the expected number of rounds to either win or get ruined.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    """
    col=[[1] for i in range(N-1)]
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=1
    p1[N][N]=1
    for i in range(1, N):
        p1[i][i-1]=q
        p1[i][i+1]=p
    
    P_T = [row[1:-1] for row in p1[1:-1]]
    I = [[1 if i == j else 0 for j in range(N-1)] for i in range(N-1)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(N-1)] for i in range(N-1)]
    
    A_inv=inverse(i_minus_p)
    
    res=mult(A_inv, col)
    if p!=q:
        theory=(N/(p-q))*((1-(q/p)**k)/(1-(q/p)**N))+(k/(q-p))
    else:
        theory=(N*k)-k**2*(1+2*(p-q)*k)
    return round(res[k-1][0], 8)
print(game_duration(0.5, 0.5, 5, 10))
