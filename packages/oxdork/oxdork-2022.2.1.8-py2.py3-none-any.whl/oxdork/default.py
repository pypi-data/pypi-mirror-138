from oxdork import colors, dump
from googlesearch import search

def dork(args,logging):
   number=0
   counter=0
   if args.verbose:
   	logging.info(f"{colors.white}Fetching {args.count} dorks...{colors.reset}")
   for results in search(args.query, num=int(args.count),start=0,stop=None,lang="en",tld="com", pause=2.5):
       number+=1
       counter+=1
       logging.debug(f"[{counter}] {colors.green}{results}{colors.reset}")
       
       if args.dump:
           dump.dump(args,results,counter)
           
       if number >= int(args.count):
       	break