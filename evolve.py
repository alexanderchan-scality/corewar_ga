#! /usr/bin/python

import sys
import time
import generation

def main():
    #initial gen
    best = generation.Champion(0, 0)
    best_lines = None
    with open("./knut.s", 'r') as ifile:
        best_lines = [line for line in ifile]
        best.take_lines(best_lines[2:])
        champion_list = [best]
        gen_0 = generation.Generation(int(sys.argv[1]))
        gen_0.load_champ("./old_gen/")
        print "compile generation"
        gen_0.compile_gen()
        gen_0.fight()
        
        ts = int(time.time())
        print (ts)
        print "Crossover, Mutation and Elitism"
        cur_gen = gen_0.next_generation()
        ts = int(time.time())
        print (ts)
        print "Compile generation"
        cur_gen.compile_gen()
        
        ts = int(time.time())
        print (ts)
        print "Figth (rank them)"
        cur_gen.fight()
        
        ts = int(time.time())
        print (ts)
        while (not cur_gen.isbest(champion_list)):
            print "Create next generation"
            cur_gen = cur_gen.next_generation()
            
            ts = int(time.time())
            print (ts)
            print "compile new generation"
            
            ts = int(time.time())
            print (ts)
            cur_gen.compile_gen()
            print "Fit function"
            cur_gen.fight()
            print "Can we beat the knut yet?"

    print "Succes"
    print ("done")
    return (0)

if __name__ == "__main__":
    main()
