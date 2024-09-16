import sys
import os
import time
import zipfile
import subprocess
import psutil
import json
import os
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except:
            return True
def getctime(filename):
    with open('ctime.json', 'r',encoding='utf-8') as file:
           ctime=json.load(file)[filename]
    return ctime
def writectime(filename):
    with open('ctime.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    data[filename]=str(int(time.time()))
    with open('ctime.json', 'w') as file:
        json.dump(data, file, indent=4)
def downctime(filename):
    with open('ctime.json', 'r',encoding='utf-8') as file:
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
    with open('lconfig.json', 'r',encoding='utf-8') as file:
           config=json.load(file)
    return config
def writeConfig(key,value):
    if value=="":
        return
    if value=="##false##":
        value=""
    with open('lconfig.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    data[key]=value
    with open('lconfig.json', 'w') as file:
        json.dump(data, file, indent=4)
    writectime("lconfig.json")
global_ctime = {}
global_data = {}
global_ctime["lconfig.json"]=getctime("lconfig.json")
global_data["lconfig.json"]=config(True)

def cconfig():
    killtask()
    if len(sys.argv)>1:
        if sys.argv[1]=="new":
            ccfg="y"
        else:
            ccfg = input("[SETUP INFO] 是否真的要更改配置文件？(y是 n否 默认否)")
    else:
        ccfg=input("[SETUP INFO] 是否真的要更改配置文件？(y是 n否 默认否)")
    if ccfg == "y":
        writeConfig("panel_ip",input("[SETUP] 请输入可以被公网访问的面板ip >"))
        writeConfig("panel_port",int(input("[SETUP] 请输入可以被公网访问的面板端口(默认23333) >")))
        writeConfig("web_ip",input("[SETUP] 请输入即将被部署的可以被公网访问的官网ip >"))
        writeConfig("web_port",int(input("[SETUP] 请输入即将被部署的可以被公网访问的官网端口(默认80) >")))
        writeConfig("server_name",input("[SETUP] 请输入服务器的中文名称 >"))
        writeConfig("server_name_en",input("[SETUP] 请输入服务器的英文名称 >"))
        writeConfig("rcon_password",input("[SETUP] 请输入服务器RCON密码(默认password) >"))
        writeConfig("rcon_ip",input("[SETUP] 请输入服务器RCON ip(一般为MC服务器ip) >"))
        writeConfig("rcon_port",int(input("[SETUP] 请输入服务器RCON端口(默认25575) >")))
        writeConfig("real_world_ip",input("[SETUP] 请输入服务器Gynmap服务器ip(一般为MC服务器ip) >"))
        writeConfig("real_world_port",int(input("[SETUP] 请输入服务器Gynmap服务器端口(默认8123) >")))
        writeConfig("server_ip",input("[SETUP] 请输入MC服务器ip >"))
        writeConfig("server_port",int(input("[SETUP] 请输入MC服务器端口(默认25565) >")))
        #writeConfig("server_id",input("[SETUP] 请输入服务器在MCSM中的id(默认0abe924f348142f1b31995641ebaa318) >"))
        #writeConfig("server_config_id",input("[SETUP] 请输入服务器在MCSM中配置文件的id(默认be994588e90c4eb7acc746b7cc6b2175) >"))
        if not input("[SETUP] 是否允许从官网进入MCSM控制面板(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网进入MCSM控制面板")
            writeConfig("enable_panel","true")
        else:
            print("[SETUP INFO] 已禁止从官网进入MCSM控制面板")
            writeConfig("enable_client_download", "##false##")
        if not input("[SETUP] 是否允许从官网下载客户端(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网下载客户端")
            writeConfig("enable_client_download","true")
        else:
            print("[SETUP INFO] 已禁止从官网下载客户端")
            writeConfig("enable_client_download", "##false##")
        if not input("[SETUP] 是否允许从官网注册游戏名(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网注册游戏名")
            writeConfig("enable_register","true")
        else:
            print("[SETUP INFO] 已禁止从官网注册游戏名")
            writeConfig("enable_register", "##false##")
        if not input("[SETUP] 是否允许从官网查看实时地图(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网查看实时地图")
            writeConfig("enable_real_world","true")
        else:
            print("[SETUP INFO] 已禁止从官网查看实时地图")
            writeConfig("enable_real_world", "##false##")
        if not input("[SETUP] 是否允许从官网下载和创建服务器镜像(y允许 n禁止 默认禁止) >")=="y":
            print("[SETUP INFO] 已禁止从官网下载和创建服务器镜像")
            writeConfig("enable_download_img","##false##")
        else:
            print("[SETUP INFO] 已允许从官网下载和创建服务器镜像")
            writeConfig("enable_download_img", "true")
        if not input("[SETUP] 是否允许从官网传送玩家(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网传送玩家")
            writeConfig("enable_tp","true")
        else:
            print("[SETUP INFO] 已禁止从官网传送玩家")
            writeConfig("enable_tp", "##false##")
        if not input("[SETUP] 是否允许从官网查看种子地图(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网查看种子地图")
            writeConfig("enable_seed_map","true")
        else:
            print("[SETUP INFO] 已禁止从官网查看种子地图")
            writeConfig("enable_seed_map", "##false##")
        if not input("[SETUP] 是否允许从官网查看关于页面(y允许 n禁止 默认允许) >")=="n":
            print("[SETUP INFO] 已允许从官网查看关于页面")
            writeConfig("enable_about","true")
        else:
            print("[SETUP INFO] 已禁止从官网查看关于页面")
            writeConfig("enable_about", "##false##")


def killtask():
    pids = psutil.pids()
    for pid in pids:
        if (not pid == os.getpid()) and (not pid == 0):
            try:
                p = psutil.Process(pid)
                process_name = p.name()
                pwd = p.exe()
                # print(pwd)
                if pwd == os.path.abspath(".") + "\\python\\python.exe":
                    print(
                        "[INFO] Killing python.exe: %s, pid is: %s" % (process_name, pid)
                    )
                    try:
                        p.kill()
                    except:
                        print("[INFO] Cannot kill")
                if pwd == os.path.abspath(".") + "\\mcsmanager\\daemon\\node_app.exe":
                    print("[INFO] Killing daemon: %s, pid is: %s" % (process_name, pid))
                    try:
                        p.kill()
                    except:
                        print("[INFO] Cannot kill")
                if pwd == os.path.abspath(".") + "\\mcsmanager\\web\\node_app.exe":
                    print("[INFO] Killing web pid: %s, pid is: %s" % (process_name, pid))
                    try:
                        p.kill()
                    except:
                        print("[INFO] Cannot kill")
            except:
                print("[INFO] Cannot check")
        else:

            print("\033[31m[INFO] Running task...\033[0m")


def start():
    killtask()
    if is_port_in_use(config()["web_port"]):
        input("\033[31m[ERROR] Web Port "+str(config()["web_port"])+" Is In Use!\n[ERROR] Cannot Start Web Server\033[0m")
        exit()
    print("\033[32m[INFO] Starting setup...\033[0m")
    with open(
        ".\\mcsmanager\\daemon\\data\\InstanceConfig\\be994588e90c4eb7acc746b7cc6b2175.json",
        "r",encoding='utf-8'
    ) as file:
        data = json.load(file)
    data["cwd"] = str(
        os.path.abspath(".")
        + "\\mcsmanager\\daemon\\data\\InstanceData\\0abe924f348142f1b31995641ebaa318"
    )
    with open(
        ".\\mcsmanager\\daemon\\data\\InstanceConfig\\be994588e90c4eb7acc746b7cc6b2175.json",
        "w",encoding='utf-8'
    ) as file:
        json.dump(data, file, indent=4)
        print(
            "\033[34m[INFO] .\\mcsmanager\\daemon\\data\\InstanceConfig\\be994588e90c4eb7acc746b7cc6b2175.json finished\033[0m"
        )
    verini = (
        "State:1\nInfo:原版 1.12\nLogo:PCL\\Logo.png\nReleaseTime:2017-06-02 21:50\nVersionFabric:\nVersionOptiFine:\nVersionLiteLoader:False\nVersionForge:\nVersionNeoForge:\nVersionApiCode:-1\nVersionOriginal:1.12\nVersionOriginalMain:12\nVersionOriginalSub:0\nVersionArgumentIndie:0\nVersionServerEnter:"
        + config()["server_ip"]
        + ":"
        + str(config()["server_port"])
        + "\nVersionArgumentTitle:"
        + config()["server_name"]
        + " (用户名：{user} - {login})\nVersionArgumentInfo:LoshopServerManagerClient\nLogoCustom:True"
    )
    try:
        os.remove(
            ".\\client_unpack\\.minecraft\\versions\\LoshopMcClient\\PCL\\Setup.ini"
        )
        print("\033[31m[INFO] Delecting old ini file...\033[0m")
    except:
        pass
    with open(
        ".\\client_unpack\\.minecraft\\versions\\LoshopMcClient\\PCL\\Setup.ini", "w",encoding='utf-8'
    ) as f:
        f.write(verini)
        print(
            "\033[34m[INFO] client_unpack\\.minecraft\\versions\\LoshopMcClient\\PCL\\Setup.ini写入成功\033[0m"
        )
    pclini = (
        "LaunchFolderSelect:$.minecraft\\\nLaunchVersionSelect:LoshopMcClient\nLoginPageType:0\nUiHiddenPageOther:True\nUiHiddenOtherAbout:True\nUiHiddenOtherTest:True\nUiHiddenOtherFeedback:True\nUiHiddenOtherVote:True\nUiHiddenOtherHelp:False\nUiHiddenPageDownload:True\nUiHiddenSetupUi:True\nUiHiddenSetupSystem:True\nUiLogoType:2\nUiLogoText:"
        + config()["server_name"]
        + "启动器\nUiHiddenFunctionSelect:True\nUiCustomType:2\nUiCustomNet:http://"
        + config()["web_ip"]
        + ":"
        + str(config()["web_port"])
        + "/static/pcl_index.xml\nLaunchAdvanceRun:\nLaunchAdvanceAssets:False"
    )
    try:
        os.remove(".\\client_unpack\\PCL\\Setup.ini")
        print("\033[31m[INFO] Delecting old ini file...\033[0m")
    except:
        pass
    with open(".\\client_unpack\\PCL\\Setup.ini", "w",encoding='utf-8') as f:
        f.write(pclini)
        print("\033[34m[INFO] client_unpack\\PCL\\Setup.ini finished\033[0m")

    pclxml = (
        '<local:MyCard Title="注意" Margin="0,0,0,15" CanSwap="False" IsSwaped="False">\n    <StackPanel Margin="25,40,23,15">\n      <local:MyHint Text="如果您的游戏名未注册，您将无法进入服务器" />\n        <TextBlock Margin="0,0,0,4" Text="" />\n        <TextBlock  Foreground="#8C7721" Text="启动游戏前请先点击下方按钮注册您的游戏名" />\n        <TextBlock Margin="0,0,0,4" Text="" />\n      <local:MyButton Width="140" Height="35" HorizontalAlignment="Left" Padding="13,0,13,0" Text="前往注册" EventType="打开网页" EventData="http://'
        + config()["web_ip"]
        + ":"
        + str(config()["web_port"])
        + '/new" />\n    </StackPanel>\n</local:MyCard>\n<local:MyCard Title="快捷入口" Margin="0,0,0,15" CanSwap="True" IsSwaped="True">\n    <StackPanel Margin="25,40,23,15">\n      <local:MyButton Width="140" Height="35" HorizontalAlignment="Left" Padding="13,0,13,0" Text="打开官网" EventType="打开网页" EventData="http://'
        + config()["web_ip"]
        + ":"
        + str(config()["web_port"])
        + '" />\n    </StackPanel>\n</local:MyCard>'
    )
    try:
        os.remove(".\\static\\pcl_index.xml")
        print("\033[31m[INFO] Delecting old xml file...\033[0m")
    except:
        pass
    with open(".\\static\\pcl_index.xml", "w", encoding="utf-8") as f:
        f.write(pclxml)
        print("\033[34m[INFO] static\\pcl_index.xml finished\033[0m")

    print("\033[1;31;40m[INFO] Starting Packing Client...\033[0m")
    dirpath = ".\\client_unpack"
    outFullName = ".\\static\\client.zip"
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        fpath = path.replace(dirpath, "")
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    print("\033[1;31;40m[INFO] Packing Finished\033[0m")
    command = ".\\python\\python.exe app.py"
    p = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("[INFO] Web Server Started")
    os.chdir(".\\mcsmanager\\daemon")
    command = "node_app.exe --enable-source-maps --max-old-space-size=8192 app.js "
    p = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("[INFO] Deamon Server Started")
    os.chdir("..\\web")
    command = "node_app.exe --enable-source-maps --max-old-space-size=8192 app.js  "
    p = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("[INFO] Panel Server Started")
    os.chdir("..\\..\\")
    command = ".\\python\\python.exe whitelist_host.py"
    p = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("[INFO] Whitelist Host Started")
    try:
        os.remove(
            ".\\Running.txt"
        )

    except:
        pass
    print("\033[31m[INFO] MCSM Account Is: username:admin   password:xvAVI0R37yvMHKiaLxIv\033[0m")
    input("\033[31m[INFO] All Server Started!\033[0m")
if len(sys.argv)>1:
    if sys.argv[1]=="new":
        cconfig()
        start()
        exit()
icase=input("[LOSM] 可用的操作：\n(1)更改配置\n(2)启动/重启服务器(默认)\n(3)停止服务器\n")
if icase=="1":
    cconfig()
    if input("[LOSM] 是否要重启服务器？(y是 n否 默认否)") == "y":
        start()
    os.remove(".\\Running.txt")
    exit()
if icase=="3":
    killtask()
    input("[INFO] Server Stopped")
    os.remove(".\\Running.txt")
    exit()
start()
os.remove(".\\Running.txt")