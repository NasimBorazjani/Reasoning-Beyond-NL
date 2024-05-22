import re
from openai import OpenAI
from NLR_dataset_var_entanglement import get_problems
import pytholog as pl
import subprocess
from threading import Timer
import time
import argparse
from collections import Counter


prompt_mwp = """The goal is to solve math word problems by converting natural language statements of the problem to prolog statements. The numerical values of the entities in the statement are encoded in prolog variables. The relationship between the variables is expressed as a set of equalities in a function called “problem”. It is important to note that the goal is to describe the problem statements, not to solve the resulting linear equations.
Variable names are a brief description of the entity in the problem. The name assigned to entities that have different numerical values must be different. Variables in an arithmetic statement in the “problem” function must have compatible units. 


When I was half my current age, my father was 30. When I was ⅓ my current age, my mother was 25. And when I was ⅙ of my current age, my sister was 7. If the sum of my age, my sister’s age, my father’s age, and my mother’s age is 116, then how old am I now?

problem(My_current_age) :-
{% When I was half my current age, my father was 30. Thus, my father's current age is 30 plus the number of years that have passed since I was half my current age.
Years_since_I_was_half_my_age = My_current_age -  1/2 * My_current_age,
My_father_current_age = 30 + Years_since_I_was_half_my_age,


% When I was 1/3 my current age, my mother was 25. First we need to calculate how many years ago I was 1/3 of my current age:
Years_since_I_was_one_third_my_age =  My_current_age  -  1/3 * My_current_age,
% My mother's current age is 25 plus the number of years that have passed since I was I/3 of my current age.
My_mother_current_age = 25 + Years_since_I_was_one_third_my_age,


% When I was 1/6 of my current age, my sister was 7. Thus, we need to add 7 to the number of years that have passed since I was 1/6 my current age to get my sister's current age.
Years_since_I_was_one_sixth_my_age =  My_current_age  -  1/6 * My_current_age,
My_sister_current_age = 7 + Years_since_I_was_one_sixth_my_age,


% The sum of my age, my sister’s age, my father’s age, and my mother’s age is 116
My_current_age + My_sister_current_age + My_father_current_age + My_mother_current_age = 116}.


We have 200 apples that we splitted between 4 salespeople (called X, Y, Z, and T) to sell at a fair. The sum of apples we gave Y and Z is 10 less than the sum we gave to X and T. In the fair X and Z sold all their apples; Y had to throw out 10 of the apples we gave him, and T threw out 5. The sum of the number of apples that T and Y sold is 5 less than twice the number of apples Z sold. X and Y set the price of each of their apples equivalent to 1/10th the number of apples they were each given, in dollars. Z set the price of each of his apples equivalent to 1/8 times the number he received, and T’s price for each apple was twice Z’s price. And T’s price for each apple is $3 more expensive than X’s price. What is the total money that the 4 salespeople made from selling the apples in the fair?

problem(Total_money_4_salespeople):-
{% A sum of 200 apples was given to 4 salespeople, X, Y, Z, and T.
Apples_given_X + Apples_given_Y + Apples_given_Z + Apples_given_T = 200,


% The sum of apples given to Y and Z is 10 less than the sum given to X and T
Apples_given_Y + Apples_given_Z = Apples_given_X + Apples_given_T,


% X and Z sold all their apples in the fair.  
Apples_sold_X = Apples_given_X,
Apples_sold_Z = Apples_given_Z,


% Y sold all but 10 of the apples (which he had to throw out) given to him
Apples_sold_Y = Apples_given_Y - 10,


% And T threw out 5 of the apples given to him, thus the number of apples he sold is 5 less then the number given to him.
Apples_sold_T = Apples_given_T - 5,


% The sum of the number of apples that T and Y sold is 5 less than 2 times the number of apples Z sold.
Apples_sold_T + Apples_sold_Y = 2 * Apples_sold_Z - 5,


% X set the price of each of his apples equal to 1/10 times the number of apples he was given, in dollars.
Price_each_apple_X = 1/10 * Apples_given_X,
% Y used the same strategy to set the price of each of his apples
Price_each_apple_Y = 1/10 * Apples_given_Y,


% Z set the price of each of his apples equivalent to 1/8 times the number of apples he was given.
Price_each_apple_Z = 1/8 * Apples_given_Z,


% T’s price for each apple is two times Z’s price for each apple.
Price_each_apple_T = 2 * Price_each_apple_Z,


% T’s price for each apple is $3 more than X’s price for each apple.
Price_each_apple_T = Price_each_apple_X + 3,


% To get the total money made from selling the apples, we must sum the earnings of the 4 salespeople.
% The earning of each salesperson is the number of apples they sold multiplied by their price for each apple.
Total_money_4_salespeople = Apples_sold_X * Price_each_apple_X + Apples_sold_Y * Price_each_apple_Y + Apples_sold_Z * Price_each_apple_Z + Apples_sold_T * Price_each_apple_T}.


We have a list of 8 numbers. If we subtract the number at index i+2  from the i_th number, we get the number at index i+1, for i less than 7 and greater than 0, indexing from 1. If the 3rd number in the list is -2 and the last number in the list is 41, then what is the sum of all numbers in this list?

problem(Sum_of_all_numbers):-
{% We know that in this list i_th number minus the number at index i+2 of the list results in the number at index i+1. i ranges from 1 to 6. Thus, starting from i = 1, we have:
First_number - Third_number = Second_number,
Second_number - Fourth_number = Third_number,
Third_number - Fifth_number = Fourth_number,
Fourth_number - Sixth_number = Fifth_number,
Fifth_number - Seventh_number = Sixth_number,
% i ranges from 1 to 6. Thus for i = 6, the given rule indicates that if we subtract the 8th number from the 6th number, we would get the 7th number.
Sixth_number - Eighth_number = Seventh_number,


Third_number = -2,
Eighth_number = 41,


% The sum of all the 8 numbers in the list is:
Sum_of_all_numbers = First_number + Second_number + Third_number + Fourth_number + Fifth_number + Sixth_number + Seventh_number + Eighth_number}.
 

Alex, Sam, and Andy got some money as a Christmas gift. Alex deposits all of his money in a bank account with an interest rate of 20 percent for 2 years. Sam deposits his money in an account with the same interest rate, but he spends 40% of the total money he has in the account after one year and keeps the rest deposited in the bank for the 2nd year. Andy buys a laptop with some of his money for which he pays a deposit of $50, and a monthly payment of $10 for two years, and keeps the rest of the money for 2 years. By the end of the 2nd year, if Sam gives $72 to Alex, then they’d have the same amount of money; this amount would be 3 times the amount Andy has after 2 years. Alex has 48 dollars more than twice the amount Andy has by the end of the 2nd year. What is the sum of their Christmas money in the beginning?

problem(Sum_chrismas_money):-
{Bank_interest_rate = 0.2,
% Alex deposited his Christmas money in the bank for 2 years. Thus, the amount he has after two years of receiving 20% interest on his money is
Alex_money_end_of_two_years = Alex_chrismas_money * (1 + Bank_interest_rate) * (1 + Bank_interest_rate),


% Sam deposited his Christmas money in the bank for one year. Thus after one year the total amount he has after receiving an interest of 20% on his deposit is:
Sam_money_end_of_first_year = Sam_christmas_money * (1 + Bank_interest_rate),
% Sam spent 40% of the money he had in the account after one year. Now his money equals:
Sam_money_end_of_first_year_after_spending = Sam_money_end_of_first_year -  0.4 * Sam_money_end_of_first_year,
% Sam kept the rest of his money deposited in the bank for the 2nd year and received 20% interest on his deposit.
Sam_money_end_of_two_years = Sam_money_end_of_first_year_after_spending * (1 + Bank_interest_rate),


% Andy made a purchase with his money for which he paid $50 initially and $10 for 24 months. So his remaining money equals:
Andy_money_end_of_two_years = Andy_christmas_money - 50 - 24 * 10,


% After 2 years, if Sam gives Alex $72, i.e. if Sam's money is $72 less and Alex's money is $72 more, then they’d have the same amount.
Sam_money_end_of_two_years - 72 = Alex_money_end_of_two_years + 72,


% If Sam gives Alex $72, then he would have three times as much money as Andy.
Sam_money_end_of_two_years - 72 = 3 * Andy_money_end_of_two_years,


% By the end of the 2nd year, Alex's money is $48 more than twice the amount Andy has.
Alex_money_end_of_two_years = Andy_money_end_of_two_years * 2 + 48,


% The sum of Alex's, Sam's, Alex's Christmas money in the beginning is:
Sum_chrismas_money = Alex_chrismas_money + Sam_christmas_money + Andy_christmas_money}.


We have a 3x3 grid of numbers. We know that in each 2x2 subgrid of this grid, the sum of the two numbers in one diagonal equals the sum of the two other numbers in the other diagonal. We also know that the number at the center of the grid equals the number at the 3rd row and 3rd column of the grid (counting left to right, top down). Below is the grid that we have, our task is to determine the numbers in the locations marked as X

3 X X
X 7 9
2 X X

What is the sum of all the numbers on this grid?

problem(Sum_numbers_marked_X):-
{% We have a 3x3 grid. Let's name the each grid I_11 to I_33, referring to the row and column index of the grid
% In each 2x2 subgrid of this grid, the sum of the two numbers in diagonal grids equals the sum of the two other numbers in the other diagonal
% The first subgrid is in the top left corner, including grids I_11, I _12, I_21, I_22. Thus based on the given condition:
I_11 + I_22 = I_12 + I_21,
% The second subgrid is in the top right corner, including grids I_12, I_13, I_22, I_23.
I_12 + I_23 = I_13 + I_22,
% The third subgrid is in the bottom left corner and includes grids I_21, I_22, I_31, I_32.
I_21 + I_32 = I_31 + I_22,
% The last subgrid is in the bottom right core and includes grids I_22, I_23, I_32, I_33.
I_22 + I_33 = I_32 + I_23,


% The number at the center of the grid, I_22, equals the I_33
I_22 = I_33,


% From the grid representation given, we can deduce
I_11 = 3,
I_22 = 7,
I_23 = 9,
I_31 = 2,


% The sum of all the numbers marked as X on this grid is
Sum_numbers_marked_X = I_12 + I_13 + I_21 + I_32 + I_33}.


Solve the below problem in the same format by encoding the problem as prolog equalities step by step. Each equality either assigns a numerical value to a variable or describes the relationship between variables. Completion must end in ‘}.’

#####
"""
prolog_code_mwp = """:- use_module(library(clpq)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(Answer),
    write(Answer),
    halt.

"""

