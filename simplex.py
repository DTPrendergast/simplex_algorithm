#Dan Prendergast
#CSCI 5454: Algorithms
#Simplex Implementation Project

import numpy as np
import simplex
import random
import time
import csv

def main():
    print ("Welcome to the Simplex Calculator!")
    print ("__________________________________")
# This program operates in 3 modes based on how the initial tableau will be created.
# Allow user to select the mode of operation.
    print ("Select from the following two options...")
    print ("     1. Manually enter a linear programming matrix")
    print ("     2. Randomly generate a linear programming matrix")
    print ("     3. Use hard coded example matrix")
    select = int(input("Select 1, 2, or 3 and press enter: "))

# Establish initial tableau based on user selection above.
    if select==1:
        print ("Please enter the augmented matrix for your linear programming problem in canonical form.")
        print ("The last row should be the objective function.  Separate values in a row with commas, and")
        print ("start new rows with semicolons.")
        tableau = np.mat(input("Enter matrix here: "), dtype=float)
        num_slack_vars = int(input("How many slack variables are in your constraint equations? "))

    elif select==2:
        num_vars = int(input("Enter the number of variables (not including slack variables): "))
        num_eqns = int(input("Enter the number of constraint inequalities: "))
        size_coeff = int(input("Enter the max value of the coefficients: "))
        Pr_zeros = float(input("Enter the probability (value from 0-1) that coefficients are zero: "))
        num_slack_vars = num_eqns
        tableau = build_tableau(num_vars, num_eqns, size_coeff, Pr_zeros)

    elif select==3:
        #Test case 1:  Example 6 in the book
        tableau = np.mat('1,0,1,0,0,0,30;0,1,0,1,0,0,20;1,2,0,0,1,0,54;-2,-3,0,0,0,1,0', dtype=float)
        num_slack_vars = 3

# Calculate the solution
    np.set_printoptions(precision=2)
    opt_value, x = simplex.calc(tableau, num_slack_vars)

# Display the results of the simplex calculation
    np.set_printoptions(precision=5)
    if opt_value=="unbounded":
        print("Solution is unbounded.")
    elif opt_value=="optimal":
        print("System is already optimal.  Optimal system value and variable values are 0.")
    else:
        print("Success!  Final Tableau =")
        print(tableau)
        print ("opt value =",opt_value)
        print ("x coefficients =",x)

# This fuction automatically builds the initial tableau if user selected option 2 above
def build_tableau(num_vars, num_eqns, size_coeff, Pr_zeros):
    tableau = np.zeros((num_eqns+1,num_vars+num_eqns+2))

    # Build the A matrix of coefficients for the constraint equations
    for i in range(num_eqns):
        for j in range(num_vars):
            irf = np.random.choice([0,1], p=[Pr_zeros,1-Pr_zeros])
            if irf==1:
                while tableau[i,j]==0:
                    tableau[i,j] = random.randint(1,size_coeff)

    # Build the c matrix of coefficients for the objective function
    for j in range(num_vars):
        while tableau[num_eqns,j]==0:
            tableau[num_eqns,j] = random.randint(-size_coeff,size_coeff)

    # Build the identity matrix for the slack variables
    for k in range(num_eqns+1):
        tableau[k,num_vars+k] = 1

    # Build the b matrix of values for the right side of the constraint equations
    for l in range(num_eqns):
        tableau[l,num_vars+num_eqns+1] = random.randint(1,size_coeff)

    return tableau

# This function calculates the solution to the linear program
def calc(tableau, num_slack_vars):

    rows, columns = tableau.shape

    # Find the negative c values in the objective function
    neg_c_index = find_neg_c(tableau, rows, columns)

    # Begin loop of pivots until there are no more negative c values in the objective function
    #unbounded_obj = 1
    already_optimal = 1
    while (neg_c_index):
        already_optimal = 0
        print("*******************************************************")
        print(tableau)

        # Find the pivot element of the current tableau
        pivot_row, pivot_column, unbounded_obj = find_pivot(tableau, rows, columns, neg_c_index)

        # If the find_pivot function found that the system is unbounded, exit the loop
        if unbounded_obj==1:
            break

        # Perform the pivot
        pivot(tableau, rows, columns, pivot_row, pivot_column)
        # Recalculate the new array of negative c values
        neg_c_index = find_neg_c(tableau, rows, columns)

    # Assign values to x and opt_val based on the results of system calculation
    if already_optimal==1:
        x = "optimal"
        opt_value = "optimal"
    elif unbounded_obj==1:
        print("No solution. Objective is Unbounded.")
        x = "unbounded"
        opt_value = "unbounded"
    else:
        x = read_x(tableau, rows, columns, num_slack_vars)
        opt_value = tableau[rows-1,columns-1]

    # Return optimal value and x array
    return opt_value, x

# Find the negative values for c or M in the objective function (last row of tableau)
def find_neg_c(tableau, rows, columns):
    neg_c_index = []
    for j in range(columns-1):
        if tableau[rows-1,j]<0:
            neg_c_index.append(j)

    return neg_c_index

# Find the pivot element in the tableau
def find_pivot(tableau, rows, columns, neg_c_index):
    # pivot column is the column with the most negative c value
    pivot_column = 0
    for j in range(len(neg_c_index)):
        if tableau[rows-1,neg_c_index[j]]<tableau[rows-1,pivot_column]:
            pivot_column = neg_c_index[j]

    # pivot row is selected according to Bland Rules (see report): a[i,pivot_column]>0 and
    # b[i]/a[i,pivot_column] is min and nonnegative
    pivot_row = 0
    prev_ratio = float("inf")
    unbounded_obj = 1
    for i in range(rows-1):
        if unbounded_obj==1:
            if tableau[i,pivot_column]>0:
                unbounded_obj = 0

        if tableau[i,pivot_column]==0:
            ratio = float("inf")
        else:
            ratio = tableau[i,columns-1]/tableau[i,pivot_column]

        if tableau[i,pivot_column]>0 and ratio>=0 and ratio<prev_ratio:
            pivot_row = i
            prev_ratio = ratio

    print("pivot element = (",pivot_row,",",pivot_column,")")
    return pivot_row, pivot_column, unbounded_obj

# Perform the pivot operation
def pivot(tableau, rows, columns, pivot_row, pivot_column):
    pivot_val = tableau[pivot_row,pivot_column]

    # Subtract multiples of the pivot row from every other row to make the cell values in the
    # pivot column equal to 0.
    for i in range(rows):
        if i!=pivot_row:
            factor = tableau[i,pivot_column]/pivot_val
            for j in range(columns):
                tableau[i,j] = tableau[i,j] - (factor*tableau[pivot_row,j])

    # Divide the pivot row by the pivot value resulting in the cell with the pivot value being
    # equal to 1
    for j in range(columns):
        tableau[pivot_row,j] = tableau[pivot_row,j]/pivot_val

# Read the solution from the final tableau
def read_x(tableau, rows, columns, num_slack_vars):
    print("Reading tableau..........")
    x = np.zeros(columns-(num_slack_vars+2))
    for j in range(columns-(num_slack_vars+2)):
        basic_var_row = -1
        is_basic_var = 1
        for i in range(rows):
            if tableau[i,j]!=0 and tableau[i,j]!=1:
                is_basic_var = 0
            if tableau[i,j]==1:
                basic_var_row = i
        if is_basic_var==1:
            x[j] = tableau[basic_var_row,columns-1]
        elif is_basic_var==0:
            x[j] = 0

    return x

if __name__=="__main__":
   main()
