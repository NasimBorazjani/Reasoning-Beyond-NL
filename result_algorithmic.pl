:- initialization main.

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
abs(X,Y) :- Y is -X.% Encoding the beads as a list of numbers, with the scratched bead represented as 1 and the other beads as 0


% add_beads_reverse_segments encodes the process of adding beads to the chain segments and reversing their order
add_beads_reverse_segments(Split_index, Bead_chain, Updated_bead_chain):-
% Splitting the bead chain at the given index
split_list_at(Split_index, Bead_chain, First_segment, Second_segment),
% Adding a bead to the front and back of each segment
append([0], First_segment, First_segment_added_to_front),
append(First_segment_added_to_front, [0], First_segment_added_to_front_back),
append([0], Second_segment, Second_segment_added_to_front),
append(Second_segment_added_to_front, [0], Second_segment_added_to_front_back),
% Reversing the order of the two segments before reconnecting them
append(Second_segment_added_to_front_back, First_segment_added_to_front_back, Updated_bead_chain).


problem(Scratched_bead_position):-
% Encoding the initial state of the bead chain
% The middle bead is the only one with a scratch
Initial_bead_chain = [0, 0, 1, 0, 0],


% Sarah rolls 2, 2, 7, 4 in four rounds of playing this game
% Updating the bead chain after each round
add_beads_reverse_segments(2, Initial_bead_chain, Bead_chain_round1),
add_beads_reverse_segments(2, Bead_chain_round1, Bead_chain_round2),
add_beads_reverse_segments(7, Bead_chain_round2, Bead_chain_round3),
add_beads_reverse_segments(4, Bead_chain_round3, Bead_chain_round4),


% To find the position of the scratched bead in the final bead chain, we use index_of_element
index_of_element(1, Bead_chain_round4, Scratched_bead_position).