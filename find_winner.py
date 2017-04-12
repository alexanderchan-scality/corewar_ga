import time
import generation

def main():
	#initial gen
	best = generation.Champion(0, 1)
	best_lines = None
	with open("./old_gen/knut.s", 'r') as ifile:
		best_lines = [line for line in ifile]
		best.take_lines(best_lines[2:])
		champion_list = [best]
		gen_0 = generation.Generation(10)
		gen_0.load_champ("./gen_5/")
		gen_0.compile_gen()

		if (gen_0.isbest(champion_list)):
			print "Succes"
		print ("done")
		return (0)

if __name__ == "__main__":
	main()
