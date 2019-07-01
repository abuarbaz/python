import os.path

if os.path.exists("C:\python3"):
    print ("file exits")
else:
    print("no file exits")

try:
    f = open("C:\Buildagent")
except FileNotFoundError:
    print ("no file exits")