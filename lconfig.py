import json
import time

def getctime(filename):
    with open('ctime.json', 'r') as file:
           ctime=json.load(file)[filename]
    return ctime
def writectime(filename):
    with open('ctime.json', 'r') as file:
        data = json.load(file)
    data[filename]=str(int(time.time()))
    with open('ctime.json', 'w') as file:
        json.dump(data, file, indent=4)
def downctime(filename):
    with open('ctime.json', 'r') as file:
        data = json.load(file)
    data[filename]=str(int(time.time())-12)
    with open('ctime.json', 'w') as file:
        json.dump(data, file, indent=4)
def config(new=False):
    if (global_ctime["lconfig.json"] == getctime("lconfig.json"))and(not(new)):
        #print("\033[1;36mconfig is not changed\033[0m")
        #print("\033[1;36mconfig is not changed\033[0m")
        return global_data["lconfig.json"]
    #print("\033[1;36mreading config file\033[0m")
    with open('lconfig.json', 'r') as file:
           config=json.load(file)
    return config
def writeConfig(key,value):
    if value=="":
        return
    with open('lconfig.json', 'r') as file:
        data = json.load(file)
    data[key]=value
    with open('lconfig.json', 'w') as file:
        json.dump(data, file, indent=4)
    writectime("lconfig.json")
global_ctime = {}
global_data = {}
global_ctime["lconfig.json"]=getctime("lconfig.json")
global_data["lconfig.json"]=config(True)

