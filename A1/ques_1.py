"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
import numpy as np
import random
M=1000000007

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

def fact(k):
    q=1
    for i in range(1, k+1):
        q*=i
    return q
# Problem 1a
def permut_cases(alice_wins, bob_wins):
    lst=['A', 'B']
    cases=[]
    for i in range(alice_wins-1):
        lst.append('A')
    for j in range(bob_wins-1):
        lst.append('B')
    def recur(c):
        if c==len(lst):
            cases.append(lst[:])
            
        duplicate=[]
        for i in range(c, len(lst)):
            if lst[i] in duplicate:
                continue
            lst[c], lst[i]=lst[i], lst[c]
            recur(c+1)
            lst[c], lst[i]=lst[i], lst[c]
            duplicate.append(lst[i])
    recur(2)
    return cases
def c(n, k): #combinatorial
    return fact(n)/(fact(n-k)*fact(k))    
    
def calc_prob(alice_wins, bob_wins):
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """
    P = 0
    N=int(c(alice_wins+bob_wins, bob_wins))
    if alice_wins>1 and bob_wins>1:
        if N<=10**5:
            cases=permut_cases(alice_wins, bob_wins)
            for case in cases:
                p=1
                a=1
                b=1
                for i in range(2, alice_wins+bob_wins):

                    if case[i]=='A':
                        p*=(b/(a+b))
                        a+=1
                    if case[i]=='B':
                        p*=(a/(a+b))
                        b+=1  
                P+=p  
        match=0
        #using importance sampling
        total_weight=0
        for k in range(10**4):
            
            na=1
            nb=1
            A_win=1
            B_win=1
            for i in range(alice_wins+bob_wins-2):
                o=np.random.choice(['A', 'B'], p=[(alice_wins-1)/(alice_wins+bob_wins-2), (bob_wins-1)/(alice_wins+bob_wins-2)]) 
                weight_A=((alice_wins-1)/(alice_wins+bob_wins-2))/(nb/(na+nb))
                weight_B=((bob_wins-1)/(alice_wins+bob_wins-2))/(na/(na+nb))
                if o=='A':
                    na+=1
                    A_win+=1
                    total_weight+=1*weight_A
                elif o=='B':
                    nb+=1
                    B_win+=1 
                    total_weight+=1*weight_B     
            if A_win==alice_wins and B_win==bob_wins:
                match+=1
            
        P=match/total_weight
    elif alice_wins==1 and bob_wins==1:
        P=1
    #[nb/(na+nb), na/(na+nb)]

    f=P.as_integer_ratio()  
    return mod_divide(f[0], f[1])
#print(calc_prob(11, 88))

def c(n, k): #combinatorial
    return fact(n)/(fact(n-k)*fact(k))    
    
# Problem 1b (Expectation)      
def calc_expectation(t):
    """
    Returns:
        The expected value of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    E=[1, -1, ] #AB__
    Pw=[1, 0, ] #probability of winning
    Pl=[0, 1, ] #probability of losing
    for i in range(3, t+1):
        pw=0
        pl=0
        for j in range(0, i-2):
            pw+=(c(i-3, j)/(2**(i-3)))*(((i-2)-j)/(i-1))
            pl+=(c(i-3, j)/(2**(i-3)))*(1-(((i-2)-j)/(i-1)))
        Pw.append(pw)
        Pl.append(pl)
        E.append(Pw[i-1]-Pl[i-1])
    f=sum(E).as_integer_ratio()
    return mod_divide(f[0], f[1])
print(calc_expectation(88))
# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    v=[0, 0, ] #AB__
    Pw=[1, 0, ] #probability of winning
    Pl=[0, 1, ] #probability of losing
    for i in range(3, t+1):
        pw=0
        pl=0
        for j in range(0, i-2):
            pw+=(c(i-3, j)/(2**(i-3)))*(((i-2)-j)/(i-1))
            pl+=(c(i-3, j)/(2**(i-3)))*(1-(((i-2)-j)/(i-1)))
        Pw.append(pw)
        Pl.append(pl)
        v.append(Pw[i-1]+Pl[i-1]-((Pw[i-1]-Pl[i-1])**2))
    f=sum(v).as_integer_ratio()
    return mod_divide(f[0], f[1])
print(calc_variance(88))
