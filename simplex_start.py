#Dan Prendergast
#CSCI 5454: Algorithms
#Problem Set 4, Problem 1a

import numpy as np
import simplex
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import random

def main():
    print ("Welcome to the Simplex Calculator!")
    print ("__________________________________")
    print ("Please enter the augmented matrix for your linear programming problem in canonical form.")
    print ("The last row should be the objective function.  Separate values in a row with commas, and")
    print ("start new rows with semicolons.")

    #tableau = np.mat(input("Enter matrix here: "))
    #num_slack_vars = int(input("How many slack variables are in your constraint equations? "))
    #print (tableau)

    #Test case 1:  Example 6 in the book
    #tableau = np.mat('1,0,1,0,0,0,30;0,1,0,1,0,0,20;1,2,0,0,1,0,54;-2,-3,0,0,0,1,0', dtype=float)
    #num_slack_vars = 3

    #Test case 2:  Example 5 in the book
    tableau = np.mat('1,0,1,0,0,0,30;0,1,0,1,0,0,20;1,2,0,0,1,0,54;-2,-3,0,0,0,1,0', dtype=float)


    opt_value, x = simplex.calc(tableau, num_slack_vars)

    if opt_value==0 and x==0:
        print("Unbounded")

    print ("opt value =",opt_value)
    print ("x coefficients =",x)

# def main():
#     # Setup initial parameters
#     print "Welcome to the Hedge Game!"
#     print "Let's setup the game."
#     num_games = np.int(raw_input("How many games would you like to play? "))
#     row_order = np.int(raw_input("How many action options would you like? "))
#     column_order = np.int(raw_input("How many action options should the computer have? "))
#     num_rounds = np.int(raw_input("How many rounds per game would you like to play? "))
#
#     # Initialize the game score matrix
#     game_scores = np.zeros(shape=(2,num_games), dtype=np.int)
#
#     # Begin loop for the appropriate number of game_scores
#     for game in range(num_games):
#         print "Begin game ",game+1
#         # Initialize the payoff matrix
#         max_payoff = 10
#         M = [[random.randint(-10,10) for j in range(column_order)] for i in range(row_order)]
#
#         # Determin board value
#         M_value = game_value(M, max_payoff)
#         print "Gameboard value is ",M_value
#
#         # Initialize AI parameters
#         weights, p_t, eta = initialize_AI(num_rounds, row_order)
#
#         # Begin the loop for each round
#         for round in range(num_rounds):
#             # Display the payoff matrix every 4 rounds
#             if round%4==0:
#                 print "The payoff matrix is..."
#                 for i in range(row_order):
#                     print(M[i][:])
#
#             # Get users move
#             user_move = np.int(raw_input("     What row would you like to play (Enter row number 1 - x)? "))
#             user_move = user_move-1
#
#             # Calculate AI's move
#             AI_move = np.int(np.random.choice(column_order, p=p_t))
#             print "     The computer chose column ",AI_move+1
#
#             # Return the rewards
#             print "     The reward to you is",M[user_move][AI_move]
#
#             # Update the game score
#             game_scores[0,game] = game_scores[0][game]+M[user_move][AI_move]
#             game_scores[1,game] = game_scores[1][game]-M[user_move][AI_move]
#
#             # Update the weights and p_t
#             weights, p_t = update_AI(M, weights, p_t, eta, user_move, max_payoff)
#
#         # Display total score for the game
#         print "You scored ",game_scores[0][:]
#         print "The computer scored ",game_scores[1][:]
#         print "The final AI weights are ",weights
#         print "The final AI probabilities are ",p_t
#
#
# def initialize_AI(num_rounds, column_order):
#     # Initialize the weights to 1, the probabilites to 1/#ofcolumns, and optimize eta
#     weights = np.ones(column_order, dtype=np.float64)
#     p_t = weights/np.sum(weights)
#     eta = np.sqrt((8*(np.log(column_order))/num_rounds))
#
#     #print "p_t =",p_t
#     #print "eta =",eta
#
#     return weights, p_t, eta
#
# def update_AI(M, weights, p_t, eta, user_move, max_payoff):
#     # Update the weights array
#     for i in range(len(weights)):
#         weights[i] = weights[i]*(np.exp(-eta*M[user_move][i]/max_payoff))
#
#     # Update the probability array
#     for j in range(len(weights)):
#         p_t[j] = weights[j]/np.sum(weights)
#
#     #print "weights =",weights
#     #print "p_t = ",p_t
#
#     return weights, p_t
#
# def game_value(M, max_payoff):
#     # Initialize weights for the AI's
#     row_order1 = len(M)
#     column_order1 = len(M[0])
#     T = 313*len(M)
#     weights1, p_t1, eta1 = initialize_AI(T, row_order1)
#     weights2, p_t2, eta2 = initialize_AI(T, column_order1)
#
#     for i in range(T):
#         # Perform the moves for the two AI's
#         AI_move1 = np.int(np.random.choice(row_order1, p=p_t1))
#         AI_move2 = np.int(np.random.choice(column_order1, p=p_t2))
#
#         # Update weights and probs for the two AI's
#         weights1, p_t1 = update_AI(M, weights1, p_t1, eta1, AI_move2, max_payoff)
#         weights2, p_t2 = update_AI(M, weights2, p_t2, eta2, AI_move1, max_payoff)
#
#         #if i == 1:
#         #    print "weights1 =",weights1
#         #    print "p_t1 =",p_t1
#         #    print "weights2 =",weights2
#         #    print "p_t2 =",p_t2
#
#         #if i > T-3:
#         #    print "weights1 =",weights1
#         #    print "p_t1 =",p_t1
#         #    print "weights2 =",weights2
#         #    print "p_t2 =",p_t2
#
#     # Calculate gameboard value
#     M_value = 0
#     for i in range(row_order1):
#         for j in range(column_order1):
#             M_value = M_value + (M[i][j]*p_t1[i]*p_t2[j])
#
#     return M_value

if __name__=="__main__":
   main()
