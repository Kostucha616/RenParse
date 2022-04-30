import sys
import os.path
import re
import json

# write a default config if it's not found
if not os.path.exists(os.path.join(os.getcwd(), "RenParseConfig.json")):
    print("Couldn't find config file, writing a default one")
    defaultConfig = {"skip comments": True,
                     "jump one directory upwards": False,
                     "extensions to check": {"image extensions": [".jpg", ".png", ".webp"],
                                             "misc extensions": [".ogg", ".mp3", ".webm"]},
                     "strings to skip": ["[prefix_]", "**"]}
    with open('RenParseConfig.json', 'w') as configFile:
        json.dump(defaultConfig, configFile, indent=2)
        print("Default config file created")
    if str(input("Input y to proceed with default settings: ")) != 'y':
        sys.exit()

# open config file & load all config vars
config = open('RenParseConfig.json', 'r')
config = json.load(config)
skipComments = config["skip comments"]
jumpOneDirUp = config["jump one directory upwards"]
imageExtensions = []
extensionsToCheck = []
stringsToSkip = []
for ext in config["extensions to check"]["image extensions"]:
    imageExtensions.append(ext)
    extensionsToCheck.append(ext)
for ext in config["extensions to check"]["misc extensions"]:
    extensionsToCheck.append(ext)
for string in config["strings to skip"]:
    stringsToSkip.append(string)

# set up all the non-config vars
# rpy files list gathered from the entire project
rpyfiles = []
# path-like strings list we'll gather from .rpy strings
# it'll be [filepath/to/.rpy, string number, string]
pathLikeStrings = []
# resulting no-file-found paths we print to a user
brokenPaths = []

# jump 1-dir upwards
if jumpOneDirUp:
    os.chdir("..")

# print what we're working with here
if skipComments:
    print("Will skip commented-out lines")
else:
    print("Will not skip commented-out lines")
if jumpOneDirUp:
    print("Will jump one directory up from the RenParse.exe path")
else:
    print("Will not jump one directory up from the RenParse.exe path")
print("Extensions to check: ", extensionsToCheck)
# pre-launch safety check
print("Working directory, MUST be 'project\\game': ", os.getcwd())
if str(input("Input y to proceed: ")) != 'y':
    sys.exit()

# loop #1
# grab all rpy files found
for path, subdirs, files in os.walk(os.getcwd(), topdown=False):
    for name in files:
        if name.endswith(".rpy"):
            rpyfiles.append(os.path.join(path, name))

# loop #2
# looking for stuff resembling a path in rpyfiles strings
for filepath in rpyfiles:
    # open a file, !we ignore errors here cause encoding!
    rpyfile = open(filepath, errors="ignore")
    # read through all strings in file, grab all w/file exts
    for num, string in enumerate(rpyfile, 1):
        # remove indent whitespaces from a string
        string = string.strip()
        # hit brakes if it's a comment
        if skipComments and string.startswith("#"):
            continue
        # check if there's an extension present, drop into a loop#3 list if there is
        if any(extension in string for extension in extensionsToCheck):
            pathLikeStrings.append([filepath, num, string])
    # close rpy file we've checked, we're not monsters
    rpyfile.close()

# set up regexp stuff for loop #3
# delimiters for path-likes are '' and ""
delimiters = "'", "\""
regexPattern = '|'.join(map(re.escape, delimiters))

# loop #3
# here's where the actual work happens
for entry in pathLikeStrings:
    # split an entry's string by '' or ""
    splitString = re.split(regexPattern, entry[2])
    for stringPart in splitString:
        # check if string part contains a string to skip, hit brakes if it does
        if any(subString in stringPart for subString in stringsToSkip):
            continue
        # check if string part doesn't contain any extensions, brakes if true
        if not any(extension in stringPart for extension in extensionsToCheck):
            continue
        # replace / with a \ for a valid path
        stringPart = stringPart.replace("/", "\\")
        # grab file extension
        stringPartExtension = os.path.splitext(stringPart)
        # if it's an image, first check down at /images
        if stringPartExtension[1] in imageExtensions:
            filePath = os.path.join(os.getcwd(), "images\\", stringPart)
            if os.path.exists(filePath):
                continue
        # check path as the user defined it now
        filePath = os.path.join(os.getcwd(), stringPart)
        if not os.path.exists(filePath):
            # append entire entry into the broken paths list
            brokenPaths.append(entry)

if not brokenPaths:
    print("\nNo broken paths found. Nice work!")
else:
    # strip entry paths of the "working dir" part to trim down their x-size
    # & replace all \ with /'s for readability
    for entry in brokenPaths:
        entry[0] = entry[0].replace(os.getcwd(), "")
        entry[0] = entry[0].replace("\\", "/")
    print("\nBroken/weird paths found: ")
    for entry in brokenPaths:
        print("File:", entry[0], "\nLine", str(entry[1])+":", entry[2], "\n")
input("\nPress enter to quit.")
