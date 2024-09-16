from flask import Flask, url_for, redirect, render_template, session, request, abort
from mcstatus import JavaServer
import json
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import time
import os
import zipfile
from gevent import pywsgi
import lconfig
import mcrcon

app = Flask(__name__)
app.secret_key = 'abc123'
app.permanent_session_lifetime = timedelta(hours=2)


def send_cmd(cmd):
    host = lconfig.config()["rcon_ip"]
    port = lconfig.config()["rcon_port"]
    password = lconfig.config()["rcon_password"]
    rcon = mcrcon.MCRcon(host, password, port)
    rcon.connect()
    response = rcon.command(cmd)
    rcon.disconnect()
    return response


def sendkey(uuid):
    if not uuid=="test":
        print("\033[1;33m" + uuid + " 的验证码是" + str(hash(uuid + "loshop"))[-6:] + "\033[0m")
    else:
        print("\033[1;33mChecking Server Status...\033[0m")
    send_cmd("tell " + uuid + " 你的验证码是" + str(hash(uuid + "loshop"))[-6:])


def auth(uuid, key):
    if str(hash(uuid + "loshop"))[-6:] == str(key):
        return True
    return False


executor = ThreadPoolExecutor(2)


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    print("\033[1;31;40m压缩中\033[0m")
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    print("\033[1;31;40m压缩完毕\033[0m")
    with open('data.json', 'r') as file:
        data = json.load(file)

    data["imgtime"] = time.asctime()
    data["ziping"] = False
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


