from tkinter import Frame,Tk
from MBPython import miniblink
import platform
import codecs
"""
import sys
print(sys.argv[0])
"""
"""
import os
print(os.getcwd())
print(os.path.abspath('.'))
print(os.path.abspath('test.txt'))
print(os.path.abspath('..'))
print(os.path.abspath(os.curdir))
"""
class Chromium:
    dictionary={}
    def __init__(self,name,url="http://www.baidu.com",title="Browser",dictionary=dictionary):
        li = [url,title]
        if type(name) == type([]):
            for i in name:
                dictionary[i] = li
        else:
            dictionary[name] = li
    def url(self,name,url,dictionary=dictionary):
        dictionary[name] = [url,dictionary[name][1]]
    def title(self,name,title,dictionary=dictionary):
        dictionary[name] = [dictionary[name][0],title]
    def run(self,name,dictionary=dictionary):
        a=Tk()
        a.state("zoom")
        a.update()
        a.title(dictionary[name][1])
        mbpython=miniblink.Miniblink
        try:
            with codecs.open("C:/TkWebPage.txt","r") as o:
                mb = mbpython.init(o.read())
        except:
            try:
                if platform.machine() == "AMD64":
                    mb=mbpython.init('/miniblink_x64.dll')
                    with codecs.open("C:/TkWebPage.txt","w") as o:
                        o.write("/miniblink_x64.dll")
                else:
                    mb=mbpython.init('/node.dll')
                    with codecs.open("C:/TkWebPage.txt","w") as o:
                        o.write("/node.dll")
            except:
                try:
                    if platform.machine() == "AMD64":
                        mb=mbpython.init('/Lib/site-packages/TkWebPage/miniblink_x64.dll')
                        with codecs.open("C:/TkWebPage.txt","w") as o:
                            o.write("/Lib/site-packages/TkWebPage/miniblink_x64.dll")
                    else:
                        mb=mbpython.init('/Lib/site-packages/TkWebPage/node.dll')
                        with codecs.open("C:/TkWebPage.txt","w") as o:
                            o.write("/Lib/site-packages/TkWebPage/node.dll")
                except:
                    try:
                        if platform.machine() == "AMD64":
                            mb=mbpython.init('./Lib/site-packages/TkWebPage/miniblink_x64.dll')
                            with codecs.open("C:/TkWebPage.txt","w") as o:
                                o.write("./Lib/site-packages/TkWebPage/miniblink_x64.dll")
                        else:
                            mb=mbpython.init('./Lib/site-packages/TkWebPage/node.dll')
                            with codecs.open("C:/TkWebPage.txt","w") as o:
                                o.write("./Lib/site-packages/TkWebPage/node.dll")
                    except:
                        try:
                            if platform.machine() == "AMD64":
                                mb=mbpython.init('./miniblink_x64.dll')
                                with codecs.open("C:/TkWebPage.txt","w") as o:
                                    o.write("./miniblink_x64.dll")
                            else:
                                mb=mbpython.init('./node.dll')
                                with codecs.open("C:/TkWebPage.txt","w") as o:
                                    o.write("./node.dll")
                        except:
                            print("找不到您的地址，请输入您把次模块下载的地址（例：C:\\Users\\TkWebPage，输入：C:/Users/TkWebPage/）")
                            if platform.machine() == "AMD64":
                                file = input(">>>")+'miniblink_x64.dll'
                            else:
                                file = input(">>>")+'node.dll'
                            mb=mbpython.init(file)
                            with codecs.open("C:/TkWebPage.txt","w") as o:
                                o.write(file)
        wke=mbpython(mb)
        window=wke.window
        webview=window.wkeCreateWebWindow(2,a.winfo_id(),0,0,a.winfo_width(),a.winfo_height())
        mb.wkeLoadURLW(webview,dictionary[name][0])
        window.wkeShowWindow(webview)
        a.mainloop()
        return dictionary[name]
