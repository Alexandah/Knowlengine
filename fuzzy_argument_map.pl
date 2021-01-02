%Declare graph here! ~~~~~~~~~~~~~~~~~~~~~
j([b,k],c).
j(x,y).
j(y,z).
j(c,z).
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%Justification edge weights here! ~~~~~~~~
w(j(x,y), 0.5).
w(j([b,k],c), 0.7).
w(j([y,c],z), 1).
w(j(y,z),1).
w(j(c,z),1).
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%Defines the incoming edges of a given node
js_into(X, Js) :-
    findall(j(P,X), j(P,X), Js).

%Declare fuzzy-truth values here! ~~~~~~~~
verid(b,1).
verid(k,1).
verid(x,1).
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%and-out justification
verid(j(In, Out), X) :-
    is_list(In),
    findall(N, (member(Z,In), verid(Z,N)), Vs),
    min_list(Vs, And),
    w(j(In, Out), W),
    X is And*W.

%direct-out justification
verid(j(In, Out), X) :-
    not(is_list(In)),
    verid(In, Y),
    w(j(In, Out), W),
    X is Y*W.

%if a node does not have an immediate veridicality,
%its verid. is defined by the max of the edge verids. 
%coming into it. This implements or.
verid(Node, X) :-
    js_into(Node, Js),
    findall(N, (member(Y, Js), verid(Y,N)), Vs),
    max_list(Vs, Or),
    X is Or.

    

    
    
    

