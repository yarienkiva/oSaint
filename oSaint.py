import os, sys, time
import string
import argparse

from argparse import RawTextHelpFormatter

version = '1.1'
valide = list(string.ascii_letters + string.digits)

def search(targetMail, out):
	cdir = os.getcwd()
	letter1 = list(targetMail)[0]
	if letter1 in valide:
		if os.path.isfile(cdir+"/data/"+letter1):
			os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+letter1 + " >> "+ out)
		else:
			letter2 = list(targetMail)[1]
			if letter2 in valide:
				if os.path.isfile(cdir+"/data/"+letter1+"/"+letter2):
					os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+letter1+"/"+letter2 + " >> "+ out)
				else:
					letter3 = list(targetMail)[2]
					if letter3 in valide:
						if os.path.isfile(cdir+"/data/"+letter1+"/"+letter2+"/"+letter3):
							os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+letter1+"/"+letter2+"/"+letter3 + " >> "+ out)
					else:
						if os.path.isfile(cdir+"/data/"+letter1+"/"+letter2+"/symbols"):
							os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+letter1+"/"+letter2+"/symbols"+ " >> "+ out)
			else:
				if os.path.isfile(cdir+"/data/"+letter1+"/symbols"):
					os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+letter1+"/symbols" + " >> "+ out)
	else:
		if os.path.isfile(cdir+"/data/"+"symbols"):
			os.system("grep -ai ^"+targetMail+": "+cdir+"/data/"+"symbols" + " >> "+ out)

if __name__ == '__main__':

	print(r"""
    ___  __       _       _
   /___\/ _\ __ _(_)_ __ | |_   _ __  _   _
  //  //\ \ / _` | | '_ \| __| | '_ \| | | |
 / \_// _\ \ (_| | | | | | |_ _| |_) | |_| |
 \___/  \__/\__,_|_|_| |_|\__(_) .__/ \__, |
                               |_|    |___/

Created by Yarienkiva
Version : {}

	""".format(version))
	parser = argparse.ArgumentParser(description=r"A query.sh on steroids",formatter_class=RawTextHelpFormatter)

	parser.add_argument('-a',"--all", action="store", metavar='DOMAIN', dest='all',
						default=None, help="DO EVERYTHING")
	parser.add_argument('-e',"--emailHarvester", action="store", metavar='DOMAIN', dest='harvester',
						default=None, help="Use EmailHarvester with specified domain")
	parser.add_argument('-f',"--file", action="store", metavar='INPUT_FILE', dest='file',
						default=None, help="Input file")
	parser.add_argument('-u',"--uniq", action="store", metavar='SINGLE_MAIL', dest='single',
						default=None, help="Single mail")
	parser.add_argument('-o',"--output", action="store", metavar='OUTPUT_FILE', dest='out',
						default="oSaint.out", help="Output file")

	if len(sys.argv) is 1:
		parser.print_help()
		sys.exit()

	args = parser.parse_args()

	if  (args.harvester and args.file) or (args.single and args.file) or (args.single and args.harvester):
		print("You can't use -e / -f / -u together you dipshit")
		sys.exit(1)

	if args.harvester:
		os.chdir("../EmailHarvester")
		os.system("python3 EmailHarvester.py -d"+args.harvester+" -s ../BreachCompilation/EHarvester -e all -l 20 --noprint")
		os.chdir("../BreachCompilation")

	input = (args.single or args.file or "EHarvester")

	elist = []
	if args.harvester or args.file:
		elist = open(input, "r").read().splitlines()
		print('Using email list:', input,'\n')
	elif args.single:
		elist.append(input)
		print("Searching "+input)

	start = time.time()
	for i in elist:
		search(i, args.out)
	diff  = time.time() - start
	os.system("tail "+args.out)
	print('\nWrote output into', args.out)
	print('\nFinished looking for passwords in {} seconds'.format(diff))
