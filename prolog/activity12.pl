faculty(xavier).
faculty(brandi).
student(harvey).
student(ariel).
student(charlie).
student(dan).
visitor(laverne).
visitor(ramon).
% advisor(X, Y) :- faculty(X), student(Y).
advisor(xavier, dan) :- faculty(xavier), student(dan).
advisor(brandi, ariel) :- faculty(brandi), student(ariel).
lab_access(X,business) :- faculty(X); student(X).
lab_access(X,weekend) :- faculty(X); advisor(Y, X).
