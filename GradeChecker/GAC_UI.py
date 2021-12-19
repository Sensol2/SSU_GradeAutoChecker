import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from GAC import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야 함
form_class = uic.loadUiType('.\CoreFiles\GAC.ui')[0]

class PlayThread(QThread, QObject): #쓰레딩
    # 시그널 정의
    signal_AddLogMessage = pyqtSignal(str)
    signal_StopFunc = pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self.main = parent
        self.isRun = False
        self.id = None
        self.pw = None
        self.windowHideMode = False  # 윈도우 숨김모드
        self.notificaionMode = False # 알림 수신 여부
        self.termHour = 1            # 알림 보내는 주기(시간)
    
    def InitUserData(self, user_id, user_pw):   # 유저 정보 저장
        self.id = user_id
        self.pw = user_pw
    
    def run(self):
        mainFunc(self)
        self.signal_StopFunc.emit()


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()

        # 스레드 선언 및 시그널 연결
        self.th = PlayThread(self)
        self.th.signal_AddLogMessage.connect(self.AddLogMessage)
        self.th.signal_StopFunc.connect(self.StopFunc)

        # UI 커넥트
        self.setupUi(self)
        self.Button_Start.clicked.connect(self.StartFunc)
        self.Button_Login.clicked.connect(self.LoginFunc)
        self.Button_clearLog.clicked.connect(self.ClearLog)

    def StartFunc(self):
        self.th.start()
        self.Button_Start.setDisabled(True)
        self.AddLogMessage("성적을 불러오겠습니다. 잠시만 기다려주세요..")

    def StopFunc(self):
        self.Button_Start.setDisabled(False)
        self.AddLogMessage("완료!")

    def LoginFunc(self):
        _id = self.input_ID.text()
        _pw = self.input_PW.text()

        if not _id or not _pw:
            self.AddLogMessage('로그인 정보가 비어있습니다!')
        else:
            self.AddLogMessage('로그인 정보가 성공적으로 입력되었습니다!')
            self.th.InitUserData(_id, _pw)  #쓰레드 멤버 변수에 추가
            self.Button_Start.setDisabled(False)

    def AddLogMessage(self, string):
        self.textbox_Log.append(string)

    def ClearLog(self):
        self.textbox_Log.clear()
        self.AddLogMessage('로그 청소 완료!')

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()