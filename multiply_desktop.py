import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from random import randrange

app = None

class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.setWindowTitle("Учим таблицу умножения")

    self.answers = []
    self.questions_count = 30
    self.current_question = 0
    self.good_answers = 0
    self.timer_count = 0
    self.prev_timer_count = 0

    self.header_label = QLabel()
    self.header_label.setAlignment(Qt.AlignCenter)
    self.question_label = QLabel()
    self.question_label.setAlignment(Qt.AlignCenter)
    self.update_question()

    self.timer_label = QLabel()
    self.timer_label.setAlignment(Qt.AlignCenter)

    self.line_edit = QLineEdit(self)
    self.line_edit.setValidator(QIntValidator(1, 99))
    self.answer_button = QPushButton("&Ответить", self)
    self.line_edit.returnPressed.connect(self.answer_button.click)

    self.progress = QProgressBar(self)
    self.progress.setGeometry(0, 0, 300, 25)
    self.progress.setMaximum(self.questions_count)

    self.answer_button.clicked.connect(self.on_answer)

    main_layout = QVBoxLayout()

    main_layout.addWidget(self.header_label)
    main_layout.addWidget(self.progress)
    main_layout.addWidget(self.timer_label)
    main_layout.addWidget(self.question_label)
    main_layout.addWidget(self.line_edit)
    main_layout.addWidget(self.answer_button)

    self.timer = QTimer()
    self.timer.timeout.connect(self.update_elapsed_time)
    self.timer.start(1000)

    widget = QWidget()
    widget.setLayout(main_layout)

    self.resize(400, 200)
    self.setCentralWidget(widget)

  def update_elapsed_time(self):
    self.timer_count += 1
    minutes, seconds = divmod(self.timer_count, 60)
    self.timer_label.setText("{}:{}".format(minutes, seconds))

  def update_question(self):
    self.x, self.y = (randrange(1, 10), randrange(1, 10))
    self.header_label.setText("Вопрос {} из {}".format(self.current_question, self.questions_count))
    self.question_label.setText("Cколько будет {} * {}?".format(self.x, self.y))

  def reset_form(self):
    self.progress.setValue(0)
    self.good_answers = 0
    self.current_question = 0
  
  def show_dialog(self):
    self.modal_window = QDialog()
    self.modal_window.setWindowTitle("Результаты")
    self.modal_window.setWindowModality(Qt.ApplicationModal)
    self.modal_window.resize(900, 270)

    stats, feedback, elapsed_text, button_text = self.choose_result_text()

    self.result_feedback = QLabel(self.modal_window)
    self.result_feedback.setText(feedback)
    self.result_label = QLabel(self.modal_window)
    self.result_label.setText(stats)
    self.elapsed_time_label = QLabel(self.modal_window)
    self.elapsed_time_label.setText(elapsed_text)
    self.ok_button = QPushButton(button_text, self.modal_window)
    self.ok_button.clicked.connect(self.on_ok_button_click)

    self.tableWidget = QTableWidget()
    self.tableWidget.setRowCount(4)
    self.tableWidget.setColumnCount(self.questions_count)

    for n, answer in enumerate(self.answers):
      x, y, a, r, t = answer
      self.tableWidget.setItem(0, n, QTableWidgetItem("{} * {}".format(x, y)))
      self.tableWidget.setItem(1, n, QTableWidgetItem(str(a)))
      result_item = QTableWidgetItem()
      if r:
        result_item.setText("+")
        result_item.setForeground(QBrush(QColor(0, 255, 0)))
      else:
        result_item.setText("-")
        result_item.setForeground(QBrush(QColor(255, 0, 0)))
      self.tableWidget.setItem(2, n, result_item)
      self.tableWidget.setItem(3, n, QTableWidgetItem("{}с".format(t)))

    self.tableWidget.resizeColumnsToContents()
    self.tableWidget.resizeRowsToContents()

    modal_layout = QVBoxLayout()
    modal_layout.addWidget(self.result_feedback)
    modal_layout.addWidget(self.result_label)
    modal_layout.addWidget(self.elapsed_time_label)
    modal_layout.addWidget(self.tableWidget)
    modal_layout.addWidget(self.ok_button)

    self.modal_window.setLayout(modal_layout)
    self.modal_window.exec_()

  def on_ok_button_click(self):
    self.reset_form()
    self.timer_count = 0
    self.prev_timer_count = 0
    self.timer.start()
    self.answers = []
    self.modal_window.accept()

  def on_answer(self):
    answer = self.line_edit.text()

    if answer:
      int_answer = int(answer)

      is_right = int_answer == self.x * self.y
      if is_right:
        self.good_answers += 1

      answer_time = self.timer_count - self.prev_timer_count
      self.prev_timer_count = self.timer_count
      self.answers.append((self.x, self.y, int_answer, is_right, answer_time))

      self.current_question += 1
      self.progress.setValue(self.current_question)
      self.line_edit.setText("")
      self.update_question()

      if self.current_question >= self.questions_count:
        self.timer.stop()
        self.show_dialog()

  def choose_result_text(self):
    stats = "Правильных ответов {} из {} вопросов.".format(self.good_answers, self.questions_count)
    feedback = ""
    button_text = ""

    if self.good_answers < self.questions_count // 3:
      button_text = "Не буду баловаться!"
      feedback = "Перестань баловаться! 8-(=) "
    elif self.good_answers < self.questions_count // 2:
      button_text = "Ой, как стыдно.. исправлюсь!"
      feedback = "Как тебе не стыдно! 8-( "
    elif self.good_answers < round(self.questions_count * 0.8):
      button_text = "Постараюсь получше!"
      feedback = "Плоховато, ты можешь лучше! 8-/ "
    elif self.good_answers < self.questions_count:
      button_text = "Сейчас сделаю без ошибок!"
      feedback = "Ты просто умничка, класс, ты просто молодец! 8-) "
    elif self.good_answers == self.questions_count:
      button_text = "Попробую повторить успех!"
      feedback = """Зимой ты получишь собаку и для нее одежду, потому что ты просто умница! :-) :-)
      Конечно если 182 дня будешь за котом смотреть.. (от папы)"""

    minutes, seconds = divmod(self.timer_count, 60)
    elapsed_time_text = "Выполнено за {} минут {} секунд".format(minutes, seconds)

    return (stats, feedback, elapsed_time_text, button_text)

def main():
    global app

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec()

if __name__ == '__main__':
    main()
