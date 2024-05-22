:- use_module(library(clpq)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(Answer),
    write(Answer),
    halt.

problem(Sum_birds_in_garden):-
{% There are 16 birds on tree Z and 24 birds in tree Y.
Birds_in_tree_Z = 16,
Birds_in_tree_Y = 24,


% The birds in tree X tell other birds that if 9 birds from tree Z come to their tree, then the new population of their tree would be equal to the population of birds in Y.
Birds_in_tree_X_after_9_birds_from_Z = Birds_in_tree_Y,
Birds_in_tree_X = Birds_in_tree_X_after_9_birds_from_Z - 9,


% The sum of the number of birds in the garden is the sum of the birds in tree X, Y, and Z.
Sum_birds_in_garden = Birds_in_tree_X + Birds_in_tree_Y + Birds_in_tree_Z}.