prolog_code_constraint = """:- use_module(library(clpfd)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(Answer),
    write(Answer),
    halt.
"""
prompt_constraint = """The goal is to solve constraint satisfaction problems by converting the constraints and information given in the natural language statements of the problem to prolog statements. The numerical values of the entities in the statement are encoded in prolog variables. The relationship between the variables is expressed as a set of equalities, inequalities, or absolute value equations in a predicate called “problem”. It is important to note that the goal is to describe the problem statements, not to solve the resulting system of inequalities.
Variable names are a brief description of the entity in the problem. The name assigned to entities that have different numerical values must be different. 

Out of a deck of 52 cards, some cards are lost. We know the number of lost cards is less than half of the deck. If we deal the remaining cards among 4 people, 3 cards remain. If we deal among three people, 2 cards remain, and if we deal among 5 people, 2 cards remain. How many cards are there in the deck?

problem(Remaining_cards):-
% There are 52 cards in a deck of cards
Deck_of_cards #= 52,
% Some of the cards are lost, thus now:
Deck_of_cards #= Lost_cards + Remaining_cards,
% At least 1 card is lost and the number of lost cards is less than half the number of cards in the deck
Lost_cards #> 0,
Lost_cards #< 26,
% If we split the remaining cards between 4 people equally, 3 remain.
Remaining_cards mod 4 #= 3,
% If we deal among three people, 2 cards remain.
Remaining_cards mod 3 #= 2,
% And if we deal among 5 people, 2 cards remain.
Remaining_cards mod 5 #= 2.


A robot and 5 blocks are positioned on a 6x6 grid. The grid coordinates are given by the row number (counting from left to right, starting from 1) and the column number (counting from top to bottom, starting from 1). Each block occupies a single grid square, and multiple blocks can be stacked on top of each other. Block1 is located at (2, 3), Block2 at (4, 3), and Block3 at (2, 5). Block4 is in the same row as Block3 but with one column separating them. Block5 is in the same column as Block4, with one row separating it from Block1. The robot is in the 3rd column and begins moving from row 1 and stops moving at row 5. How many blocks will the robot move?

problem(Blocks_moved_total):-
% Block1 is located at 2nd row, 3rd column
Block1_row #= 2,
Block1_col #= 3,


% Block2 is on row 4, col 3
Block2_row #= 4,
Block2_col #= 3,


% Block3 is at (2, 5)
Block3_row #= 2,
Block3_col #= 5,


% Block4 is in the same row as Block3
Block4_row #= Block3_row,
% There's one column between Block3 and Block4. Thus the difference between Block4's and Block3's column numbers is 2.
abs(Block4_col - Block3_col) #= 2,
% We know that Block4 is positioned on the 6x6 grid. Therefore, the column number of Block4 must be in the [1, 6] range.
Block4_col #>= 1,
Block4_col #=< 6,


% Block5 is in the same column as Block4
Block5_col #= Block4_col,
% One row is separating Block5 and Block1, thus the absolute difference between Block5's row number and Block1's row number is 2.
abs(Block5_row - Block1_row) #= 2,
% The row number of Block5 must be within the bounds of the 6x6 grid.
Block5_row #>= 1,
Block5_row #=< 6,


% Now we can check to see how many of the blocks are positioned on the robot's path and thus are moved by the robot.
% Iterating through each block; for the block to be moved, it must be placed the 3rd column and row 1 to 5
% Initializing the count of blocks moved as 0
Blocks_moved_b0 = 0,
% If Block1 is on the third column and on rows 1 to 5:
((Block1_col #= 3, Block1_row #=< 5, Block1_row #>= 1)
% Then updated count of blocks moved must be incremented by 1
-> Blocks_moved_b1 #= Blocks_moved_b0 + 1;
% Otherwise the count of number of blocks moved stays the same
Blocks_moved_b1 #= Blocks_moved_b0),


% Iterating through the rest of the blocks, and updating the count of moved blocks accordingly
((Block2_col #= 3, Block2_row #=< 5, Block2_row #>= 1)
-> Blocks_moved_b2 #= Blocks_moved_b1 + 1 ;
Blocks_moved_b2 #= Blocks_moved_b1),


((Block3_col #= 3, Block3_row #=< 5, Block3_row #>= 1)
-> Blocks_moved_b3 #= Blocks_moved_b2 + 1 ;
Blocks_moved_b3 #= Blocks_moved_b2),


((Block4_col #= 3, Block4_row #=< 5, Block4_row #>= 1)
-> Blocks_moved_b4 #= Blocks_moved_b3 + 1 ;
Blocks_moved_b4 #= Blocks_moved_b3),


% After checking whether or not block5 is on the robot;s path,we have the final count of the number of blocks moved.
((Block5_col #= 3, Block5_row #=< 5, Block5_row #>= 1)
-> Blocks_moved_total #= Blocks_moved_b4 + 1 ;
Blocks_moved_total #= Blocks_moved_b4).


We are attempting to crack a safe with a 4-digit code. We have the following clues about the pin: The second digit from the right is not divisible by 2 and it’s not divisible by 3. This digit is larger than two of the other digits in the pin. Also this digit is equal to the difference between two of the other digits in the pin. Each digit in the pin is unique. The 4-digit number is an odd number. And the sum of the first and third digits from the right is 15. What is this 4-digit number?

problem(Pin_number):-
% We are given information about each digit of the pin number. To get the pin number, we can write it in terms of the digits:
% Counting the digits from right to left
Pin_number #= 1000 * Digit4 + 100 * Digit3 + 10 * Digit2 + Digit1,


% Each of the digits of the pin are single digit numbers in range [0, 9]
Digit1 #>= 0,
Digit1 #< 10,
Digit2 #>= 0,
Digit2 #< 10,
Digit3 #>= 0,
Digit3 #< 10,
% Besides the leftmost digit which can not be 0 because otherwise the pin would be a 3 digit number.
% The leftmost number must be in range [1, 9]
Digit4 #> 0,
Digit4 #< 10,


% The second digit is not divisible by 2 and it’s not divisible by 3.
Digit2 mod 2 #\= 0,
Digit2 mod 3 #\= 0,


% We know that the second digit is larger than two of the other digits, but we don't know which 2 of the remaining 3 digits.
% We can encode this constraint by considering all 3 possibilities: Digit2 is either larger than the 1st and 3rd digits or the 1st and 4th digits or the 3rd and 4th digits
((Digit2 #> Digit1, Digit2 #> Digit3); (Digit2 #> Digit1, Digit2 #> Digit4); (Digit2 #> Digit3, Digit2 #> Digit4)),


% The second digit is also equal to the absolute difference between two of the other digits in the pin. There are 3 possibilities again:
(abs(Digit1 - Digit3) #= Digit2; abs(Digit1 - Digit4) #= Digit2; abs(Digit3 - Digit4) #= Digit2),


% Each digit in the pin is unique, thus o 2 digits in the pin can be equal.
Digit1 #\= Digit2,
Digit1 #\= Digit3,
Digit1 #\= Digit4,
Digit2 #\= Digit3,
Digit2 #\= Digit4,
Digit3 #\= Digit4,


% The 4-digit pin number is odd thus
Pin_number mod 2 #= 1,
% The sum of the first and third digits is 15
Digit3 + Digit1 #= 15.

In a street there’s only a blue, a green, a red, and a yellow house. We don’t know the order of the houses. One pet lives in each house; we know that there’s only a rabbit, a lizard, a dog, and a cat living on this street. The green and red houses are neighbors, and the house with the rabbit and the  house with the lizard are next to each other, the blue house is the house after the house with the dog, and the cat lives in the blue house, and the red house is the first house. What’s the index of the house with the dog in this street, counting from 1?

problem(Index_house_with_dog):-
% We want to discover the order of the houses in this street. To do so, we must encode the possible range for the index of each house.
% There's a blue, a green, a red, and a yellow house in the street, and we count from one, thus the index of each house must be in range [1, 4]
Index_green_house #>= 1,
Index_green_house #=< 4,
Index_blue_house #>= 1,
Index_blue_house #=< 4,
Index_red_house #>= 1,
Index_red_house #=< 4,
Index_yellow_house #>= 1,
Index_yellow_house #=< 4,
% Moreover, the index of each house is unique in this range, ie no 2 houses have the same index
Index_green_house #\= Index_blue_house,
Index_green_house #\= Index_red_house,
Index_green_house #\= Index_yellow_house,
Index_blue_house #\= Index_red_house,
Index_blue_house #\= Index_yellow_house,
Index_red_house #\= Index_yellow_house,


% Also, we know one pet lives in each house, and there’s only a rabbit, a lizard, a dog, and a cat living on this street.
% We are given constraints about the order of houses with the pets, thus we must encode the index range of the houses with regards to the pets as well.
Index_house_with_rabbit #>= 1,
Index_house_with_rabbit #=< 4,
Index_house_with_lizard #>= 1,
Index_house_with_lizard #=< 4,
Index_house_with_dog #>= 1,
Index_house_with_dog #=< 4,
Index_house_with_cat #>= 1,
Index_house_with_cat #=< 4,
% The index of each house is unique
Index_house_with_rabbit #\= Index_house_with_lizard,
Index_house_with_rabbit #\= Index_house_with_dog,
Index_house_with_rabbit #\= Index_house_with_cat,
Index_house_with_lizard #\= Index_house_with_dog,
Index_house_with_lizard #\= Index_house_with_cat,
Index_house_with_dog #\= Index_house_with_cat,


% Now, we need to encode the constraints connecting the indices related to the color of each house with the indices related to the pet living in each house.
% Each house has one pet. Thus the green house must be the house with the rabbit, or the house with the lizard or the fouse with the dog or the house with the cat.
(Index_green_house #= Index_house_with_rabbit; Index_green_house #= Index_house_with_lizard; Index_green_house #=Index_house_with_dog; Index_green_house #= Index_house_with_cat),
% The blue house must be the house with one of the 4 pets as well.
(Index_blue_house #= Index_house_with_rabbit; Index_blue_house #= Index_house_with_lizard; Index_blue_house #=Index_house_with_dog; Index_blue_house #= Index_house_with_cat),
(Index_red_house #= Index_house_with_rabbit; Index_red_house #= Index_house_with_lizard; Index_red_house #=Index_house_with_dog; Index_red_house #= Index_house_with_cat),
(Index_yellow_house #= Index_house_with_rabbit; Index_yellow_house #= Index_house_with_lizard; Index_yellow_house #=Index_house_with_dog; Index_yellow_house #= Index_house_with_cat),


% The green and red houses are neighboring. Thus the absolute difference between their indices must be 1.
abs(Index_green_house - Index_red_house) #= 1,
% The house with the rabbit and the house with the lizard are next to each other. We don't know which house comes first, but there's 1 difference between their indices
abs(Index_house_with_lizard - Index_house_with_rabbit) #= 1,
% The blue house is placed right after the house with the dog
Index_blue_house #= Index_house_with_dog + 1,
% The cat lives in the blue house, thus the index of the blue house and the index of the house with the cat are identical.
Index_house_with_cat #= Index_blue_house,
% The red house is the first house in the street.
Index_red_house #= 1.


In the game of “1 to 9” there’s a 4x4 grid of numbers, each of the four overlapping 3x3 subgrids of this grid  must be filled with numbers 1 through 9, with each number appearing only once in each of 3x3 subgrids. The task of the player is to reveal the masked numbers, represented as X below. If we are given the bard below what is the sum of numbers that are currently masked in the first and fourth row?

7 6 X X
4 1 5 9
X 8 3 X
X 2 X 6

problem(Sum_of_masked_numbers):-
% Encoding the visible numbers in the grid
Number_row1_col1 #= 7,
Number_row1_col2 #= 6,
Number_row2_col1 #= 4,
Number_row2_col2 #= 1,
Number_row2_col3 #= 5,
Number_row2_col4 #= 9,
Number_row3_col2 #= 8,
Number_row3_col3 #= 3,
Number_row4_col2 #= 2,
Number_row4_col4 #= 6,


% Encoding the possible range of the masked numbers in the grid. Each cell in the four 3x3 subgrids must be filled with numbers 1 through 9.
Maksed_number_row1_col3 #>= 1,
Maksed_number_row1_col3 #=< 9,
Maksed_number_row1_col4 #>= 1,
Maksed_number_row1_col4 #=< 9,
Maksed_number_row3_col1 #>= 1,
Maksed_number_row3_col1 #=< 9,
Maksed_number_row3_col4 #>= 1,
Maksed_number_row3_col4 #=< 9,
Maksed_number_row4_col1 #>= 1,
Maksed_number_row4_col1 #=< 9,
Maksed_number_row4_col3 #>= 1,
Maksed_number_row4_col3 #=< 9,




% Now we must iterate trough each subgrid to encode the constraint that each number appears only once in each of 3x3 subgrids.
% Starting with the top left subgrid which includes rows 1 to 3 and columns 1 to 3 and has 2 masked numbers
% We have to encode that each masked number in this subgrid can not be equal to any of the other numbers in the subgrid
Maksed_number_row1_col3 #\= Number_row1_col1,
Maksed_number_row1_col3 #\= Number_row1_col2,
Maksed_number_row1_col3 #\= Number_row2_col1,
Maksed_number_row1_col3 #\= Number_row2_col2,
Maksed_number_row1_col3 #\= Number_row2_col3,
Maksed_number_row1_col3 #\= Maksed_number_row3_col1,
Maksed_number_row1_col3 #\= Number_row3_col2,
Maksed_number_row1_col3 #\= Number_row3_col3,


Maksed_number_row3_col1 #\= Number_row1_col1,
Maksed_number_row3_col1 #\= Number_row1_col2,
Maksed_number_row3_col1 #\= Number_row2_col1,
Maksed_number_row3_col1 #\= Number_row2_col2,
Maksed_number_row3_col1 #\= Number_row2_col3,
Maksed_number_row3_col1 #\= Number_row3_col2,
Maksed_number_row3_col1 #\= Number_row3_col3,


% Moving to the second subgrid in the top right corner which spans rows 1 to 3 and columns 2 to 4, and has 3 masked numbers
Maksed_number_row1_col3 #\= Number_row1_col2,
Maksed_number_row1_col3 #\= Maksed_number_row1_col4,
Maksed_number_row1_col3 #\= Number_row2_col2,
Maksed_number_row1_col3 #\= Number_row2_col3,
Maksed_number_row1_col3 #\= Number_row2_col4,
Maksed_number_row1_col3 #\= Number_row3_col2,
Maksed_number_row1_col3 #\= Number_row3_col3,
Maksed_number_row1_col3 #\= Maksed_number_row3_col4,


Maksed_number_row1_col4 #\= Number_row1_col2,
Maksed_number_row1_col4 #\= Number_row2_col2,
Maksed_number_row1_col4 #\= Number_row2_col3,
Maksed_number_row1_col4 #\= Number_row2_col4,
Maksed_number_row1_col4 #\= Number_row3_col2,
Maksed_number_row1_col4 #\= Number_row3_col3,
Maksed_number_row1_col4 #\= Maksed_number_row3_col4,


Maksed_number_row3_col4 #\= Number_row1_col2,
Maksed_number_row3_col4 #\= Number_row2_col2,
Maksed_number_row3_col4 #\= Number_row2_col3,
Maksed_number_row3_col4 #\= Number_row2_col4,
Maksed_number_row3_col4 #\= Number_row3_col2,
Maksed_number_row3_col4 #\= Number_row3_col3,




% The third subgrid is the bottom left one which spans rows 2 to 4 and columns 1 to 3, and has 3 masked numbers
Maksed_number_row3_col1 #\= Number_row2_col1,
Maksed_number_row3_col1 #\= Number_row2_col2,
Maksed_number_row3_col1 #\= Number_row2_col3,
Maksed_number_row3_col1 #\= Number_row3_col2,
Maksed_number_row3_col1 #\= Number_row3_col3,
Maksed_number_row3_col1 #\= Maksed_number_row4_col1,
Maksed_number_row3_col1 #\= Number_row4_col2,
Maksed_number_row3_col1 #\= Maksed_number_row4_col3,


Maksed_number_row4_col1 #\= Number_row2_col1,
Maksed_number_row4_col1 #\= Number_row2_col2,
Maksed_number_row4_col1 #\= Number_row2_col3,
Maksed_number_row4_col1 #\= Number_row3_col2,
Maksed_number_row4_col1 #\= Number_row3_col3,
Maksed_number_row4_col1 #\= Number_row4_col2,
Maksed_number_row4_col1 #\= Maksed_number_row4_col3,


Maksed_number_row4_col3 #\= Number_row2_col1,
Maksed_number_row4_col3 #\= Number_row2_col2,
Maksed_number_row4_col3 #\= Number_row2_col3,
Maksed_number_row4_col3 #\= Number_row3_col2,
Maksed_number_row4_col3 #\= Number_row3_col3,
Maksed_number_row4_col3 #\= Number_row4_col2,


% The last 3x3 subgrid is on the bottom right corner pans rowns 2 to 4 and columns 2 to 4 and has 2 masked numbers.
Maksed_number_row3_col4 #\= Number_row2_col2,
Maksed_number_row3_col4 #\= Number_row2_col3,
Maksed_number_row3_col4 #\= Number_row2_col4,
Maksed_number_row3_col4 #\= Number_row3_col2,
Maksed_number_row3_col4 #\= Number_row3_col3,
Maksed_number_row3_col4 #\= Number_row4_col2,
Maksed_number_row3_col4 #\= Maksed_number_row4_col3,
Maksed_number_row3_col4 #\= Number_row4_col4,


Maksed_number_row4_col3 #\= Number_row2_col2,
Maksed_number_row4_col3 #\= Number_row2_col3,
Maksed_number_row4_col3 #\= Number_row2_col4,
Maksed_number_row4_col3 #\= Number_row3_col2,
Maksed_number_row4_col3 #\= Number_row3_col3,
Maksed_number_row4_col3 #\= Number_row4_col2,
Maksed_number_row4_col3 #\= Number_row4_col4,


% The sum of the masked numbers in the first and fourth rows is:
Sum_of_masked_numbers #= Maksed_number_row1_col3 + Maksed_number_row1_col4 + Maksed_number_row4_col1 + Maksed_number_row4_col3.


Solve the below problem in the same format by encoding the problem as prolog equalities or inequalities step by step. Each statement must either assign a numerical value to a variable or describe the relationship between variables. Or statements must be enclosed in parentheses.

#####
"""

