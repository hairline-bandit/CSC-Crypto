# "https://cdn.jsdelivr.net/npm/brython@3.8.9/brython_stdlib.js"
# "https://cdn.jsdelivr.net/npm/brython@3.8.9/brython.min.js"

def num(num):
    return float(num) if "." in num else int(num)


import six_fo
import hashlib
from flask import Flask, render_template, request, redirect, url_for
import ast
app = Flask(__name__)

blockchain = [{"send": "SYSTEM", "receive": "SYSTEM", "amount": 0, "time": 1587374420, "verify": "0" * 64, "last_key": 0, "key": 0}] # <- Genesis block
mining_queue = []



def make_file():
    global blockchain
    global mining_queue
    with open("blockchain.txt", "w") as f:
        for i in blockchain:
            if i != {"send": "SYSTEM", "receive": "SYSTEM", "amount": 0, "time": 1587374420, "verify": "0" * 64, "last_key": 0, "key": 0}:
                for j in i.values():
                    f.write(str(j) + " ")
                f.write("\n")
    with open("mining_queue.txt", "w") as f:
        for i in mining_queue:
            for j in i.values():
                f.write(str(j) + " ")
            f.write("\n")


def is_dist_hash(hash, difficulty):
    with open("dist_for_mine.txt", "r") as f:
        content = [i[:-2] for i in f.readlines()]
        for i in content:
            if i.split(" ")[1] == hash and i.split(" ")[0] == str(difficulty):
                return True
    return False

def is_compl_hash(hash):
    with open("completed_mine.txt", "r") as f:
        content = [i[:-2] for i in f.readlines()]
        for i in content:
            if i == hash:
                return True
    return False

def get_dist_hash(hash):
    with open("dist_for_mine.txt", "r") as f:
        content = [i[:-2] for i in f.readlines()]
        for i in content:
            if i.split(" ")[1] == hash:
                return i[i.index("{"):]
    return -1

def get_balance(user):
    if get_pass(user) != None:
        balance = float(0)
        with open("blockchain.txt", "r") as f:
            content = [i[:-2] for i in f.readlines()]
            for i in content:
                if i.split(" ")[0] == user:
                    balance -= float(i.split(" ")[2])
                elif i.split(" ")[1] == user:
                    balance += float(i.split(" ")[2])
        with open("mining_queue.txt", "r") as f:
            content = [i[:-2] for i in f.readlines()]
            for i in content:
                if len(i.split(" ")) > 0 and i.split(" ")[0] == user:
                    balance -= float(i.split(" ")[2])
                elif len(i.split(" ")) > 1 and i.split(" ")[1] == user:
                    balance += float(i.split(" ")[2])
        with open("mine_reward.txt", "r") as f:
            content = [i[:-2] for i in f.readlines()]
            for i in content:
                if i.split(" ")[0] == user:
                    balance += float(i.split(" ")[1])
        return balance
    return None



users = []
usersn = []

asd = None
asd2 = None
asd3 = None
def get_pass(user):
    with open("users.txt", "r") as f:
        content = f.readlines()
        for i in content:
            if i.split(" ")[0] == user:
                return i[i.index("\"") + 1:-2]
    return None

@app.route("/")
def index():
    make_file()
    return render_template("index.html")

@app.route("/createacc", methods=["POST", "GET"])
def createacc():
    make_file()
    if request.method == "POST":
        global users
        global usersn
        global asd
        user = request.values["user"]
        passw = request.values["passw"]
        if user.replace(" ", "") not in usersn and user.replace(" ", "") != "" and " " not in user and "\"" not in user and user != "SYSTEM":
            usersn.append(user.replace(" ", ""))
            users.append((user.replace(" ", ""), passw))
            f = open("users.txt", "a")
            for i in enumerate(users):
                f.write(i[1][0] + " " + "\"" + i[1][1] + "\"" + "\n")
            f.close()
            asd = True
            return redirect(url_for("success"))
        elif user.replace(" ", "") in usersn or user.replace(" ", "") == "" or " " in user or "\"" in user or user == "SYSTEM":
            asd = False
            return redirect(url_for("fail"))
    else:
        return render_template("createacc.html", userlist=usersn)

@app.route("/success")
def success():
    make_file()
    return render_template("success.html")

@app.route("/failure")
def fail():
    make_file()
    return render_template("fail.html")

@app.route("/sendtransac", methods=["POST", "GET"])
def sendtransac():
    make_file()
    global mining_queue
    if request.method == "POST":
        global users
        global usersn
        global asd2
        tim = request.values["time"]
        user = request.values["send"]
        verify = request.values["verify"]
        passw = get_pass(user)
        receive = request.values["receive"]
        amount = request.values["amount"]
    
        if hashlib.sha256((str(tim) + passw).encode("UTF-8")).hexdigest() == verify and user in usersn and receive in usersn and get_pass(user) != None and get_balance(user) >= float(amount):
            mining_queue.append({"send": user, "receive": receive, "amount": amount, "time": tim, "verify": verify, "last_key": None, "key": None})
            print(mining_queue)
            asd2 = True
            return redirect(url_for("success"))
        else:
            asd2 = False
            return redirect(url_for("success"))
    else:
        return render_template("transac.html")

