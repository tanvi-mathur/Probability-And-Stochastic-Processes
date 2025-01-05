import numpy as np
import random

def prob_matrix(nA, nB):
    prob={0:([nB/(nA+nB), 0, nA/(nA+nB)], [0.7, 0, 0.3], [5/11, 0, 6/11]), 
          1: ([0.3, 0, 0.7], [1/3, 1/3, 1/3], [0.3, 0.5, 0.2]), 
          2: ([6/11, 0, 5/11], [0.2, 0.5, 0.3], [0.1, 0.8, 0.1])}
    return prob

class Alice:
    
    points=1
    past_play_styles = [1,1] 
    results = [1,0]
    opp_play_styles = [1,1]   

    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 2a here.
         
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        nA=Alice().points
        nB=Bob().points
        
        if Alice().results[-1]==1:
            b=0
        elif Alice().results[-1]==0:
            b=2
        elif Alice().results[-1]==0.5:
            b=1
        E=[1*prob_matrix(nA, nB)[0][b][0]+0.5*prob_matrix(nA, nB)[0][b][1], 1*prob_matrix(nA, nB)[1][b][0]+0.5*prob_matrix(nA, nB)[1][b][1], 1*prob_matrix(nA, nB)[2][b][0]+0.5*prob_matrix(nA, nB)[2][b][1]]
       
        if E[0]==max(E):
            return 0
        elif E[1]==max(E):
            return 1
        else:
            return 2
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        #self.past_play_styles.append(own_style)
        Alice.past_play_styles.append(own_style)
        #self.results.append(result)
        Alice.results.append(result)
        #self.opp_play_styles.append(opp_style)
        Alice.opp_play_styles.append(opp_style)
        Alice.points += result

class Bob:
    
    points=1
    past_play_styles = [1,1] 
    results = [0,1]
    opp_play_styles = [1,1]    

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        if Bob.results[-1] == 1:
            return 2
        elif Bob.results[-1] == 0.5:
            return 1
        else:  
            return 0

    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """ 
        #self.past_play_styles.append(own_style)
        Bob.past_play_styles.append(own_style)
        #self.results.append(result)
        Bob.results.append(result)
        #self.opp_play_styles.append(opp_style)
        Bob.opp_play_styles.append(opp_style)
        Bob.points += result

"""expec_matrix=[]
for i in prob_matrix(Alice.points, Bob.points):
    l=[]
    l.append([i[0][0]*1+i[0][1]*0.5, i[1][0]*1+i[1][1]*0.5, i[2][0]*1+i[2][1]*0.5])
    expec_matrix.append(l)"""

def simulate_round(a, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    alice_wins=0 #if alice wins: 1 (true) otherwise 0 (false)
    
    outcome=np.random.choice(['Alice Wins', "Draw", "Bob Wins"], p=[payoff_matrix[a][bob][0], payoff_matrix[a][bob][1], payoff_matrix[a][bob][2]])  
    if outcome=='Alice Wins':
        Alice().observe_result(a, bob, 1)
        alice_wins=1
    elif outcome=='Bob Wins':
        Bob().observe_result(bob, a, 1)
    else:
        Alice().observe_result(a, bob, 0.5)
        Bob().observe_result(bob, a, 0.5)
    return alice_wins
        
def estimate_tau(T):
    """
    Estimate the expected value of the number of rounds taken for Alice to win 'T' rounds.
    Your total number of simulations must not exceed 10^5.

    Returns:
        Float: estimated value of E[tau]
    """
    
    tau=0
    
    for i in range(10**4):
        e=0
        a=1
        while a<T:
            a+=simulate_round(Alice().play_move(), Bob().play_move(), prob_matrix(Alice().points, Bob().points))
            e+=1
        
        tau+=e
        
    return tau/10**4

print(estimate_tau(17))