prolog_code_algorithmic = """:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(Answer),
    write(Answer),
    halt.

index_of_element(Element, [Element|_], 0).
index_of_element(Element, [_|Tail], Index):-
 index_of_element(Element, Tail, Index1),
 Index is Index1+1.


split_list_at(0, List, [], List).
split_list_at(N, [Head|Tail], [Head|List1], List2) :-
    N > 0,
    N1 is N - 1,
    split_list_at(N1, Tail, List1, List2).


len_list([], 0 ).
len_list([_|Xs], L):- len_list(Xs,N), L is N+1.


min(X, Y, X) :- X =< Y, !.
min(X, Y, Y) :- X > Y.


max(X, Y, X) :- X >= Y, !.
max(X, Y, Y) :- X < Y.


remove( _, [], []).
remove( R, [R|T], T).
remove( R, [H|T], [H|T2]) :- H \= R, remove( R, T, T2).


pop_last([X],X, []).
pop_last([X|Xs], Last, [X|WithoutLast]) :-
    pop_last(Xs, Last, WithoutLast).


is_in(X, [X | _]) :- !.
is_in(X, [_ | Rest]) :-  
 is_in(X, Rest).


abs(X,X) :- X >= 0, !.
abs(X,Y) :- Y is -X."""
prompt_algorithmic = """The objective is to solve the given problems by translating the problem's rules and conditions into Prolog statements. To arrive at the solution, we iterate through the provided states according to the given instructions and update the model described by the problem as necessary. 

Variable names are a brief description of the entity in the problem. Entities with different numerical values should have distinct names. 

The following helper predicates are provided

index_of_element(Element, [Element|_], 0).
index_of_element(Element, [_|Tail], Index):-
 index_of_element(Element, Tail, Index1),
 Index is Index1+1.


split_list_at(0, List, [], List).
split_list_at(N, [Head|Tail], [Head|List1], List2) :-
   N > 0,
   N1 is N - 1,
   split_list_at(N1, Tail, List1, List2).


len_list([], 0 ).
len_list([_|Xs], L):- len_list(Xs,N), L is N+1.


min(X, Y, X) :- X =< Y, !.
min(X, Y, Y) :- X > Y.


max(X, Y, X) :- X >= Y, !.
max(X, Y, Y) :- X < Y.


remove( _, [], []).
remove( R, [R|T], T).
remove( R, [H|T], [H|T2]) :- H \= R, remove( R, T, T2).


pop_last([X],X, []).
pop_last([X|Xs], Last, [X|WithoutLast]) :-
    pop_last(Xs, Last, WithoutLast).


is_in(X, [X | _]) :- !.
is_in(X, [_ | Rest]) :-  
 is_in(X, Rest).


abs(X,X) :- X >= 0, !.
abs(X,Y) :- Y is -X.


Important: All other predicates must be implemented.

In "Match the Range", three players each have four numbered cards. Players take turns placing a card from their set on top of a center stack of cards. This card must match, be one higher, or one lower than the top card in the center stack. If a player has multiple valid cards, they choose the card with the highest number. If none are valid, the player must take the bottom card from the center stack. Player 1 has [4, 1, 8, 2], Player 2 has [3, 3, 9, 5], and Player 3 has [8, 9, 7, 6]. The center stack starts with a single 5 card. The game starts with Player 1's turn, followed by Player 2 and Player 3. What's the total sum of all player cards after Player 1's third turn?

% Encoding the player's set of cards and the center stack as lists of numbers


% play_trun encodes the rules of a player playing their turn
play_turn(Player_cards, Center_stack, Player_cards_updated, Center_stack_updated):-
% Getting the top card in the center stack
Center_stack = [Top_card_center_stack|Rest],
% A valid card in player's cards is equal to, one higher or one lower than the top card of the center stack
Max_card is Top_card_center_stack + 1,
Min_card is Top_card_center_stack - 1,


% Must choose the card with the highest number if player has multiple eligible cards
% Checking for eligible cards in player's cards from the largest to the smallest
% If player has the max_eligible card, remove the card from player's list then add the card to the start of center stack
(is_in(Max_card, Player_cards) ->
remove(Max_card, Player_cards, Player_cards_updated), append(Max_card, Center_stack, Center_stack_updated);
% Elif player has a card equal to the top card, the second largest card
is_in(Top_card_center_stack, Player_cards) ->
remove(Top_card_center_stack, Player_cards, Player_cards_updated), append(Top_card_center_stack, Center_stack, Center_stack_updated);
% ELif player has the min valid card
is_in(Min_card, Player_cards) ->
remove(Min_card, Player_cards, Player_cards_updated), append(Min_card, Center_stack, Center_stack_updated);
% Otherwise the player doesn't have a valid card. Then move the last card in the center stack to the player's cards using pop_last which removes and returns the last element of a list
pop_last(Center_stack, Last_card_in_middle_stack, Center_stack_updated), append(Last_card_in_middle_stack, Player_cards, Player_cards_updated)).




problem(Sum_players_cards):-
% Encoding the initial status of the players' cards and the center stack
P1_cards = [4, 1, 8, 2],
P2_cards = [3, 3, 9, 5],
P3_cards = [8, 9, 7, 6],
Center_stack = [5],


% The game starts with Player 1's turn, followed by Player 2 and Player 3
% Updating the players' cards and the center stack after each player's turn
play_turn(P1_cards, Center_stack, P1_cards_turn1, Center_stack_P1_turn1),


play_turn(P2_cards, Center_stack_P1_turn1, P2_cards_turn1, Center_stack_P2_turn1),


play_turn(P3_cards, Center_stack_P2_turn1, P3_cards_turn1, Center_stack_P3_turn1),


% Each player has played once
play_turn(P1_cards_turn1, Center_stack_P3_turn1, P1_cards_turn2, Center_stack_P1_turn2),


play_turn(P2_cards_turn1, Center_stack_P1_turn2, P2_cards_turn2, Center_stack_P2_turn2),


play_turn(P3_cards_turn1, Center_stack_P2_turn2, P3_cards_turn2, Center_stack_P3_turn2),


% Each player has played twice
% The game ends after Player 1's third turn. Player 1 plays 3 turns, other players 2 turns
% Last turn
play_turn(P1_cards_turn2, Center_stack_P3_turn2, P1_cards_turn3, Center_stack_P1_turn3),


% To find the total sum of all cards held by players, we use sum_list to calculate sum of each player's cards
sum_list(P1_cards_turn3, P1_cards_sum_final),
sum_list(P2_cards_turn2, P2_cards_sum_final),
sum_list(P3_cards_turn2, P3_cards_sum_final),


Sum_players_cards is P1_cards_sum_final + P2_cards_sum_final + P3_cards_sum_final.


Sam starts creating a bracelet with two beads marked 'S' and 'D', her initials, with the ‘S’ bead being the first one. She uses a coin flip to decide where to add unmarked beads. If the coin lands on heads, she splits the bead chain after 'S' and if it lands on tails, she splits the chain after 'D'. She adds three beads if the length of the shorter chain is odd (one at the beginning of the first segment and two to the end of the second segment), and adds eight unmarked beads if  the length of the shorter chain is even (two at both ends of each chain segment). If she flips heads, tails, heads, heads, how many unmarked beads are between 'S' and 'D' in the end?

% Encoding the bead chain the bracelet as a list of chars, 'S' and 'D' represent the initial beads and 'U' represents the unmarked beads
% The coin flip result is encoded as 'H' for heads or 'T' for tails


% split_chain_add_beads encodes how the bead chain will be updated after a coin flip
split_chain_add_beads(Coin_flip, Bead_chain, Updated_bead_chain):-
% If the coin lands on heads, the chain is split after the S bead
(Coin_flip = 'H' ->
% Getting the index of the S bead in the chain
index_of_element('S', Bead_chain, Index_S_bead),
% We must split the chain after the S bead, the split index is 1 after the S bead
Split_index is Index_S_bead + 1,
% Using the split_list_at to get the 2 sub-lists resulting from splitting the chain
split_list_at(Split_index, Bead_chain, First_segment, Second_segment);


% Else: coin landed on tails, splitting the bead chain after the D bead
index_of_element('D', Bead_chain, Index_D_bead),
Split_index is Index_D_bead + 1,
split_list_at(Split_index, Bead_chain, First_segment, Second_segment)),


% Getting the lengths of the resulting subchains to determine the number of beads to add
len_list(First_segment, Len_first_segment),
len_list(Second_segment, Len_second_segment),
% We need to check the parity of the length of the shorter segment
min(Len_first_segment, Len_second_segment, Len_shorter_segment),


% If the length of the shorter segment is odd then we add 3 beads
(Len_shorter_segment mod 2 =:= 1 ->
% add_3_beads encodes how 3 beads are added, implemented below
add_3_beads(First_segment, Second_segment, Updated_bead_chain);
% Otherwise: the length is even and we add 8 beads. add_8_beads is implemented below
add_8_beads(First_segment, Second_segment, Updated_bead_chain)).


% add_3_beads encodes how 3 unmarked beads are added to the chain segments
add_3_beads(First_segment, Second_segment, Updated_bead_chain):-
% 1 unmarked bead, U, is added to the start of the first chain segment
append(['U'], First_segment, First_segment_added_to_front),
% 2 unmarked beads are added to the end of the second segment
append(Second_segment, ['U', 'U'], Second_segment_added_to_end),
% Reconnecting the two bead segments to get the final updated bead chain
append(First_segment_added_to_front, Second_segment_added_to_end, Updated_bead_chain).


% add_8_beads encodes the addition of 8 beads to the chain segments
add_8_beads(First_segment, Second_segment, Updated_bead_chain):-
% 2 unmarked beads are added to the beginning and end of each chain
% First add the beads to the start of the first segment
append(['U', 'U'], First_segment, First_segment_added_to_front),
% Add 2 beads to the end of the first segment
append(First_segment_added_to_front, ['U', 'U'], First_segment_added_to_front_end),
% Same for the second segment
append(['U', 'U'], Second_segment, Second_segment_added_to_front),
append(Second_segment_added_to_front, ['U', 'U'], Second_segment_added_to_front_end),
% Finally reconnecting the two updated chain segments
append(First_segment_added_to_front_end, Second_segment_added_to_front_end, Updated_bead_chain).




problem(Num_beads_between_S_D):-
% Encoding the initial state of the bead chain
% The two first beads are the marked ones, with S being the first bead
Initial_bead_chain = ['S', 'D'],


% Sam gets heads, tails, heads, and heads from flipping a coin in four rounds of adding beads
split_chain_add_beads('H', Initial_bead_chain, Bead_chain_round1),
split_chain_add_beads('T', Bead_chain_round1, Bead_chain_round2),
split_chain_add_beads('H', Bead_chain_round2, Bead_chain_round3),
split_chain_add_beads('H', Bead_chain_round3, Bead_chain_round4),


% To calculate the number of unmarked beads that end up between S and D, we need the indices of the marked beads
index_of_element('S', Bead_chain_round4, Index_S_bead),
index_of_element('D', Bead_chain_round4, Index_D_bead),


% The number of beads between the marked ones is the index of D bead, placed later in the chain, minus the index of S bead minus 1
Num_beads_between_S_D is Index_D_bead - Index_S_bead - 1.


There’s a cinema with 12 seats organized in 3 rows and 4 columns. Due to covid there’s a policy that a seat can be filled only if none of the seats right next to it in the same column or the same row are not filled. If we place a person in the seat in the second column of the first row and then start to fill the seats left to right, row by row, starting row with 1, how many people can be seated in the cinema in total?

% Encoding an empty seat as 0 and a filled seat as 1


% seat_check encodes the conditions under which a seat can be seated
seat_check(Neighbouring_seats, Prev_seat_status, Final_seat_status, Prev_Num_filled, Updated_Num_filled):-
% If any of the neighboring seats are filled, then the seat can not be filled  
(is_in(1, Neighbouring_seats) ->
Final_seat_status is Prev_seat_status, Updated_Num_filled is Prev_Num_filled;
% Else: if all neighboring seats are empty, then change the status of the seat to be filled and increment the number of seats filled by 1
Final_seat_status is 1, Updated_Num_filled is Prev_Num_filled + 1).


problem(Num_filled_final):-
% Encoding the initial status of all seats as empty initially
% There are 12 seats in the cinema, 3 rows and 4 columns
Seat_r1_c1 is 0,
Seat_r1_c2 is 0,
Seat_r1_c3 is 0,
Seat_r1_c4 is 0,
Seat_r2_c1 is 0,
Seat_r2_c2 is 0,
Seat_r2_c3 is 0,
Seat_r2_c4 is 0,
Seat_r3_c1 is 0,
Seat_r3_c2 is 0,
Seat_r3_c3 is 0,
Seat_r3_c4 is 0,


% A person is seated in row 1, second column
Seat_r1_c2_updated is 1,
Num_filled_initial is 1,


% Iterating through the seats left to right, row by row, starting with row 1, to check if the seat can be filled
% A list of all neighboring seats, seats in the same row or column, must be constructed for each target seat to pass to seat_check
% If the status of a seat is updated, must pass the updated status
% row 1 col 1 seat is a corner seat with 2 neighboring seats, one to the right one below
Seat_r1_c1_neighbouring = [Seat_r1_c2_updated, Seat_r2_c1],
seat_check(Seat_r1_c1_neighbouring, Seat_r1_c1, Seat_r1_c1_updated, Num_filled_initial, Num_filled_after_r1_c1),


% We were told seat in row 1 col 2 is filled


% Seat in row 1 col 3 is an edge seat with 3 neighboring seats, one to right, below, and to the left
Seat_r1_c3_neighbouring = [Seat_r1_c4, Seat_r2_c3, Seat_r1_c2_updated],
seat_check(Seat_r1_c3_neighbouring, Seat_r1_c3, Seat_r1_c3_updated, Num_filled_after_r1_c1, Num_filled_after_r1_c3),


% Seat in row 1 col 4 is a corner seat with 2 neighboring seats, one below and one to left
Seat_r1_c4_neighbouring = [Seat_r2_c4, Seat_r1_c3_updated],
seat_check(Seat_r1_c4_neighbouring, Seat_r1_c4, Seat_r1_c4_updated, Num_filled_after_r1_c3, Num_filled_after_r1_c4),


% The leftmost seat in row 2 has 3 neighboring seats, one above to the right and below it
Seat_r2_c1_neighbouring = [Seat_r1_c1_updated, Seat_r2_c2, Seat_r3_c1],
seat_check(Seat_r2_c1_neighbouring, Seat_r2_c1, Seat_r2_c1_updated, Num_filled_after_r1_c4, Num_filled_after_r2_c1),


% Seat in row 2 col 2 is not an edge or corner seat and has 4 neighboring seats
Seat_r2_c2_neighbouring = [Seat_r1_c2_updated, Seat_r2_c3, Seat_r3_c2, Seat_r2_c1_updated],
seat_check(Seat_r2_c2_neighbouring, Seat_r2_c2, Seat_r2_c2_updated, Num_filled_after_r2_c1, Num_filled_after_r2_c2),


% Similarly seat in row 2 col 3 has 4 neighboring seats
Seat_r2_c3_neighbouring = [Seat_r1_c3_updated, Seat_r2_c4, Seat_r3_c3, Seat_r2_c2_updated],
seat_check(Seat_r2_c3_neighbouring, Seat_r2_c3, Seat_r2_c3_updated, Num_filled_after_r2_c2, Num_filled_after_r2_c3),


% The rightmost seat in the second row has 3 neighboring seats, one above one below and to the left
Seat_r2_c4_neighbouring = [Seat_r1_c4_updated, Seat_r3_c4, Seat_r2_c3_updated],
seat_check(Seat_r2_c4_neighbouring, Seat_r2_c4, Seat_r2_c4_updated, Num_filled_after_r2_c3, Num_filled_after_r2_c4),


% The leftmost seat in the the last row is a corner seat with 2 neighboring seats one above and to the right
Seat_r3_c1_neighbouring = [Seat_r2_c1_updated, Seat_r3_c2],
seat_check(Seat_r3_c1_neighbouring, Seat_r3_c1, Seat_r3_c1_updated, Num_filled_after_r2_c4, Num_filled_after_r3_c1),


% Seat in row 3 col 2 is an edge seat with 3 neighboring seats, to above to the right and to the left
Seat_r3_c2_neighbouring = [Seat_r2_c2_updated, Seat_r3_c3, Seat_r3_c1_updated],
seat_check(Seat_r3_c2_neighbouring, Seat_r3_c2, Seat_r3_c2_updated, Num_filled_after_r3_c1, Num_filled_after_r3_c2),


% Similarly seat in row 3 col 3 has 3 neighboring seats, one above to the right and to the left
Seat_r3_c3_neighbouring = [Seat_r2_c3_updated, Seat_r3_c4, Seat_r3_c2_updated],
seat_check(Seat_r3_c3_neighbouring, Seat_r3_c3, Seat_r3_c3_updated, Num_filled_after_r3_c2, Num_filled_after_r3_c3),


% The last seat in the bottom right corner has 2 neighboring seats, one above it and one to the left
Seat_r3_c4_neighbouring = [Seat_r2_c4_updated, Seat_r3_c3_updated],
seat_check(Seat_r3_c4_neighbouring, Seat_r3_c4, Seat_r3_c4_updated, Num_filled_after_r3_c3, Num_filled_final).

In the game "Twist It", players can push a rod right, left, or not at all. If both players push the rod in the same direction, it spins 60 degrees in that direction. If one player pushes the rod and the other doesn't, it spins 40 degrees in the direction of the push. If neither push, it stays still. If the players push in opposite directions, the rod bends 20 degrees total symmetrically at the center. The rod starts parallel to the x-axis. In rounds 1-5, Player 1's moves are: no push, right, no push, right, left. Player 2 rolls a dice and pushes left if it lands on 5 or a number divisible by 3, otherwise right. His rolls are 2, 6, 5, 3, 5. What's the total absolute (ignoring the direction) angle change at each rod end?

% Encoding the rotation of the rod to the right as 1 and to the left as -1. Encoding no push as 0.


% push_rod encodes how the angle of each player's end of the rod changes based on the two players' actions
push_rod(P1_action, P2_action, P1_angle_prev_round, P2_angle_prev_round, P1_angle_now, P2_angle_now):-
% Each player has 3 action choices. Thus there are 9 combinations of actions that can change the angle of the rod's ends.
% Iterating through all possible action combinations to update the rod's angles based on the given rules
% If both players push right
((P1_action =:= 1, P2_action =:= 1) ->
% Then the rod rotates around the center without bending, each end of the rod rotates by 60 degrees
P1_angle_now is P1_angle_prev_round + (1 * 60),
P2_angle_now is P2_angle_prev_round + (1 * 60);
% If both players push left
(P1_action =:= -1, P2_action =:= -1) ->
P1_angle_now is P1_angle_prev_round + (-1 * 60),
P2_angle_now is P2_angle_prev_round + (-1 * 60);


% If one player pushes right and the other doesn't push then the rod rotates by 40 degrees to the right of each player
((P1_action =:= 0, P2_action =:= 1) ; (P1_action =:= 1, P2_action =:= 0)) ->
P1_angle_now is P1_angle_prev_round + (1 * 40),
P2_angle_now is P2_angle_prev_round + (1 * 40);


% If one player pushes their end to left and the other doesn't push
((P1_action =:= 0, P2_action =:= -1); ((P1_action =:= -1, P2_action =:= 0))) ->
P1_angle_now is P1_angle_prev_round + (-1 * 40),
P2_angle_now is P2_angle_prev_round + (-1 * 40);


% If the player 1 pushes right and player 2 pushes left
(P1_action =:= 1, P2_action =:= -1) ->
% Then the rod bends by 20 degrees symmetrically at the center,  each end of the rod will move 10 degrees in opposite directions as the rod bends
P1_angle_now is P1_angle_prev_round + (1 * 10),
P2_angle_now is P2_angle_prev_round + (-1 * 10);
% If players push in opposite directions, with player 1 pushing the rod to the left
(P1_action =:= -1, P2_action =:= 1) ->
% The rod bends again by 20 degrees total, each end rotating by 10 degrees
P1_angle_now is P1_angle_prev_round + (-1 * 10),
P2_angle_now is P2_angle_prev_round + (1 * 10);


% If neither player chooses to push the rod
(P1_action =:= 0, P2_action =:= 0) ->
% The angle of the rod's ends do not change
P1_angle_now is P1_angle_prev_round,
P2_angle_now is P2_angle_prev_round).


% player2_action determines Player 2's rod push based on the dice roll result
player2_action(Dice_roll, P2_action):-
% If the dice lands on 5 or a number divisible by 3, player 2 pushes the rod to the left
((Dice_roll =:= 5; Dice_roll mod 3 =:= 0) ->
P2_action is -1;
% Otherwise he will choose to push right
P2_action is 1).


problem(Sum_abs_P1_angle_P2_angle):-
% Encoding the angle of the rod's ends at the starting position.
P1_angle_initial is 0,
P2_angle_initial is 0,


% Now we iterate through the actions taken by the players in rounds 1 to 5
% player 1: no push, dice: 2
player2_action(2, P2_action_round1),
push_rod(0, P2_action_round1, P1_angle_initial, P2_angle_initial, P1_angle_round1, P2_angle_round1),


% player 1: right, dice: 6
player2_action(6, P2_action_round2),
push_rod(1, P2_action_round2, P1_angle_round1, P2_angle_round1, P1_angle_round2, P2_angle_round2),


% player 1: no push, dice: 5
player2_action(5, P2_action_round3),
push_rod(0, P2_action_round3, P1_angle_round2, P2_angle_round2, P1_angle_round3, P2_angle_round3),


% player 1: right, dice: 3
player2_action(3, P2_action_round4),
push_rod(1, P2_action_round4, P1_angle_round3, P2_angle_round3, P1_angle_round4, P2_angle_round4),


% Lastly player 1: left, dice: 5
player2_action(5, P2_action_round5),
push_rod(-1, P2_action_round5, P1_angle_round4, P2_angle_round4, P1_angle_round5, P2_angle_round5),


% Calculating the absolute values of the angles
abs(P1_angle_round5, Abs_P1_angle_final),
abs(P2_angle_round5, Abs_P2_angle_final),
Sum_abs_P1_angle_P2_angle is Abs_P1_angle_final + Abs_P2_angle_final.

A 100m x 100m field has 4 wind blowers at the midpoint of each edge, facing the center. The blowers on opposite sides neutralize each other. There’s an object placed at the field’s center which moves at 2 m/s in the Y direction when the north or south blower is activated and 3m/s in the X direction when the east or west one is activated. At time 0s (s indicating seconds), the north and south blowers are switched on. At 10s, the south blower is turned off and the east one is turned on. At 25s, the north blower is switched off.  At 30s, the east wind blower is switched off and the south one is switched on for a second time. The west blower is activated from 30s to 55s. The south blower is turned off at 70s. What is the object's distance from its starting position at 71s, as a rounded number?

% Encoding the north wind blower as 'N', the south one as 'S', the east one as 'E', and the west one as 'W'


% move_object encodes how the position of the object changes in the x and y direction when a single wind blower is activated for a given number of seconds  
move_object(Windblower, Activated_seconds, X_position_prev, Y_position_prev, X_position_now, Y_position_now):-
% If the north blower is activated, then the object moves in the negative y direction with speed 2m/s
(Windblower = 'N' ->
X_position_now is X_position_prev,
Y_position_now is Y_position_prev - (2 * Activated_seconds);
% If the south one is on, the object moves upwards in the positive Y direction
Windblower = 'S' ->
X_position_now is X_position_prev,
Y_position_now is Y_position_prev + (2 * Activated_seconds);
% The east blower moves the object in the negative X direction with speed 3m/s
Windblower = 'E' ->
X_position_now is X_position_prev - (3 * Activated_seconds),
Y_position_now is Y_position_prev;
% The west one pushes the object to the right with speed 3m/s
Windblower = 'W' ->
X_position_now is X_position_prev + (3 * Activated_seconds),
Y_position_now is Y_position_prev).


problem(Distance_rounded):-
% Encoding the switch-on and switch-off times of each blower to determine the total time each one influences the object's position
North_on = 0,
South_on = 0,


South_off = 10,
East_on = 10,


North_off = 25,
East_off = 30,
South_second_on = 30,


West_on = 30,
West_off = 55,


South_second_off = 70,


% The total duration each blower is on is calculated by subtracting the turn-on time from the turn-off time
North_total_activated = North_off - North_on,
% The south blower is the only one that was activated twice
South_total_activated = (South_off - South_on) + (South_second_off - South_second_on),
East_total_activated = East_off - East_on,
West_total_activated = West_off - West_on,


% Encoding the starting position of the object at the field's center
X_position_initial is 0,
Y_position_initial is 0,


% Updating the object's location by iterating through each wind blower and calculating the blower's impact on the object's position
move_object('N', North_total_activated, X_position_initial, Y_position_initial, X_position_north_updated, Y_position_north_updated),


move_object('S', South_total_activated, X_position_north_updated, Y_position_north_updated, X_position_north_south_updated, Y_position_north_south_updated),


move_object('E', East_total_activated, X_position_north_south_updated, Y_position_north_south_updated, X_position_north_south_east_updated, Y_position_north_south_east_updated),


move_object('W', West_total_activated, X_position_north_south_east_updated, Y_position_north_south_east_updated, X_position_final, Y_position_final),


% Calculating the distance of the object from its starting position using the Pythagoras theorem
Distance is sqrt((X_position_final ^ 2) + (Y_position_final ^ 2)),


% Getting the distance as a rounded number
Distance_rounded is round(Distance).

Solve the problem below by encoding the rules of the problem as Prolog predicates and then iterating through the provided instructions/states step by step. 

#####
"""

