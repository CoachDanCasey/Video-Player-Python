import cv2
import pytesseract
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super(MediaPlayer, self).__init__(parent)

        self.media_path = ""
        self.cap = None
        self.frame = None
        self.annotation_text = ""
        self.annotation_color = (255, 0, 0)  # red
        self.annotation_thickness = 2
        self.annotation_font = cv2.FONT_HERSHEY_SIMPLEX
        self.annotation_scale = 1

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Media Player")
        self.setGeometry(300, 300, 640, 480)

        self.media_label = QLabel("No media selected")
        self.media_label.setAlignment(Qt.AlignCenter)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.valueChanged.connect(self.slider_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.media_label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def play(self):
        if self.media_path:
            self.cap = cv2.VideoCapture(self.media_path)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # 30ms interval
        else:
            print("No media selected")

    def pause(self):
        if self.timer:
            self.timer.stop()

    def stop(self):
        if self.timer:
            self.timer.stop()
        self.cap.release()

    def update_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            # Process the frame here (e.g., perform OCR, add annotations)
            self.process_frame()
            self.display_frame()
        else:
            self.stop()

    def process_frame(self):
    # Perform OCR to recognize text in the frame
    text = pytesseract.image_to_string(self.frame)
    # Add annotations to the frame
    cv2.putText(self.frame, text, (10, 30), self.annotation_font, self.annotation_scale, self.annotation_color, self.annotation_thickness)

    # Check for user input (e.g., mouse clicks)
    if self.mouse_down:
        x, y = self.mouse_pos
        cv2.circle(self.frame, (x, y), 10, (0, 255, 0), 2)  # draw a green circle at the mouse position

    # Check for keyboard presses
    if self.key_pressed == ord('a'):
        self.annotation_text += 'A'
    elif self.key_pressed == ord('b'):
        self.annotation_text += 'B'
    # ...

    # Draw the annotation text
    cv2.putText(self.frame, self.annotation_text, (10, 50), self.annotation_font, self.annotation_scale, self.annotation_color, self.annotation_thickness)
    def display_frame(self):
        height, width, _ = self.frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.media_label.setPixmap(pixmap)

    def slider_changed(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider.value())

if __name__ == "__main__":
    app = QApplication([])
    player = MediaPlayer()
    player.show()
    app.exec_()