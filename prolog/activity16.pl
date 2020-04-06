student(grace).
student(omar).
student(pablo).
student(molly).
student(anthony).
faculty(david).
major(grace, cs).
major(omar, cs).
major(pablo, chemistry).
major(molly, history).
major(anthony, biology).
cs3210(grace).
cs3600(grace).
cs3600(omar).
che3190(pablo).
che3200(pablo).
bio1080(molly).
bio1080(anthony).

hirable(X) :- student(X),((major(X, cs),cs3210(X));(che3190(X));(major(X, biology)).