def get_oai_reponse(final_prompt, model, temp, max_tokens):
    if model == "GPT4":
        model = "gpt-4"
    elif model == "GPT3.5":
        model = "gpt-3.5-turbo"
    response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": final_prompt
        }
    ],
    temperature=temp,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response = response.choices[0].message.content
    
    return response
        

def get_llm_solution(problem, model, temp, type, max_tokens):
    if type == "MWP":
        prompt_examples = prompt_mwp
    elif type == "CS":
        prompt_examples = prompt_constraint
    else:
        prompt_examples = prompt_algorithmic
    
    final_prompt = prompt_examples.replace("#####", '"' + problem + '"')
    
    # Try to get openai's response 5 times, then give up
    tries = 6
    while tries >= 0:
        try:
            response = get_oai_reponse(final_prompt, model, temp, max_tokens)
            break
        except Exception as e:
            if tries == 0:
                raise 
            else:
                # Wait a few seconds before retrying 
                time.sleep(6) 
                if "maximum context length" in str(e):
                    num_tokens_context = re.findall(r'-?\b\d+\b', str(e))[3]
                    max_tokens = 8192 - int(num_tokens_context)
                tries -= 1
                continue
    
    pl_file = None
    try:
        if type == "MWP":
            code_begin_index = response.index("problem(")
            code_end_index = response.index("}.")
            code_llm = response[code_begin_index:code_end_index + 2]
            code = prolog_code_mwp + code_llm
            pl_file = "result_mwp.pl"
        elif type == "CS":
            code_begin_index = response.index("problem(")
            code_llm = response[code_begin_index:]
            code = prolog_code_constraint + code_llm
            pl_file = "result_constraint.pl"
        else:
            code_begin_index = response.index("%")
            code_llm = response[code_begin_index:]
            code = prolog_code_algorithmic + code_llm
            pl_file = "result_algorithmic.pl"

        f = open(pl_file, "w")
        f.write(code)
        f.close()    
        correct_format = True

    except ValueError:
        correct_format = False
        code_llm = response
        
    return correct_format, code_llm, pl_file
    

