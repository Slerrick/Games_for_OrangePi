import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
#import wiringpi;
#from wiringpi import GPIO;
import random as rd
import json

# Настройка GPIO
# (Этот раздел пока не используется, добавьте код для управления GPIO, если необходимо)

#wiringpi.wiringPiSetup();
#wiringpi.setwarnings = False

#INIT GPIO

PIN_WIN = 7  # GPIO-пин для сигнала победы       green / 7 pin
PIN_LOSE = 12 # GPIO-пин для сигнала поражения   red / 12 pin

#ARRAY_GPIO = [PIN_LOSE, PIN_WIN];
#for Num in ARRAY_GPIO:
#    wiringpi.pinMode(Num, GPIO.OUTPUT);
#    print(wiringpi.digitalRead(Num));

# Функция для генерации случайного результата
def generate_result():
    return "Орёл" if rd.randint(0, 1) == 0 else "Решка"

# Функция для обработки нажатия кнопок
def button_clicked(button_text):
    global wins, losses
    result = generate_result()

    if button_text == result:
        # Победа
        label.setText(f"Победа! Выпал {result}")
        wins += 1
        #GPIO.output(PIN_WIN, GPIO.HIGH)  # Включить пин победы
    else:
        # Поражение
        label.setText(f"Поражение! Выпал {result}")
        losses += 1
        #GPIO.output(PIN_LOSE, GPIO.HIGH) # Включить пин поражения

    update_score()  # Обновление счетчика
    # Деактивация GPIO-пинов после 1 секунды
    #QTimer.singleShot(1000, lambda: GPIO.output(PIN_WIN, GPIO.LOW))
    #QTimer.singleShot(1000, lambda: GPIO.output(PIN_LOSE, GPIO.LOW))

# Функция для обновления счетчика
def update_score():
    score_label.setText(f"Победы: {wins}, Поражения: {losses}")

# Функция для сохранения статистики
def save_stats():
    data = {"wins": wins, "losses": losses}
    try:
        with open("stats.json", "w") as f:
            json.dump(data, f)
        QMessageBox.information(window, "Сохранение", "Статистика сохранена!")
    except Exception as e:
        QMessageBox.critical(window, "Ошибка", f"Не удалось сохранить статистику: {e}")

# Функция для загрузки статистики
def load_stats():
    global wins, losses
    try:
        with open("stats.json", "r") as f:
            data = json.load(f)
            wins = data["wins"]
            losses = data["losses"]
            update_score()
    except FileNotFoundError:
        QMessageBox.information(window, "Загрузка", "Файл статистики не найден.")
    except Exception as e:

        QMessageBox.critical(window, "Ошибка", f"Не удалось загрузить статистику: {e}")

# Функция для изменения правил игры
def change_rules():
    global rules
    new_rules = rules_input.text()
    if new_rules:
        rules = new_rules.split(",")
        rules_label.setText(f"Правила игры: {', '.join(rules)}")
    else:
        QMessageBox.warning(window, "Предупреждение", "Введите правила игры!")

# Создание основного окна приложения
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Орёл или решка")

# Настройка стиля
window.setStyleSheet("""
    QWidget {
        background-color: #C0D8E2; /* Серый-голубой фон */
        height: 400px;
        width: 700px;
    }

    QLabel {
        font-size: 74px; /* Увеличить размер текста */
        font-weight: bold;
        color: #282c34; /* Тёмно-серый цвет текста */
    }

    QPushButton {
        background-color: #5099D5; /* Синий цвет кнопок */
        color: white;
        font-size: 50px;
        padding: 10px 20px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #4284C2; /* Тёмно-синий цвет при наведении */
    }

    QLineEdit {
        padding: 5px;
        border: 6px solid #000;
        font-size: 20px;
    }
""")

# Создание элементов интерфейса
label = QLabel("Нажмите кнопку")
label.setAlignment(Qt.AlignCenter)  # Выравнивание текста по центру
button_eagle = QPushButton("Орёл")
button_tails = QPushButton("Решка")
score_label = QLabel("Победы: 0, Поражения: 0")
save_button = QPushButton("Сохранить")
load_button = QPushButton("Загрузить")
rules_label = QLabel("Правила игры: Орёл, Решка")
change_rules_button = QPushButton("Изменить правила")
rules_input = QLineEdit()

# Начальные значения
wins = 0
losses = 0
rules = ["Орёл", "Решка"]

# Подключение сигналов к слотам
button_eagle.clicked.connect(lambda: button_clicked("Орёл"))
button_tails.clicked.connect(lambda: button_clicked("Решка"))
save_button.clicked.connect(save_stats)
load_button.clicked.connect(load_stats)
change_rules_button.clicked.connect(change_rules)

# Размещение элементов в layout
hbox1 = QHBoxLayout()
hbox1.addWidget(button_eagle)
hbox1.addWidget(button_tails)

hbox2 = QHBoxLayout()
hbox2.addWidget(save_button)
hbox2.addWidget(load_button)

hbox3 = QHBoxLayout()
hbox3.addWidget(change_rules_button)
hbox3.addWidget(rules_input)

vbox = QVBoxLayout()
vbox.addWidget(label)
vbox.addLayout(hbox1)
vbox.addWidget(score_label)
vbox.addLayout(hbox2)
vbox.addWidget(rules_label)
vbox.addLayout(hbox3)
vbox.addStretch(1)

window.setLayout(vbox)

# Настройка размера шрифта в зависимости от размера окна
def resizeEvent(event):
    label.setFont(QFont("Arial", window.width() // 10))  # Размер шрифта в зависимости от ширины окна
    button_eagle.setFont(QFont("Arial", window.width() // 15))
    button_tails.setFont(QFont("Arial", window.width() // 15))
    score_label.setFont(QFont("Arial", window.width() // 20))
    rules_label.setFont(QFont("Arial", window.width() // 20))
    change_rules_button.setFont(QFont("Arial", window.width() // 20))
    rules_input.setFont(QFont("Arial", window.width() // 20))

window.resizeEvent = resizeEvent  # Задайте обработчик изменения размера

# Отображение окна приложения
window.show()

sys.exit(app.exec_())

# Очистка GPIO-пинов при выходе из программы
#GPIO.cleanup()