@app.route("/getbalance", methods=["POST", "GET"])
def getbalance():
    make_file()
    if request.method == "POST":
        user = request.form["user"]
        balance = get_balance(user)
        if balance == None:
            return "The user that you entered does not exist"
        else:
            return render_template("viewbalance.html", balan=balance)
    else:
        return render_template("getbalance.html")

@app.route("/result")
def result():
    make_file()
    if asd:
        return render_template("success.html")
    elif not asd:
        return render_template("fail.html")

@app.route("/resulttransac")
def result_transac():
    make_file()
    if asd2:
        return render_template("success.html")
    elif not asd2:
        return render_template("fail2.html")

@app.route("/mining", methods=["POST", "GET"])
def mining():
    make_file()
    global mining_queue
    global blockchain
    global asd3
    if request.method == "POST":
        key_num = request.values["key"]
        block_hash = request.values["hash"]
        difficulty = request.values["difficulty"]
        user = request.values["user"]
        if six_fo.encrypt(block_hash, format(int(key_num), "064x"))[:int(difficulty)] == "0" * int(difficulty) and is_dist_hash(block_hash, int(difficulty)) and not is_compl_hash(block_hash):
            dic = None
            try:
                dic = ast.literal_eval(get_dist_hash(block_hash))
            except:
                asd3 = "none"
                return redirect(url_for("fail"))
            dicc = {}
            for k, v in dic.items():
                if k == "key":
                    dicc[k] = int(key_num)
                elif k == "last_key":
                    dicc[k] = int(blockchain[-1]["key"])
                else:
                    dicc[k] = v
            blockchain.append(dicc)
            dic_no_key = dic
            dic_no_key["key"] = None
            dic_no_key["last_key"] = None
            mining_queue.remove(dic_no_key)
            with open("completed_mine.txt", "a") as f:
                f.write(str(block_hash) + "\n")
            with open("mine_reward.txt", "a") as f:
                f.write(user + " " + "10" + " \n")
            asd3 = "full"
            return redirect(url_for("success"))
        elif six_fo.encrypt(block_hash, format(int(key_num), "064x"))[:int(difficulty)] == "0" * int(difficulty) and is_dist_hash(block_hash, int(difficulty)):
            with open("mine_reward.txt", "a") as f:
                f.write(user + " " + "0.25" + " \n")
            asd3 = "semi"
            return redirect(url_for("success"))
        else:
            asd3 = "none"
            return redirect(url_for("success"))
    elif len(mining_queue) > 0:
        bhash = hashlib.sha256((mining_queue[0]["send"] + mining_queue[0]["receive"] + str(mining_queue[0]["amount"]) + str(mining_queue[0]["time"]) + mining_queue[0]["verify"]).encode("UTF-8")).hexdigest()
        diff = len(blockchain) // 1000 + 4
        with open("dist_for_mine.txt", "a") as f:
            f.write(str(diff) + " " + bhash + " " +  str(mining_queue[0]) + " \n")
        return render_template("mining.html", bh=bhash, dif=diff)
    else:
        return render_template("nothing_mine.html")

@app.route("/mineresult")
def mine_result():
    make_file()
    if asd3 == "full":
        return render_template("result_mine.html", amount=10)
    elif asd3 == "semi":
        return render_template("result_mine.html", amount=0.25)
    else:
        return render_template("no_mine.html")

if __name__ == "__main__":
    help = {0: "send", 1: "receive", 2: "amount", 3: "time", 4: "verify", 5: "last_key", 6: "key"}
    with open("blockchain.txt", "r") as f:
        content = [i[:-2] for i in f.readlines()]
        for i in content:
            out = {}
            curr = i.split(" ")
            for j in range(len(curr)):
                if j == 0 or j == 1 or j == 4:
                    out[help[j]] = curr[j]
                else:
                    out[help[j]] = num(curr[j])
            blockchain.append(out)

    with open("mining_queue.txt", "r") as f:
        content = [i[:-2] for i in f.readlines()]
        for i in content:
            out = {}
            curr = i.split(" ")
            for j in range(len(curr)):
                if j == 0 or j == 1 or j == 4:
                    out[help[j]] = curr[j]
                elif j == 2 or j == 3:
                    out[help[j]] = num(curr[j])
                else:
                    out[help[j]] = None
            mining_queue.append(out)
    
    if len(mining_queue) == 0:
        mining_queue.append({"send": "SYSTEM", "receive": "SYSTEM", "amount": 0, "time": 1587374420, "verify": "0" * 64, "last_key": None, "key": None})
    app.run(debug=True)
