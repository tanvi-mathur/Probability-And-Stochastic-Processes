"""
Use the following function to convert the decimal fraction of k/N into it's binary representation
using k_prec number of bits after the decimal point. You may assume that the expansion of 
k/N terminates before k_prec bits after the decimal point.
"""
import math
def decimalToBinary(num, k_prec) : 
  
    binary = ""  
    Integral = int(num)    
    fractional = num - Integral 
   
    while (Integral) :       
        rem = Integral % 2
        binary += str(rem);  
        Integral //= 2

    binary = binary[ : : -1]  
    binary += '.'

    while (k_prec) : 
        fractional *= 2
        fract_bit = int(fractional)  
  
        if (fract_bit == 1) :  
            fractional -= fract_bit  
            binary += '1'       
        else : 
            binary += '0'
        k_prec -= 1
        
    return binary 
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
    Return the probability of winning while gambling aggressively.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    N : int, maximum wealth
    """
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=1
    p1[N][N]=1
    for i in range(1, math.ceil(N/2)):
        p1[i][0]=q
        p1[i][2*i]=p
    for i in range(math.ceil(N/2), N):
        p1[i][2*i-N]=q
        p1[i][N]=p
    A=[[row[0]]+[row[-1]] for row in p1[1:-1]]
    P_T = [row[1:-1] for row in p1[1:-1]]
    I = [[1 if i == j else 0 for j in range(N-1)] for i in range(N-1)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(N-1)] for i in range(N-1)]
    F=inverse(i_minus_p)
    res=mult(F, A)
    return res[k-1][1]

def game_duration(p, q, k, N):
    """
    Return the expected number of rounds to either win or get ruined while gambling aggressively.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    N : int, maximum wealth
    """
    col=[[1] for i in range(N-1)]
    p1=[[0 for i in range(N+1)] for j in range(N+1)]
    p1[0][0]=1
    p1[N][N]=1
    for i in range(1, math.ceil(N/2)):
        p1[i][0]=q
        p1[i][2*i]=p
    for i in range(math.ceil(N/2), N):
        p1[i][2*i-N]=q
        p1[i][N]=p
    P_T = [row[1:-1] for row in p1[1:-1]]
    I = [[1 if i == j else 0 for j in range(N-1)] for i in range(N-1)]
    i_minus_p=[[I[i][j] - P_T[i][j] for j in range(N-1)] for i in range(N-1)]
    F=inverse(i_minus_p)
    res=mult(F, col)
    return res[k-1][0]
