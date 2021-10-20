import re
import yaml
import sys
import os
import subprocess
if len(sys.argv) != 1:
    mode = sys.argv[1]
else:
    print("No backup mode selected, please run file with arguments")
    exit()
dir_path = os.path.dirname(os.path.realpath(__file__))
configFile = open('config.yml', 'r')
config = yaml.load(configFile, Loader=yaml.FullLoader)

nobackups = config['schedule'][mode]


def rsyncData(port, user, host, folderToBackup, destination):
    args = ["rsync", "-arvz", "-e", "ssh -p "+str(port), "-r"]
    args.append(user + "@" + host + ":"+folderToBackup)
    args.append(destination)
    print("executing " + ' '.join(args))
    subprocess.call(args)


def managefolders(destination, prefix, nobackups):
    print(destination, prefix)
    regex = re.escape(prefix)+r"."
    backupsInFolder = []
    initialfolder = os.path.join(destination, prefix+".0")

    folders = os.listdir(destination)
    for dir in folders:
        if(re.match(regex, dir)):
            backupsInFolder.append(dir.split('.'))
    backupsInFolder = backupsInFolder[::-1]
    if len(backupsInFolder) != 0:
        for backup in backupsInFolder:
            iteration = int(backup[1])+1
            old = os.path.join(destination, (backup[0]+'.'+backup[1]))
            new = os.path.join(destination, (backup[0]+'.'+str(iteration)))
            os.rename(old, new)
            if iteration > int(nobackups):
                os.rmdir(new)
    if not os.path.exists(initialfolder):
        os.mkdir(initialfolder)
    return initialfolder


def createFolder(destination):
    if not os.path.exists(destination):
        try:
            os.makedirs(destination)
        except OSError as e:
            if e.errno == 13:
                print("You don't have permision to create folder", destination)
            else:
                raise


destinationBase = config['folders']['path']
destination = destinationBase.split("/", 1)
if destination[0] == '.':
    destination = os.path.join(dir_path, destination[1])
else:
    destination = destinationBase
createFolder(destination)
interbackup = managefolders(destination, mode, nobackups)
for i in config['hosts']:
    backho = config['hosts'][i]
    host = backho['host']
    user = backho['user']
    folderToBackup = backho['folder']
    port = backho['port']
    rsyncData(port, user, host, folderToBackup, interbackup)
