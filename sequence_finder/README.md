# Sequence finder
Sequence finder is a toy project for finding the expression of a numeric sequence, given the sequence itself.

I've used a Genetic Algorithm approach. The main idea is to treat a random expression as a phenotype. So, we have a set of expression created randomly and the simulation compute how much they "fit" to the searched sequence and let them evolve; the fitness is defined as the difference between the searched values and the values evaluated by the random expression. 

For more details about the structure, see my blog post:
[http://andreaiacono.blogspot.it/2015/12/a-numeric-sequence-finder-based-on.html](http://andreaiacono.blogspot.it/2015/12/a-numeric-sequence-finder-based-on.html)
