import requests
import base64
import json
import random
import time
import uuid
from urllib.parse import unquote
from requests_toolbelt import MultipartEncoder  # pip3 install requests-toolbelt
from threading import Timer
import time
import re


class KuaiNiao_Client:

    def __init__(self):
        # Base Funciton
        self._time_int = lambda: int(time.time())
        self._random_uuid4 = lambda: str(uuid.uuid4())
        self._random_int = lambda: random.randint(10000000, 99999999)
        self._getRealIP = lambda iptext:  re.findall(
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", iptext)[0]
        # InitData
        self._status = -1  # -1 未初始化
        self._default_header ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }
        self._httpclient = requests.session()
        self._sdkInfo = self.GetWebSdkInfo()
        self._peerid = ""
        self._sequence = ""
        self.getCookies()
        if self._peerid == "":
            self._peerid = self._random_uuid4()
        if self._sequence == "":
            self._sequence = self._random_int()
        self._dsq = self.DownSpeedQuery()
        self._bwq = self.BandwidthInfo()
    def showInitMsg(self):
        dsq = self._dsq
        bwq = self._bwq
        print(
            '''------------------------------
当前用户:%s
状态:%s
当前网络状态:%s%s IP:%s
宽带账户:%s 允许提速:%s
签约带宽:%sM 预计提升速度:%sM
------------------------------''' % (
                unquote(self._cookies["usernick"]),
                self.PingUser()["msg"],
                dsq["sp_name"], dsq["province_name"], dsq["interface_ip"],
                bwq["dial_account"], bool(bwq["can_upgrade"]),
                str(bwq["bandwidth"]["downstream"] /
                    1024), str(bwq["max_bandwidth"]["downstream"]/1024)
            ))
    # 初始化账户Cookies

    def getCookies(self):
        cookies = ''
        with open("./cookies.txt", "r+", encoding="utf-8") as cf:
            cookies = cf.read()
            pass
        cookies = json.loads(base64.b64decode(cookies).decode('utf-8'))
        requests.utils.add_dict_to_cookiejar(self._httpclient.cookies, cookies)
        self._cookies = cookies
        return cookies

    def GetWebSdkInfo(self):
        params = {
            "ctype": "websdk",
            "ckey": "rules",
            "format": "json"
        }
        return self._httpclient.get("https://xluser-ssl.xunlei.com/config/v1/PubGetOne", params=params,headers=self._default_header).json()

    # 用户心跳包
    def PingUser(self):
        params = {
            "appid": "101",
            "appName": "WEB-k.xunlei.com",
            "deviceModel": "chrome/79.0.3945.130",
            "deviceName": "PC-Chrome",
            "hl": "",
            "OSVersion": "Win32",
            "provideName": "NONE",
            "netWorkType": "NONE",
            "providerName": "NONE",
            "sdkVersion": self._sdkInfo['data']["defaultVersion"],
            "clientVersion": "NONE",
            "protocolVersion": "300",
            "devicesign": self._cookies["deviceid"],
            "platformVersion": "1",
            "fromPlatformVersion": "1",
            "format": "cookie",
            "timestamp": "self._time_int()",
            "userID": self._cookies["userid"],
            "sessionID": self._cookies["sessionid"],
        }
        data = MultipartEncoder(
            fields=params, boundary='----WebKitFormBoundarytZTJQrWcjjcJIMVQ')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "authority": "xluser-ssl.xunlei.com",
            'Content-Type': data.content_type,
            "method": "POST",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "path": "/xluser.core.login/v3/ping",
            "scheme": "https",
        }
        result = self._httpclient.post(
            "http://xluser-ssl.xunlei.com/xluser.core.login/v3/ping", data=data, headers=headers)
        if result.status_code == 200:
            if result.text == "":
                return {"status": "Login", "msg": "用户保持在线中..."}
            else:
                try:
                    r = result.json()
                    r["status"] = "Logout"
                    r["msg"] = "用户离线."
                    return r
                except:
                    return {"status": "UnkownError", "msg": "异常错误:"+result.text}
        else:
            return {"status": "UnkownError", "msg": "异常错误:"+result.text}

    def DownSpeedQuery(self):
        params = {
            "host": "api.portal.swjsq.vip.xunlei.com",
            "port": "81",
            "callback": "",
            "sequence": self._sequence,
            "peerid": self._peerid,
            "sessionid": self._cookies["sessionid"],
            "userid": self._cookies["userid"],
            "client_type": "kn-speed",
            "client_version": "2.0.0",
            "_": self._time_int()
        }
        result = self._httpclient.get(
            "https://xlkn-ssl.xunlei.com/queryportal", params=params,headers=self._default_header).json()
        #realip = self._getRealIP(
        #    self._httpclient.get("http://ip.3322.net").text)
        #if result["interface_ip"] != realip:
        #    print("[Info]:FixRealIP:%s->%s" % (result["interface_ip"], realip))
        #    result["interface_ip"] = realip
        return result

    def UPSpeedQuery(self):
        params = {
            "host": "upspeed.swjsq.xunlei.com",
            "port": "80",
            "callback": "",
            "sequence": self._sequence,
            "peerid": self._peerid,
            "sessionid": self._cookies["sessionid"],
            "userid": self._cookies["userid"],
            "client_type": "kn-speed",
            "client_version": "2.0.0",
            "_": self._time_int()
        }
        return self._httpclient.get("https://upspeed-swjsq-ssl.xunlei.com/queryportal", params=params,headers=self._default_header).json()

    def BandwidthInfo(self):
        downspeedquery = self._dsq
        params = {
            "host": downspeedquery["interface_ip"],
            "port": downspeedquery["interface_port"],
            "callback": "",
            "sequence": self._sequence,
            "peerid": self._peerid,
            "sessionid": self._cookies["sessionid"],
            "userid": self._cookies["userid"],
            "client_type": "kn-speed",
            "client_version":  "2.0.0",
            "_": self._time_int()
        }
        result = self._httpclient.get("https://xlkn-ssl.xunlei.com/bandwidth", params=params,headers=self._default_header).json()
        if result["errno"]!=0:
            print("[Error]:"+result["richmessage"])
            exit(0)
        return result
    def UpgradeBW(self):
        self._dsq = self.DownSpeedQuery()
        self._bwq = self.BandwidthInfo()
        downspeedquery = self._dsq
        bwq = self._bwq
        params = {
            "host": downspeedquery["interface_ip"],
            "port": downspeedquery["interface_port"],
            "user_type": 1,
            "dial_account": bwq["dial_account"],
            "callback": "",
            "sequence": self._sequence,
            "peerid": self._peerid,
            "sessionid": self._cookies["sessionid"],
            "userid": self._cookies["userid"],
            "client_type": "kn-speed",
            "client_version":  "2.0.0",
            "_": self._time_int()
        }
        result = self._httpclient.get(
            "https://xlkn-ssl.xunlei.com/upgrade", params=params,headers=self._default_header).json()
        return result

    def RecoverBW(self):
        self._dsq = self.DownSpeedQuery()
        self._bwq = self.BandwidthInfo()
        downspeedquery = self._dsq
        bwq = self._bwq
        params = {
            "host": downspeedquery["interface_ip"],
            "port": downspeedquery["interface_port"],
            "dial_account": bwq["dial_account"],
            "callback": "",
            "sequence": self._sequence,
            "peerid": self._peerid,
            "sessionid": self._cookies["sessionid"],
            "userid": self._cookies["userid"],
            "client_type": "kn-speed",
            "client_version":  "2.0.0",
            "_": self._time_int()
        }
        result = self._httpclient.get(
            "https://xlkn-ssl.xunlei.com/recover", params=params,headers=self._default_header).json()
        if result["errno"] == 0:
            result["message"] = "下线成功!"
        return result


wait_t_arr = []


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    wait_t_arr.append(t)
    return t

def update_speedup(kn_c):
    print("[Info]:"+kn_c.PingUser()["msg"])
    print("[Info]:"+kn_c.RecoverBW()["message"]+"等待上线加速...")
    time.sleep(60)
    print("[Info]:"+kn_c.UpgradeBW()["message"])

if __name__ == "__main__":
    kn_c = KuaiNiao_Client()
    # print(kn_c.PingUser())
    # print(kn_c.GetWebSdkInfo())
    # print(kn_c.DownSpeedQuery())
    # print(kn_c.UPSpeedQuery())
    # print(kn_c.BandwidthInfo())
    # print(kn_c.UpgradeBW())
    kn_c.showInitMsg()
    update_speedup(kn_c)
    set_interval(lambda: kn_c.showInitMsg(), 60*60*2)
    set_interval(lambda: print("[Info]:"+kn_c.PingUser()["msg"]), 60*15)
    set_interval(lambda: update_speedup(kn_c), 60*60*1.5)
    for t in wait_t_arr:
        t.join()
    print("Ending...")
