import string
import sys
from math import log10
# 添加上一级，防止ffmpeg调用出bug
# 在Release里面可以考虑把ffmpeg整合进来
sys.path.append("../ffmpeg")
sys.path.append("./ffmpeg")

# 导入实际工作的api
import encapsulation as en

from modules import *
from widgets import *


# 自定义的日志打印窗口

from logWindow import LogWindow

#os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
# 以上的那一行必须禁用

widgets = None
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

class ThreadFor3rdPartyFunctions (QThread):

    T3_VIDEO = 0
    T3_BULLETCHAT = 1
    T3_LIKE = 2
    T3_SEARCH = 3
    T3_SEARCH_DW = 4

    pa = None
    pa_d = None
    returnBuffer = None
    def __init__(self):
        """
        logWindow: 用于显示
        """
        super(ThreadFor3rdPartyFunctions, self).__init__()

    def selectFunction(self, x):
        self.fu = x

    def setParameter(self, p:string):
        self.pa = p

    def setParameterD(self, p:dict):
        self.pa_d = p

    def setLog(self, lw: LogWindow):
        self.lw: LogWindow = lw

    def run(self):

        """
        这里通过前面的方法设定线程参数
        """
        if self.fu == self.T3_VIDEO:
            en.ec_video.execute(self.pa, self.lw)
            widgets.url_ensure.setEnabled(True)
        if self.fu == self.T3_BULLETCHAT:
            en.ec_bulletChat.execute(self.pa, self.lw)
            widgets.cid_ensure.setEnabled(True)
        if self.fu == self.T3_SEARCH:
            self.returnBuffer = en.ec_search.search(self.pa)
            """
            以下添加排序代码，最后返回的就是排序后的数据力
            """
            for index, elements in enumerate(self.returnBuffer):
                self.returnBuffer[index] = [elements, 0] # 为原始的数据添加一个score项
                bvid = elements["bvid"]
                data = en.ec_like.execute_bv_notSave(bvid)
                self.returnBuffer[index][1] = log10(float(data["view"])+1) \
                                            /8*0.2+log10(float(data["favorite"]+1)) \
                                            /7*0.2+log10(float(data["coin"])+1) \
                                            /6*0.3+log10(float(data["like"])+1) \
                                            /6*0.3
            list.sort(self.returnBuffer,key= lambda x: x[1], reverse = True)
            widgets.kwd_sch.setEnabled(True)
            widgets.kwd_show.setEnabled(True)

        if self.fu == self.T3_SEARCH_DW:
            url = self.pa_d['url']
            cid = self.pa_d['cid']
            en.ec_video.execute(url, self.lw)
            en.ec_bulletChat.execute(cid, self.lw)

        self.lw.clearText()
        self.lw.hide() # 阅后即焚
        self.quit()



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        """
        此处进行一些变量的初始化
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.schBuf = None

        Settings.ENABLE_CUSTOM_TITLE_BAR = True


        """
        自定义描述内容
        """
        title = u"维多利加最可爱了🤤"
        description = "Control Panel for Bilibili Web Spider"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        """
        处理侧边栏的触发
        """
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)


        """
        左侧窗口事件绑定
        """
        widgets.btn_cid.clicked.connect(self.buttonClick)
        widgets.btn_kwd.clicked.connect(self.buttonClick)
        widgets.btn_url.clicked.connect(self.buttonClick)
        widgets.btn_about.clicked.connect(self.buttonClick)

        """
        控制按键事件绑定
        """
        widgets.url_ensure.clicked.connect(self.buttonClick)
        widgets.cid_ensure.clicked.connect(self.buttonClick)
        widgets.kwd_sch.clicked.connect(self.buttonClick)
        

        """
        搜索事件绑定
        """
        widgets.kwd_show.itemDoubleClicked.connect(self.selectItem)

        """
        初始化完成，开始显示
        """
        self.show()


        """
        设定一下特定的样式
        """
        widgets.btn_about.setStyleSheet(UIFunctions.selectMenu(widgets.btn_about.styleSheet()))
        widgets.stackedWidget.setCurrentWidget(widgets.home)

        """
        下载线程的定义
        """
        self.extraThread = ThreadFor3rdPartyFunctions()

        """
        log窗口的定义
        """
        self.lw = LogWindow(self)
        self.lw.hide() # 这里先把窗口进行隐藏
        self.extraThread.setLog(self.lw)




    """
    url 输入事件处理
    """
    def url_ensureClick(self):
        widgets.url_ensure.setEnabled(False)
        
        targetUrl = widgets.url_input.text() # 获取链接输入

        # 显示日志打印窗口 
        self.lw.show()


        """
        这里需要使用之前创建的一个线程对象来调用对应的函数
        """
        self.extraThread.selectFunction(ThreadFor3rdPartyFunctions.T3_VIDEO)
        self.extraThread.setParameter(targetUrl)
        self.extraThread.start()

    """
    cid 输入事件处理
    """
    def cid_ensureClick(self):
        widgets.cid_ensure.setEnabled(False)
        targetCid = widgets.cid_input.text()
        
        self.lw.show()
        self.extraThread.selectFunction(ThreadFor3rdPartyFunctions.T3_BULLETCHAT)
        self.extraThread.setParameter(targetCid)
        self.extraThread.start()
       
    """
    关键词搜索处理——搜索部分
    """
    def kwd_schClick(self):
        widgets.kwd_sch.setEnabled(False)
        widgets.kwd_show.setEnabled(False)

        targetKwd = widgets.kwd_input.text()

        self.lw.show()
        self.lw.log.append("获取搜索数据中……")
        self.lw.redraw = True

        self.extraThread.selectFunction(ThreadFor3rdPartyFunctions.T3_SEARCH)
        self.extraThread.setParameter(targetKwd)
        self.extraThread.start()


        # 等待线程的结束
        while not self.extraThread.isFinished():
            QApplication.processEvents()
            # 不断刷新主线程页面防止阻塞
        
        """
        防止搜索返回空，这里添加try-exception
        """
        try:
            self.schBuf = self.extraThread.returnBuffer.copy()
        except(AttributeError):
            self.schBuf = []
            
        
        """
        此后进行条目的打印输出
        条目的顺序由schBuf中的顺序决定
        """
        widgets.kwd_show.clear() # 先清理门户
        if len(self.schBuf) > 0:
            for index, item in enumerate(self.schBuf):
                qitem = QListWidgetItem()
                qitem.setText(item[0]["title"]
                            .replace("<em class=\"keyword\">", "")
                            .replace("</em>", "")
                            .replace("&amp", "")
                            )
                qitem.setWhatsThis(str(index))
    
                widgets.kwd_show.addItem(qitem)
        else:
            widgets.kwd_show.addItem("空空如也~😢")

    """
    此处放置按钮触发的处理函数
    """
    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_url":
            widgets.stackedWidget.setCurrentWidget(widgets.page_url)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        if btnName == "btn_kwd":
            widgets.stackedWidget.setCurrentWidget(widgets.page_kwd)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        if btnName == "btn_cid":
            widgets.stackedWidget.setCurrentWidget(widgets.page_cid)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        if btnName == "btn_about":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        if btnName == "url_ensure":
            self.url_ensureClick()
        if btnName == "cid_ensure":
            self.cid_ensureClick()
        if btnName == "kwd_sch":
            self.kwd_schClick()

    """
    鼠标点击的事件
    """
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def selectItem(self, selectedQitem):
        """
        这是处理选中了条目后的行为
        """
        widgets.kwd_show.setEnabled(False)
        self.lw.show()

        data = self.schBuf[int(selectedQitem.whatsThis())][0]
        print (f"cid {data['cid']}, url {data['url']}")
        self.extraThread.setParameterD(data)
        self.extraThread.selectFunction(ThreadFor3rdPartyFunctions.T3_SEARCH_DW)

        self.extraThread.start()

        while not self.extraThread.isFinished():
            QApplication.processEvents()


        widgets.kwd_show.setEnabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
