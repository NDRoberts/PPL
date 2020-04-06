% Knowledge Base
mount(everest).
mount(aconcagua).
mount(mckinley).
mount(kilimanjaro).
mount(elbrus).
mount(vinson).
mount(puncak_jaya).

peak(everest, 29029).
peak(aconcagua, 22841).
peak(mckinley, 20312).
peak(kilimanjaro, 19340).
peak(elbrus, 18510).
peak(vinson, 16050).
peak(puncak_jaya, 16023).

location(everest, asia).
location(aconcagua, south_america).
location(mckinley, north_america).
location(kilimanjaro, africa).
location(elbrus, europe).
location(vinson, antarctica).
location(puncak_jaya, australia).

climber(john).
climber(kelly).
climber(maria).
climber(derek).
climber(thyago).

certified(john).
certified(kelly).
certified(maria).
certified(derek).
not(certified(thyago)).

would_climb(C, M) :- climber(C), mount(M), (
    (C == john, certified(john), location(M, north_america));
    (C == kelly, certified(kelly), peak(M, H), H > 20000);
    (C == maria, certified(maria));
    (C == derek, certified(derek), (location(M, europe); location(M, africa); location(M, australia)), peak(M, H), H < 19000)
).

% Queries
/*
?- mount(everest).
?- location(kilimanjaro, africa).
?- peak(elbrus, H), H > 18000.
?- certified(thyago).
?- certified(john).
?- certified(C).
?- would_climb(john, M).
?- would_climb(kelly, M).
?- would_climb(maria, M).
?- would_climb(derek, M).
?- would_climb(thyago, M).
*/