def run_llm_prolog_result(pl_file):
    kill = lambda process: process.kill()
    cmd = ['swipl', pl_file]
    ping = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cancelled  = False
    #kill prolog if it takes more than 2 secs, would be due to failed initialization, ie the problem did not return a result
    my_timer = Timer(2, kill, [ping])
    try:
        my_timer.start()
        stdout, stderr = ping.communicate()
    finally:
        my_timer.cancel()
        if stderr.decode('ascii'):
            cancelled = True
        
    prolog_solution = stdout.decode('ascii')
    return prolog_solution, cancelled
    
     
def final_record(log_file, incorrect_format, incorrect_ids, max_id, type, model,
                 reached_max_tries, reached_max_tries_ids, repeat_max,
                 corrected_after_multiple_try, incorrect_after_multiple_try, 
                 temp_at_max, total_number_calls, count_correct, VE_correct_count):
    #log problems that were not solved due to incorrect formatting
    f = open(log_file, "a")   
    f.write("\n" + "-"*50 + "\n")
    f.write("model:"+ "\n")
    f.write(model + "\n")
    
    f.write("\n" + "-"*50 + "\n")
    f.write("nlr_dataste problem type:"+ "\n")
    f.write(type + "\n")
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect formats"+ "\n")
    for id in incorrect_format:
        f.write(str(id))
        f.write(str(incorrect_format[id]) + "\n")
        
    #ids of problems that got incorrect solutions
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect ids" + "\n")
    f.write(str(incorrect_ids))
    
    #number of times prolog still didn't run after repeat max calls
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("Number of max tries"+ "\n")
    f.write(str(repeat_max))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Number of times prolog didn't run after repeat max tries"+ "\n")
    f.write(str(reached_max_tries))
   
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem ids that prolog didn't run after max tries"+ "\n")
    f.write(str(reached_max_tries_ids))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem number that got correct solution after many tries"+ "\n")
    f.write(str(corrected_after_multiple_try))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem number with incorrect solution after many tries"+ "\n")
    f.write(str(incorrect_after_multiple_try))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Tempreture at the max repeat call number"+ "\n")
    f.write(str(temp_at_max))
    

    #total number of calls to LLM
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("total number of calls to LLM"+ "\n")
    f.write(str(total_number_calls))

    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("stats"+ "\n")
    f.write(str(count_correct) + " out of " + str(max_id) + " is correct.")
    
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("stats"+ "\n")
    f.write(f"The count of correct solutions for {type} problmes out of 5 problems for each variable entanglement leve is: \n {VE_correct_count}")
    f.close()

   
   
