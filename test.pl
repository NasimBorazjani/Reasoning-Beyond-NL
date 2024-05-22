:- use_module(library(clpfd)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(A, B, C, D, E).

problem(Andy_birth_date, Blake_birth_date, Conor_birth_date, Emma_birth_date, Danny_birth_date):-
% Birthdays of Andy, Blake, Conor, Danny, and Emma are on or between 11th and 15th of a month.
Andy_birth_date #>= 11,
Andy_birth_date #=< 15,
Blake_birth_date #>= 11,
Blake_birth_date #=< 15,
Conor_birth_date #>= 11,
Conor_birth_date #=< 15,
Danny_birth_date #>= 11,
Danny_birth_date #=< 15,
Emma_birth_date #>= 11,
Emma_birth_date #=< 15,

% No two people's birthdays are on the same date.
Andy_birth_date #\= Blake_birth_date,
Andy_birth_date #\= Conor_birth_date,
Andy_birth_date #\= Danny_birth_date,
Andy_birth_date #\= Emma_birth_date,
Blake_birth_date #\= Conor_birth_date,
Blake_birth_date #\= Danny_birth_date,
Blake_birth_date #\= Emma_birth_date,
Conor_birth_date #\= Danny_birth_date,
Conor_birth_date #\= Emma_birth_date,
Danny_birth_date #\= Emma_birth_date,

% Emma was born 2 days before Andy
Emma_birth_date #= Andy_birth_date - 2,

% Blake was born 2 days before Danny
Blake_birth_date #= Danny_birth_date - 2,

% Emma’s birthday is before Blake’s birthday
Emma_birth_date #< Blake_birth_date,

% The number of days between Danny’s birthday and Conor’s birthday is less than the number of days between Blake’s and Connor’s birthday
abs(Danny_birth_date - Conor_birth_date) #< abs(Blake_birth_date - Conor_birth_date),

% Connor is born after Danny
Conor_birth_date #> Danny_birth_date,

% Andy's birth date minus Blake’s birth date plus Conor’s birth date
Andy_birth_date_minus_Blake_birth_date_plus_Danny_birth_date #= Andy_birth_date - Blake_birth_date + Danny_birth_date.
