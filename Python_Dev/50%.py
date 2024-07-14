import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QTimer
import wiringpi;
from wiringpi import GPIO;
import random as rd

# Настройка GPIO

wiringpi.wiringPiSetup();
wiringpi.setwarnings = False

#INIT GPIO

PIN_WIN = 2  # GPIO-пин для сигнала победы      green / 7 pin
PIN_LOSE = 6 # GPIO-пин для сигнала поражения   red / 12 pin

ARRAY_GPIO = [PIN_LOSE, PIN_WIN];
for Num in ARRAY_GPIO:
    wiringpi.pinMode(Num, GPIO.OUTPUT);
    print(wiringpi.digitalRead(Num));

# Функция для генерации случайного результата
def generate_result():
    return "Орёл" if rd.randint(0, 1) == 0 else "Решка"

# Функция для обработки нажатия кнопок
def button_clicked(button_text):
    result = generate_result()

    if button_text == result:
        # Победа
        label.setText(f"Победа! Выпал {result}")
        GPIO.output(PIN_WIN, GPIO.HIGH)
    else:
        # Поражение
        label.setText(f"Поражение! Выпал {result}")
        GPIO.output(PIN_LOSE, GPIO.HIGH)

    # Деактивация GPIO-пинов после 1 секунды
    QTimer.singleShot(1000, lambda: GPIO.output(PIN_WIN, GPIO.LOW))
    QTimer.singleShot(1000, lambda: GPIO.output(PIN_LOSE, GPIO.LOW))

# Создание основного окна приложения
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Орёл или решка")

# Создание элементов интерфейса
label = QLabel("Нажмите кнопку")
button_eagle = QPushButton("Орёл")
button_tails = QPushButton("Решка")

# Подключение сигналов к слотам
button_eagle.clicked.connect(lambda: button_clicked("Орёл"))
button_tails.clicked.connect(lambda: button_clicked("Решка"))

# Размещение элементов в layout
hbox = QHBoxLayout()
hbox.addWidget(button_eagle)
hbox.addWidget(button_tails)

vbox = QVBoxLayout()
vbox.addWidget(label)
vbox.addLayout(hbox)

window.setLayout(vbox)

# Отображение окна приложения
window.show()

sys.exit(app.exec_())

# Очистка GPIO-пинов при выходе из программы
GPIO.cleanup()