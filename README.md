# corewar_ga

An attempt at generating a Corewar champion with Genetic Algorithm methodologies: 
+Elitism by keeping winners in the pool such that their traits can be inherited and culling of losing corewar champions. 
+Mutation by adding variants in the pool in attempt to create one that will beat previous champions. 
+Crossover, another form of adding variants, by crossing traits from winning champions to another winning champions such that an "offspring" can be created.

Starting with generation 0, written by students from 42, champions are pit against one another in a fight. The winners will advance into the next generation, and "new" champions will be added into the pool by applying the genetic algorithm methods. This process will continue until one such champion is generated that can beat all of the human written corewar champions in a fight, the terminating condition.
