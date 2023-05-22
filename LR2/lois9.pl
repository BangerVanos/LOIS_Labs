% Лабораторная работа №3 по дисциплине ЛОИС
% Выполнена студентом группы 921702 БГУИР Ляпкин Дмитрий Андреевич
% 07.05.2022
% Файл содержит описание предикатов, позволяющих расставить на шахматной доске 8 ферзей так,
% чтобы ни один ферзь не находился под боем другого ферзя.

% будем искать решение как набор 8 координат вида X/Y каждого из ферзей
% при этом понятно, что поскольку все вертикали так или иначе будут заняты
% задача сводится к отысканию соответствующих Y - координат

get(S):-
    find(S),
    write(S).

% доска без ферзей очевидно является решением
find([]).

% доска является решением, если является решением её под-доска,
% а первый ферзь не бьет ферзей на этой под-доске.
find([X/Y | Oth]) :-
    find(Oth),
    member(Y, [1, 2, 3, 4, 5, 6, 7, 8]),
    notBeat(X/Y, Oth).

% очевидно что ферзь с любыми координатами не бьет ферзей из пустого массива,
% поскольку просто некого бить

notBeat(_, []).

% ферзь не бьет набор ерзей если он не бьет первого ферзя из набора
% и не бьет остальных ферзей набора
notBeat(X/Y, [X1/Y1 | Oth]) :-
    Y =\= Y1,
    Y1-Y =\= X1-X,
    Y1-Y =\= X-X1,
    notBeat(X/Y, Oth).
