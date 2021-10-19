import yaml
import sys
import os
if len(sys.argv) != 1:
    mode = sys.argv[1]
else:
    print("No backup mode selected, please run file with arguments")
dir_path = os.path.dirname(os.path.realpath(__file__))
configFile = open('config.yml', 'r')
config = yaml.load(configFile, Loader=yaml.FullLoader)

destinationBase = config['folders']['path']
destination = destinationBase.split("/", 1)
if destination[0] == '.':
    destination = os.path.join(dir_path, destination[1])
else:
    destination = destinationBase
print(destination)
try:
    os.makedirs(destination)
except OSError as e:
    if e.errno == 13:
        print("You don't have permision to create folder", destination)
    else:
        raise
