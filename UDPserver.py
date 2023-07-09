from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt6 import uic, QtGui
import cv2, imutils, socket
import numpy as np
import time
import base64

class MyGui (QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("UdpServer.ui",self)
        self.show()
        self.current_file = "starship.mp4"
        #self.setFixedSize(pixmap.width(), pixmap.height())
        self.label.setMinimumSize(1,1)
        self.actionOpen_Video.triggered.connect(self.open_video)
        self.BeginTranslation.clicked.connect(self.Translate_Button)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        self.textEdit.setPlainText(host_ip)

    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Video File (*.mp4 )")
        if filename != "":
            self.current_file = filename

    def Translate_Button(self):
        BUFF_SIZE = 65536
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(host_ip)
        port = int(self.textEdit_2.toPlainText())
        #port = 9999
        socket_address = (host_ip, port)
        server_socket.bind(socket_address)
        print('Listening at:', socket_address)
        vid = cv2.VideoCapture(self.current_file)
        #vid = cv2.VideoCapture('starship.mp4')  # replace 'starship.mp4' with 0 for webcam
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)

        while True:
            msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from', client_addr)
            WIDTH = 400
            while (vid.isOpened()):
                _, frame = vid.read()
                frame = imutils.resize(frame, width=WIDTH)
                encode, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                message = base64.b64encode(buffer)
                server_socket.sendto(message, client_addr)
                frame = cv2.putText(frame, 'FPS :' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow('TRANSMITTING VIDEO', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    server_socket.close()
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
