# -*- coding:utf-8 -*-
import json
import pyperclip
from playwright.sync_api import sync_playwright
import wx

用户列表 = "用户列表.json"
登陆地址 = 'https://home.m.jd.com/myJd/home.action'
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='', size=(400, 350),name='frame',style=541072384)
        self.启动窗口 = wx.Panel(self)
        self.Centre()
        self.选择列表框1 = wx.CheckListBox(self.启动窗口,size=(360, 250),pos=(10, 10),name='listBox',choices=[],style=0)
        self.选择列表框1.SetOwnBackgroundColour((204, 237, 199, 255))
        self.按钮1 = wx.Button(self.启动窗口,size=(360, 30),pos=(10, 270),label='开始执行',name='button')
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        listData = []
        with open(用户列表, "r") as f:
            data = json.load(f)
            for x in data:
                listData.append("{name}|{passwd}".format(name=x, passwd=data[x]))
        self.选择列表框1.SetItems(listData)
        self.选择列表框1.SetCheckedItems(list(range(0, len(listData))))

    def 按钮1_按钮被单击(self,event):
        cookies = ''
        for item in self.选择列表框1.GetCheckedStrings():
            用户名 = item.split("|")[0].strip()
            密码 = item.split("|")[1].strip()
            print("用户名=[{name}] 密码=[{passwd}]".format(name=用户名, passwd=密码))
            with sync_playwright() as playwright:
                cookies += self.run(playwright, 用户名, 密码)
                cookies += "&"
                pyperclip.copy(cookies)
                pass

    def run(self, playwright, 帐号, 密码):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()

        # Open new page
        page = context.new_page()

        # Go to https://plogin.m.jd.com/login/login?appid=300&returnurl=https%3A%2F%2Fwq.jd.com%2Fpassport%2FLoginRedirect%3Fstate%3D2404625993%26returnurl%3Dhttps%253A%252F%252Fhome.m.jd.com%252FmyJd%252Fnewhome.action%253Fsceneval%253D2%2526ufc%253D%2526&source=wq_passport
        page.goto(登陆地址)

        # Click text=账号密码登录
        page.click("text=账号密码登录")

        # Fill [placeholder="用户名/邮箱/手机号"]
        page.fill('//*[@id="username"]', 帐号)

        # Fill [placeholder="请输入密码"]
        page.fill('//*[@id="pwd"]', 密码)

        # Check input[type="checkbox"]
        page.check("input[type=\"checkbox\"]")

        # Click text=登 录
        page.click("text=登 录")

        jsonData = {}
        iCount = 0
        while iCount <= 300:
            for x in context.cookies():
                if x['name'] == 'pt_key':
                    jsonData['PT_KEY'] = x['value']
                    print("cookie.pt_key : " + x['value'])
                if x['name'] == 'pt_pin':
                    jsonData['PT_PIN'] = x['value']
                    print("cookie.pt_pin : " + x['value'])
            if 'PT_KEY' in jsonData and 'PT_PIN' in jsonData:
                break
            else:
                iCount += 1
                if browser.is_connected():
                    page.wait_for_timeout(1 * 1000)
                else:
                    break

        # pyperclip.copy(json.dumps(jsonData))
        # pt_key=${ptKey};pt_pin=${ptPin}
        # context.storage_state(path="auth.json")
        context.close()
        browser.close()
        return 'pt_key={ptKey};pt_pin={ptPin}'.format(ptKey=jsonData['PT_KEY'], ptPin=jsonData['PT_PIN'])



class myApp(wx.App):
    def  OnInit(self):
        self.iDmfbdvaNk = Frame()
        self.iDmfbdvaNk.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()