def record(id, log_file, prolog_solution, problem, code_llm, repeated = None, corrected = False):
    f = open(log_file, "a")
    f.write("ID: " + str(id) + "\n" + str(problem) + "\n")
    if repeated:
        f.write("repeated: " + str(repeated) + "\n")
    else:
        f.write("NOT repeated \n")
    if corrected:
        f.write("Corrected!!!!!" + "\n")
    f.write(str(code_llm)+ "\n")
    f.write("prolog run result: " + str(prolog_solution) + " problem answer: " + str(problem["answer"]) + "\n\n\n\n")
    f.close()
    

    
def main():    
    parser = argparse.ArgumentParser(description='This script evaluates GPT4 or GPT3.5 Turbo on a subset of the NLR dataset with 0-4 entangled variables in each problem/state, using our prolog augmented neurosymbolic approach.')
    parser.add_argument('OAI_key', type=str, help='Your OpenAI API key.')
    parser.add_argument('model', type=str, choices=['GPT4', 'GPT3.5'], help='Name of the model you want to do inference on, either GPT4 or GPT3.5.')
    parser.add_argument('subset', type=str, choices=['MWP', 'AI'], help='Name of the subset of NLR dataset you want to do inference on. MWP stands for math word problems, CS is constraint satisfaction problems, AI is algorithmic instructions.')
    parser.add_argument('--print', type=str, choices=['True', 'False'], default='True', nargs='?', help='If set to True, the script will print a statemnt about the result of each call to the model')

    args = parser.parse_args()
    
    global client
    client = OpenAI(
    api_key=args.OAI_key,
    )
    model = args.model
    type = args.subset
    global print_progress
    print_progress = args.print

    log_file = f"{model}_multiTry_{type}_prolog_var_entanglement.txt"
    repeat_max = 50
    total_number_calls = 0
    reached_max_tries = 0
    reached_max_tries_ids = []
    corrected_after_multiple_try = 0
    incorrect_after_multiple_try = 0
    temp_at_max = 0.4
    
    problems = get_problems(type) 
    count_correct = 0
    incorrect_format = {}
    incorrect_ids = []
    
    if type == "MWP":
        max_tokens = 3000
        VE_key =  "Number of entangled variables"
    elif type == "AI":
        max_tokens = 1400
        VE_key = "Number of entangled variables in each state"
            
    min_id = min(problems.keys())
    num_problmes = len(problems)
    
    VE_correct_count = Counter()
    
    for id, problem in problems.items():
        if id != 24 and id!= 28:
            continue
                
        repeated = 0
        #repeat if prolog didn't run
        while True:
            repeat = False
            #repeated 0 -> temp 0, repeated 50 -> temp 0.4
            temp = (temp_at_max * repeated)/repeat_max
            correct_format, code_llm, pl_file = get_llm_solution(problem["statement"], model, temp, type, max_tokens)
            total_number_calls += 1
            
            if correct_format:
                prolog_solution, cancelled = run_llm_prolog_result(pl_file)
                if cancelled or "_" in prolog_solution or "r" in prolog_solution or "?" in prolog_solution:
                    repeat = True
                    
            else:
                prolog_solution = None
                incorrect_format[id] = code_llm
                repeat = True

            #if format was correct and prolog ran then break
            if not repeat:
                break
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)
                if print_progress:
                    print("repeated: " + str(repeated) + " llm: " + str(prolog_solution))

                repeated += 1
                if repeated > repeat_max: 
                    reached_max_tries += 1
                    if print_progress:
                        print("reached max tries, total number of failed attmepts to run prolog: " + str(reached_max_tries))
                    reached_max_tries_ids.append(id)
                    break
                
        #prolog ran, check answer
        if repeated <= repeat_max and prolog_solution and round(float(prolog_solution), 2) == problem["answer"]:
            count_correct += 1
            VE_correct_count[problem[VE_key]] += 1
            if print_progress:
                print(str(count_correct) + " out of " + str(id - min_id + 1) + " is correct.")
            
            if repeated > 0:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated, corrected = True)
                corrected_after_multiple_try += 1
                if print_progress:
                    print("corrected after more than 1 try, total corected after multiple tries count: " + str(corrected_after_multiple_try))
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)


        else:
            if print_progress:
                print("incorrect llm_solution: " + str(prolog_solution) + "  actual_solution " + str(problem["answer"]))
            incorrect_ids.append(id)
            record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)

            if repeated > 0:
                incorrect_after_multiple_try += 1
                if print_progress:
                    print("incorrect after more than 1 try, total incorrect after multiple tries count: " + str(incorrect_after_multiple_try))

    final_record(log_file, incorrect_format, incorrect_ids, len(problems),type, model,
                reached_max_tries, reached_max_tries_ids, repeat_max,
                 corrected_after_multiple_try, incorrect_after_multiple_try, 
                 temp_at_max, total_number_calls, count_correct, VE_correct_count)
    
    print(f"The count of correct solutions for {type} problmes out of 5 problems for each variable entanglement level is {VE_correct_count}")

     
     


main()


    
