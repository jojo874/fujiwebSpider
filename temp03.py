import requests, json, sys, os, datetime

webhook = "http://172.22.21.17:4003/?access_token=88dd02ac5f4b731c4a03973c3a023f0e461d270dc6e476bd1bed0b3f9ada3d04"

user = sys.argv[1]
text = sys.argv[3]
data = {
    "msgtype": "text",
    "text": {
        "content": "报警"+text
    },
    "at": {
        "atMobiles": [
            user
        ],
        "isAtAll": False
    }
}
headers = {'Content-Type': 'application/json'}
x = requests.post(url=webhook, data=json.dumps(data), headers=headers)
print(x.json())
# if os.path.exists("/tmp/dingding.log"):
#     f = open("/tmp/dingding.log", "a+")
# else:
#     f = open("/tmp/dingding.log", "w+")
# f.write("\n" + "--" * 30)
# if x.json()["errcode"] == 0:
#     f.write("\n" + str(datetime.datetime.now()) + "  " + str(user) + "  " + "发送成功" + "\n" + str(text))
#     f.close()
# else:
#     f.write("\n" + str(datetime.datetime.now()) + "  " + str(user) + "  " + "发送失败" + "\n" + str(text))
#     f.close()