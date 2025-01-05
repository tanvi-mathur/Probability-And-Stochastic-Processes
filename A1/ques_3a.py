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
        Decide Alice's play style for the current round. Implement your strategy for 3a here.
        
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        best_score=0
        alice_pts=Alice().points
        bob_pts=Bob().points
        alice_strategy=[0, 1, 2]
        bob_strategy=[0, 1, 2]
        optimal_strat=None
        expec_curr=[1]
        strat=[1]
        for alice in alice_strategy: 
            for bob in bob_strategy:
                
                outcome=np.random.choice(['Alice Wins', 'Draw', 'Bob Wins'], p=prob_matrix(alice_pts, bob_pts)[alice][bob])   
                if outcome=='Alice Wins':
                    alice_pts+=1
                elif outcome=='Draw':
                    alice_pts+=0.5
                    bob_pts+=0.5
                else:
                    bob_pts+=1
                expec_future=1*prob_matrix(alice_pts, bob_pts)[alice][bob][0]+0.5*prob_matrix(alice_pts, bob_pts)[alice][bob][1]
                expec_total=expec_curr[-1]+expec_future
                if expec_total>best_score:
                    expec_future_final=expec_future
                    best_score=expec_total
                    optimal_strat=alice
        strat.append(optimal_strat)
        expec_curr.append(expec_future_final)
        return optimal_strat
    
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
        move = np.random.choice([0, 1, 2])
        return move
        
    
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
 
alice_wins=1
def simulate_round(a, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    global alice_wins
    
    outcome=random.choices(['Alice Wins', "Draw", "Bob Wins"], [payoff_matrix[a][bob][0], payoff_matrix[a][bob][1], payoff_matrix[a][bob][2]], k=1)[0]  
    if outcome=='Alice Wins':
        Alice().observe_result(a, bob, 1)
        alice_wins+=1
    elif outcome=='Bob Wins':
        Bob().observe_result(bob, a, 1)
    else:
        Alice().observe_result(a, bob, 0.5)
        Bob().observe_result(bob, a, 0.5)

def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    for i in range(num_rounds):
        simulate_round(Alice().play_move(), Bob().play_move(), prob_matrix(Alice().points, Bob().points))  
 
# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=88)
    print(Alice().points, Bob().points)
    print(Alice().results)