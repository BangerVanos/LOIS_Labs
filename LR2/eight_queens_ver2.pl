% Define the eight queens problem
queens(N, Solution) :-
    length(Solution, N),
    numlist(1, N, Rows),
    permutation(Rows, Solution),
    safe(Solution).

% Define the safe/1 predicate to check if queens are safe from each other
safe([]).
safe([Queen|Queens]) :-
    safe(Queens, 1, Queen).

safe([], _, _).
safe([OtherQueen|Queens], Offset, Queen) :-
    Queen =\= OtherQueen,
    Queen + Offset =\= OtherQueen,
    Queen - Offset =\= OtherQueen,
    NewOffset is Offset + 1,
    safe(Queens, NewOffset, Queen).

% Define the solution predicate to find all solutions
find_all_solutions(N, Solutions) :-
    findall(Solution, queens(N, Solution), Solutions).
