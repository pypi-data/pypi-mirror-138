#!/usr/bin/env python3

import logging
import argparse
from datetime import datetime
from googlesearch import search
from oxdork import colors, minimal, default, banner         

def main():
    parser = argparse.ArgumentParser(description=f"{colors.white}Google dorking tool{colors.reset}",epilog=f"{colors.red}ox{colors.white}Dork uses Google dorking techniques and Google dorks to find security holes and misconfigurations in web servers. Developed by {colors.green}Richard Mwewa{colors.white} | https://about.me/{colors.green}rly0nheart{colors.reset}")
    parser.add_argument("query", help=f"{colors.white}search query{colors.reset}")
    parser.add_argument("-c","--count",help=f"{colors.white}number of results to show ({colors.green}default is 10{colors.white}){colors.reset}",metavar=f"{colors.white}number{colors.reset}", default=10)
    parser.add_argument("-d","--dump",help=f"{colors.white}dump output to specified file{colors.reset}",metavar=f"{colors.white}path/to/file{colors.reset}")
    parser.add_argument("--minimal",help=f"{colors.white}run a minimal version of oxdork{colors.reset}",action="store_true")
    parser.add_argument("-v","--verbose",help=f"{colors.white}enable verbosity{colors.reset}",action="store_true")
    parser.add_argument("-u","--update",help=argparse.SUPPRESS) # This is only available in the Github version of oxDork; as pypi packages can be updated with pip
    args = parser.parse_args()
    
    start_time = datetime.now()
    logging.basicConfig(format=f"%(asctime)s {colors.white}%(message)s{colors.reset}",datefmt=f"{colors.white}%I{colors.red}:{colors.white}%M{colors.red}:{colors.white}%S%p{colors.reset}",level=logging.DEBUG)
    
    print(banner.banner)
    while True:
        try:
            if args.minimal:
                print(minimal.dork(args))
                break
            else:
            	default.dork(args,logging)
            	break
            	
        except KeyboardInterrupt:
            if args.verbose:
            	print("\n")
            	logging.info(f"{colors.white}Process interrupted with {colors.red}Ctrl{colors.white}+{colors.red}C{colors.reset}")
            	break
            break
            
        except Exception as e:
            if args.verbose:
            	logging.info(f"{colors.white}Error: {colors.red}{e}{colors.reset}")
            	
    if args.verbose:
        logging.info(f"{colors.white}Stopped in {colors.green}{datetime.now()-start_time}{colors.white} seconds.{colors.reset}")