@app.route("/rezip")
def rezip():
    try:
        os.remove(".\\static\\server.zip")
    except:
        pass
    with open('data.json', 'r') as file:
        data = json.load(file)
    if data["ziping"]:
        print("\033[1;31;42m压缩中\033[0m")
        return render_template("rezip.html", servername=lconfig.config()["server_name"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    data["ziping"] = True
    print("\033[1;31;42m未压缩\033[0m")
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    executor.submit(zipDir, ".\\mcsmanager\\daemon\\data\\InstanceData\\" + lconfig.config()["server_id"],
                    ".\\static\\server.zip")

    return render_template("rezip.html", time=data["imgtime"], servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/ziping")
def ziping():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return str(data["ziping"])


@app.route("/zip")
def dzip():
    if lconfig.config()["enable_download_img"] == "":
        abort(403)
    with open('data.json', 'r') as file:
        data = json.load(file)
    if data["ziping"]:
        return redirect(url_for("rezip"))
    return render_template("zip.html", time=data["imgtime"], servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/viewer")
def viewer():
    if lconfig.config()["enable_seed_map"] == "":
        abort(403)
    return render_template("viewer.html", servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/rpanel")
def pviewer():
    abort(404)
    return render_template("panel.html", servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/sw")
def wviewer():
    if lconfig.config()["enable_real_world"] == "":
        abort(403)
    return render_template("world.html", servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


def getlist():
    host = lconfig.config()["rcon_ip"]
    port = lconfig.config()["rcon_port"]
    password = lconfig.config()["rcon_password"]
    rcon = mcrcon.MCRcon(host, password, port)
    rcon.connect()
    response = rcon.command("list")
    rcon.disconnect()
    return response.split(":")[1].split(",")


@app.route("/getl")
def gl():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


@app.route('/new', methods=["POST", "GET"])
def result():
    if lconfig.config()["enable_register"] == "":
        abort(403)
    if request.method == "POST":
        result = request.form.get("name")
        if result == "":
            return render_template("new.html", result=result + "请输入游戏名", color="red",
                                   servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
                                   e_real_world=lconfig.config()["enable_real_world"],
                                   e_download_img=lconfig.config()["enable_download_img"],
                                   e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                                   e_about=lconfig.config()["enable_about"],
                                   e_client_download=lconfig.config()["enable_client_download"],
                                   e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
        with open('data.json', 'r') as file:
            data = json.load(file)
        if result in data["user"]:
            return render_template("new.html", result=result + "已经注册，请勿重复操作", color="red",
                                   servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
                                   e_real_world=lconfig.config()["enable_real_world"],
                                   e_download_img=lconfig.config()["enable_download_img"],
                                   e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                                   e_about=lconfig.config()["enable_about"],
                                   e_client_download=lconfig.config()["enable_client_download"],
                                   e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
        data["user"].append(result.strip(' '))
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return render_template("new.html", result=result + " 注册成功！", color="white",
                               servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    return render_template("new.html", servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route('/tp_api', methods=['POST'])
def tpapi():
    rjson = request.json
    print('recv:', rjson)
    res = {"res": "200", "t": "ok", "c": "red"}
    if request.method == "POST":
        result = rjson["name"]
        if result == "":
            res["t"] = "请输入游戏名"
            res["c"] = "red"
            return res
        with open('data.json', 'r') as file:
            data = json.load(file)
        if result in data["user"]:
            if not auth(rjson["name"], rjson["ukey"]):
                res["t"] = "验证码错误！"
                res["c"] = "red"
                return res
            if rjson["x"] == "" or rjson["y"] == "" or rjson["z"] == "":
                res["t"] = "请输入目的地坐标！"
                res["c"] = "red"
                return res
            try:
                cmd("tp " + rjson["name"] + " " + rjson["x"] + " " + rjson["y"] + " " + rjson["z"])
            except:
                res["t"] = "无法传送！"
                res["c"] = "red"
                return res
            res["c"] = "white"
            res["t"] = "已将 " + result + "传送到 x:" + rjson["x"] + " y:" + rjson["y"] + " z:" + rjson["z"] + " ！"
            return res

        res["c"] = "red"
        res["t"] = "请先注册游戏名！"

    return res


@app.route('/sendcode_api', methods=['POST'])
def scapi():
    rjson = request.json
    print('recv:', rjson)
    res = {"res": "200", "t": "ok", "c": "red"}
    if request.method == "POST":
        result = rjson["name"]
        if result == "":
            res["t"] = "请输入游戏名"
            res["c"] = "red"
            return res
        with open('data.json', 'r') as file:
            data = json.load(file)
        if result in data["user"]:
            res["c"] = "white"
            res["t"] = " 验证码已发送到" + result + "！"
            try:
                sendkey(rjson["name"])
            except:
                res["t"] = "验证码发送失败！"
                res["c"] = "red"
                return res
            return res

        res["c"] = "red"
        res["t"] = "请先注册游戏名！"

    return res


@app.route('/new_api', methods=['POST'])
def login():
    rjson = request.json
    print('recv:', rjson)
    res = {"res": "200", "t": "ok", "c": "red"}
    if request.method == "POST":
        result = rjson["name"]
        if result == "":
            res["t"] = "请输入游戏名"
            res["c"] = "red"
            return res
        with open('data.json', 'r') as file:
            data = json.load(file)
        if result in data["user"]:
            res["c"] = "red"
            res["t"] = result + " 已经注册，请勿重复操作"
            return res

        data["user"].append(result.strip(' '))
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        res["c"] = "white"
        res["t"] = result + " 注册成功！"

    return res


#@app.route('/del', methods=["POST", "GET"])
#def udel():
#    abort(403)
#    if request.method == "POST":
#        result = request.form.get("name")
#        sendkey(result)
#        if result == "":
#            return render_template("del.html", result=result + "请输入游戏名", color="red",
#                                   servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
#                                   e_real_world=lconfig.config()["enable_real_world"],
#                                   e_download_img=lconfig.config()["enable_download_img"],
#                                   e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
#                                   e_about=lconfig.config()["enable_about"],
#                                   e_client_download=lconfig.config()["enable_client_download"],
#                                   e_register=lconfig.config()["enable_register"],
#                               qq_group_id=lconfig.config()["qq_group_id"],
#                               qq_group_link=lconfig.config()["qq_group_link"])
#        with open('data.json', 'r') as file:
#            data = json.load(file)
#        if result.strip(' ') not in data["user"]:
#            return render_template("del.html", result=result + "已经移除，请勿重复操作", color="red",
#                                   servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
#                                   e_real_world=lconfig.config()["enable_real_world"],
#                                   e_download_img=lconfig.config()["enable_download_img"],
#                                   e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
#                                   e_about=lconfig.config()["enable_about"],
#                                   e_client_download=lconfig.config()["enable_client_download"],
#                                   e_register=lconfig.config()["enable_register"],
#                               qq_group_id=lconfig.config()["qq_group_id"],
#                               qq_group_link=lconfig.config()["qq_group_link"])
#        data["user"].remove(result.strip(' '))
#        with open('data.json', 'w') as file:
#            json.dump(data, file, indent=4)
#        return render_template("del.html", result=result + " 移除成功！", color="white",
#                               servername=lconfig.config()["server_name"], e_panel=lconfig.config()["enable_panel"],
#                               e_real_world=lconfig.config()["enable_real_world"],
#                               e_download_img=lconfig.config()["enable_download_img"],
#                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
#                               e_about=lconfig.config()["enable_about"],
#                               e_client_download=lconfig.config()["enable_client_download"],
#                               e_register=lconfig.config()["enable_register"],
#                               qq_group_id=lconfig.config()["qq_group_id"],
#                               qq_group_link=lconfig.config()["qq_group_link"])
#    return render_template("del.html", e_panel=lconfig.config()["enable_panel"],
#                           e_real_world=lconfig.config()["enable_real_world"],
#                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
#                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
#                           e_client_download=lconfig.config()["enable_client_download"],
#                           e_register=lconfig.config()["enable_register"],
#                               qq_group_id=lconfig.config()["qq_group_id"],
#                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/debug")
def debug():
    abort(403)
    mserver = JavaServer.lookup(lconfig.config()["server_ip"] + ":" + lconfig.config()["server_port"])

    return str(mserver.status().players.online)


def check_online():
    wtime = 0
    while True:
        time.sleep(1)
        wtime = wtime + 1
        try:
            sendkey("test")
            lconfig.downctime("offline")
            return 0
        except:
            lconfig.writectime("offline")
        if wtime > 10:
            return 114


@app.route("/")
def index():
    if int(time.time()) - int(lconfig.getctime("offline")) <= 10:
        return render_template('index.html', servername=lconfig.config()["server_name"],
                               servername_en=lconfig.config()["server_name_en"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    try:
        mserver = JavaServer.lookup(lconfig.config()["server_ip"] + ":" + str(lconfig.config()["server_port"]))
        lconfig.downctime("offline")
        return render_template('index.html', servername=lconfig.config()["server_name"],
                               pc=str(mserver.status().players.online), online=str(" , ".join(getlist())),
                               servername_en=lconfig.config()["server_name_en"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    except Exception as e:
        lconfig.writectime("offline")
        executor.submit(check_online)
        return render_template('index.html', servername=lconfig.config()["server_name"],
                               servername_en=lconfig.config()["server_name_en"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/auth", methods=["POST", "GET"])
def wa():
    abort(403)
    if request.method == "POST":
        result = request.form.get("key")
        session['ukey'] = result
        return redirect(url_for("tp"))

    return render_template("auth.html", servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/client")
def c():
    if lconfig.config()["enable_client_download"] == "":
        abort(403)
    return render_template('client.html', servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route("/tp")
def tp():
    if lconfig.config()["enable_tp"] == "":
        abort(403)
    if int(time.time()) - int(lconfig.getctime("offline")) <= 10:
        return render_template('tp.html', servername=lconfig.config()["server_name"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    try:
        sendkey("test")
        lconfig.downctime("offline")

    except Exception as e:
        lconfig.writectime("offline")
        executor.submit(check_online)
        return render_template('tp.html', servername=lconfig.config()["server_name"],
                               e_panel=lconfig.config()["enable_panel"],
                               e_real_world=lconfig.config()["enable_real_world"],
                               e_download_img=lconfig.config()["enable_download_img"],
                               e_tp=lconfig.config()["enable_tp"], e_seed_map=lconfig.config()["enable_seed_map"],
                               e_about=lconfig.config()["enable_about"],
                               e_client_download=lconfig.config()["enable_client_download"],
                               e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])
    return render_template('tp.html', servername=lconfig.config()["server_name"], online="ok",
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


def cmd(cmmd):
    host = lconfig.config()["rcon_ip"]
    port = lconfig.config()["rcon_port"]
    password = lconfig.config()["rcon_password"]
    rcon = mcrcon.MCRcon(host, password, port)
    rcon.connect()
    response = rcon.command(cmmd)
    rcon.disconnect()
    return response


@app.route('/tpp', methods=["POST"])
def tpp():
    ukey = session.get('ukey', None)
    if not auth(request.form.get("name"), ukey):
        sendkey(request.form.get("name"))
        return redirect(url_for("tp"))
    cmd("tp " + request.form.get("name") + " " + request.form.get("x"))
    return redirect(url_for("tp"))


@app.route("/about")
def about():
    if lconfig.config()["enable_about"] == "":
        abort(403)
    return render_template('about.html', servername=lconfig.config()["server_name"],
                           e_panel=lconfig.config()["enable_panel"], e_real_world=lconfig.config()["enable_real_world"],
                           e_download_img=lconfig.config()["enable_download_img"], e_tp=lconfig.config()["enable_tp"],
                           e_seed_map=lconfig.config()["enable_seed_map"], e_about=lconfig.config()["enable_about"],
                           e_client_download=lconfig.config()["enable_client_download"],
                           e_register=lconfig.config()["enable_register"],
                               qq_group_id=lconfig.config()["qq_group_id"],
                               qq_group_link=lconfig.config()["qq_group_link"])


@app.route('/tpw', methods=["POST"])
def tpw():
    if not auth(request.form.get("name"), request.form.get("ukey")):
        sendkey(request.form.get("name"))
        return redirect(url_for("tp"))
    cmd("tp " + request.form.get("name") + " " + request.form.get("x") + " " + request.form.get(
        "y") + " " + request.form.get("z"))
    return redirect(url_for("tp"))


@app.route("/client_download")
def cd():
    if lconfig.config()["enable_client_download"] == "":
        abort(403)
    return redirect(url_for('static', filename='client.zip'))


@app.route("/net_download")
def jd():
    return redirect(url_for('static', filename='net.exe'))


@app.route("/panel")
def panel():
    if lconfig.config()["enable_panel"] == "":
        abort(403)
    return redirect("http://" + lconfig.config()["panel_ip"] + ":" + str(lconfig.config()["panel_port"]))


@app.route("/real_world")
def rw():
    if lconfig.config()["enable_real_world"] == "":
        abort(403)
    return redirect("http://" + lconfig.config()["real_world_ip"] + ":" + str(lconfig.config()["real_world_port"]))


@app.route("/world")
def ww():
    if lconfig.config()["enable_real_world"] == "":
        abort(403)
    return redirect("http://" + lconfig.config()["real_world_ip"] + ":" + str(lconfig.config()["real_world_port"]))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403


if __name__ == '__main__':
    try:

        lconfig.downctime("offline")
        print("\033[1;32mServer Started on 0.0.0.0:"+str(lconfig.config()["web_port"])+"\033[0m")
        server = pywsgi.WSGIServer(('0.0.0.0', int(lconfig.config()["web_port"])), app)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\033[1;31mServer Stopped\033[0m")
    except:
        print("\033[1;31mCannot Run Server!\033[0m")