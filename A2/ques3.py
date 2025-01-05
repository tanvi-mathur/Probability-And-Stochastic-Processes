"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
M=1000000007
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
def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))


def game_duration(p, q, k, t, W):
    """
    Return the expected number of rounds the gambler will play before quitting.

    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    t : int, t < k, the gambler will quit if she reaches t
    W : int, the threshold on maximum wealth the gambler can reach
    
    """
    col=[[1] for i in range(k+W-1)]
    p1=[[0 for i in range(k+W+1)] for j in range(k+W+1)]
    p1[0][0]=1
    p1[k+W][k+W-1]=1
    p1[t][t]=1
    for i in range(1, k+W):
        if i==t:
            continue
        p1[i][i-1]=q
        p1[i][i+1]=p
    P_T = [row[1:t]+row[t+1:] for row in p1[1:t]+p1[t+1:]]
    I = [[1 if i == j else 0 for j in range(k+W-1)] for i in range(k+W-1)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(k+W-1)] for i in range(k+W-1)]
    F=inverse(i_minus_p)
    res=mult(F, col)
    return res[k-2][0]
print(game_duration(0.3, 0.7, 201, 200, 1))
