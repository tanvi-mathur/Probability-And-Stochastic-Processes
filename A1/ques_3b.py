"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
import numpy as np
M=1000000007
def prob_matrix(nA, nB):
    prob={0:([nB/(nA+nB), 0, nA/(nA+nB)], [0.7, 0, 0.3], [5/11, 0, 6/11]), 
          1: ([0.3, 0, 0.7], [1/3, 1/3, 1/3], [0.3, 0.5, 0.2]), 
          2: ([6/11, 0, 5/11], [0.2, 0.5, 0.3], [0.1, 0.8, 0.1])}
    return prob
lst=[1, 1]

visited={}
total_score=0

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M
def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

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

# Problem 3b
def optimal_strategy(na, nb, tot_rounds):
    """
    Calculate the optimal strategy for Alice maximize her points in the future rounds
    given the current score of Alice(na) and Bob(nb) and the total number of rounds(tot_rounds).
    
    Return the answer in form of a list [p1, p2, p3],
    where p1 is the probability of playing Attacking
    p2 is the probability of playing Balanced
    p3 is the probability of playing Defensive
    """
    global strat
    best_score=0
    alice_pts=na
    bob_pts=nb
    alice_strategy=[0, 1, 2]
    bob_strategy=[0, 1, 2]
    optimal_strat=None
    expec_curr=[1]
    strat=[1]
    #bob=np.random.choice([0,1,2], p=[1/3,1/3,1/3])
    if (na, nb, tot_rounds) in list(visited.keys()):
        return visited[na, nb, tot_rounds]
    if tot_rounds==0:
        return None
    for i in range(tot_rounds):
        for alice in alice_strategy: 
            for bob in bob_strategy:
                
                outcome=np.random.choice(['Alice Wins', 'Draw', 'Bob Wins'], p=prob_matrix(na, nb)[alice][bob])   
                if outcome=='Alice Wins':
                    alice_pts+=1
                elif outcome=='Draw':
                    alice_pts+=0.5
                    bob_pts+=0.5
                else:
                    bob_pts+=1
                expec=1*prob_matrix(alice_pts, bob_pts)[alice][bob][0]+0.5*prob_matrix(alice_pts, bob_pts)[alice][bob][1]
                #expec_total=expec_curr[-1]+expec_future
                if expec>best_score:
                    #expec_future_final=expec_future
                    best_score=expec
                    optimal_strat=alice
        strat.append(optimal_strat)
        #expec_curr.append(expec_future_final)
    visited[(alice_pts, bob_pts, tot_rounds)]=optimal_strat
    prob=[0, 0, 0]
    if optimal_strat==0:
        prob[0]=1
    elif optimal_strat==1:
        prob[1]=1
    else:
        prob[2]=1
    return prob


def expected_points(na, nb, tot_rounds):
    """
    Given the total number of rounds(tot_rounds), calculate the expected points that Alice can score after the tot_rounds,
    assuming that Alice plays optimally.

    Return : The expected points that Alice can score after the tot_rounds.
    """
    t=0
    score=0
    while t<=tot_rounds:
        t+=1
        if optimal_strategy(na, nb, t)[0]==1:
            alice=0
        elif optimal_strategy(na, nb, t)[1]==1:
            alice=1
        else:
            alice=2
        score+=1*prob_matrix(na, nb)[alice][np.random.choice([0,1,2], p=[1/3,1/3,1/3])][0]+0.5*prob_matrix(na, nb)[alice][np.random.choice([0,1,2], p=[1/3,1/3,1/3])][1] 
        
    f=score.as_integer_ratio()
    
    return score
print(optimal_strategy(2, 2, 66), expected_points(2,2, 66))
