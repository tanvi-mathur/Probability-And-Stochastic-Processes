import numpy as np
import random
"""0 : attack
1 : balanced
2 : defence """
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
        Decide Alice's play style for the current round. If you think there is no better strategy than 2a,
        then implement the same strategy here. Else implement that non greedy strategy here.
        
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        nA=Alice().points
        nB=Bob().points
        if nA<nB:
            if Alice().results[-1]==1:
                return 2
            elif Alice.results[-1]==0.5:
                return 0
            elif Alice.results[-1]==0:
                return 0
        if nA>nB:
            if Alice().results[-1]==1:
                return 2
            elif Alice().results[-1]==0.5:
                return 0
            else:
                return 0
        else:
            return 1
        
        
    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
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
        Bob.past_play_styles.append(own_style)
        #self.results.append(result)
        Bob.results.append(result)
        #self.opp_play_styles.append(opp_style)
        Bob.opp_play_styles.append(opp_style)
        Bob.points += result
 

def simulate_round(a, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    global alice_win
    global bob_win
   
    outcome=random.choices(['Alice Wins', "Draw", "Bob Wins"], [payoff_matrix[a][bob][0], payoff_matrix[a][bob][1], payoff_matrix[a][bob][2]], k=1)[0]  
    if outcome=='Alice Wins':
        Alice().observe_result(a, bob, 1)
        alice_win=1
        bob_win=0
    elif outcome=='Bob Wins':
        Alice().observe_result(a, bob, 0)
        Bob().observe_result(bob, a, 1)
        bob_win=1
        alice_win=0
    else:
        Alice().observe_result(a, bob, 0.5)
        alice_win=0.5
        Bob().observe_result(bob, a, 0.5)
        bob_win=0.5

def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    """global a
    global b
    alice_score=0
    bob_score=0
    for i in range(num_rounds):
        alice=0
        bob=0
        simulate_round(Alice().play_move(), Bob().play_move(), prob_matrix(Alice().points, Bob().points))
        alice+=alice_win
        bob+=bob_win
        alice_score+=alice
        bob_score+=bob
    a=alice_score/num_rounds
    b=bob_score/num_rounds"""
    for i in range(num_rounds):
        simulate_round(Alice().play_move(), Bob().play_move(), prob_matrix(Alice().points, Bob().points)) 

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10**5)
    print(Alice().points, Bob().points)