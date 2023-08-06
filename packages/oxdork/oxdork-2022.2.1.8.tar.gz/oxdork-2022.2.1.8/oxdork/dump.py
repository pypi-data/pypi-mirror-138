def dump(args,results,counter):
	with open(args.dump, "a") as file:
		file.write(f"[{counter}] {results}\n")
		file.close()