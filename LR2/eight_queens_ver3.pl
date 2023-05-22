% Define the eight queens problem with coordinates as output
queens(N, Solution) :-
    length(Solution, N),
    numlist(1, N, Rows),
    permutation(Rows, Columns),
    coordinates(Columns, Rows, Solution),
    safe(Solution).

% Define the safe/1 predicate to check if queens are safe from each other
safe([]).
safe([row(Column, Row)|Queens]) :-
    safe(Queens, 1, Column, Row).

safe([], _, _, _).
safe([row(OtherColumn, OtherRow)|Queens], Offset, Column, Row) :-
    Column =\= OtherColumn,
    Column + Offset =\= OtherColumn + OtherRow,
    Column - Offset =\= OtherColumn - OtherRow,
    NewOffset is Offset + 1,
    safe(Queens, NewOffset, Column, Row).

% Define the coordinates/3 predicate to convert columns and rows into coordinates
coordinates([], [], []).
coordinates([Column|Columns], [Row|Rows], [row(Column, Row)|Coordinates]) :-
    coordinates(Columns, Rows, Coordinates).

% Define the solution predicate to find and print one solution at a time
find_solution(N) :-
    queens(N, Solution),
    print_solution(Solution),
    !.

% Define the predicate to print a solution
print_solution([]).
print_solution([row(Column, Row)|Queens]) :-
    write('('), write(Column), write(', '), write(Row), write(') '),
    print_solution(Queens).
