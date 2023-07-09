from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt6 import uic, QtGui
import cv2, imutils, socket
import numpy as np
import time
import base64

class MyGui (QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("UdpServer.ui", self)
        self.show()
        # self.setFixedSize(pixmap.width(), pixmap.height())
        self.label.setMinimumSize(1, 1)
        self.BeginTranslation.clicked.connect(self.Translate_Button)

    def Translate_Button(self):
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        host_name = socket.gethostname()
        #host_ip = '10.8.21.142'
        host_ip = self.textEdit.toPlainText()
        print(host_ip)
        port = int(self.textEdit_2.toPlainText())
        #port = 9999
        message = b'Hello'
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        client_socket.sendto(message, (host_ip, port))

        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS :' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('RECEIVING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1



def main():
    app = QApplication([])
    window = MyGui()
    app.exec()


if __name__ == "__main__":
    main()

