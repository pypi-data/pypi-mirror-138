"""prayer_tool"""
import sys
import getopt
from datetime import datetime
from .voice_assist import Assistant

##Declaring needed variables
SCHOOL = 3
CURRENT_TIME = datetime.now().time()
LOCATION = "Brussels"
DEST = "fr"
VOLUME = 20
HELP_STRING = '\nArguments:\n -c <city> (default -> Brussels) \n -l <language> (default -> fr)\n'
ERROR_LINE = "An error occured, check for typos in the command line arguments or try again later"

##Getting all the command line arguments
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hc:l:v:",["city=","lang=", "volume="])
except getopt.GetoptError:
    print(HELP_STRING)
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print (HELP_STRING)
        sys.exit()
    elif opt in ("-c", "--city"):
        LOCATION = arg
    elif opt in ("-l", "--lang"):
        DEST = arg
    elif opt in ("-v", "--volume"):
        VOLUME = arg

def main():
    instance = Assistant(LOCATION, DEST, VOLUME)
    instance.loop()

if __name__ == "__main__":
    main()