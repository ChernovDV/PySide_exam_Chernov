import json
import sys
from random import choice
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


# ---------- Определение модели плитки ----------
class Tile(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = None
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 24))
        # Гибкая политика размера для адаптации
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(50, 50)  # Минимальная ширина плитки
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.update_style()

    def set_value(self, val):
        self.value = val
        self.setText(str(val)) if val else self.clear()
        self.update_style()

    def update_style(self):
        colors = {
            None: "#BBADA0",
            2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61",
            512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }
        bg_color = colors.get(self.value, "#BBADA0")
        fg_color = "black" if isinstance(self.value, int) and self.value <= 4 else "white"
        style = f"QLabel {{ background-color: {bg_color}; color: {fg_color}; }}"
        self.setStyleSheet(style)


# ---------- Логика игры ----------
class GameLogic:
    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.score = 0

    def reset(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.score = 0

    def place_new_tile(self):
        empty_spots = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] is None]
        if empty_spots:
            pos = choice(empty_spots)
            self.board[pos[0]][pos[1]] = 2

    def merge_row(self, row):
        temp = [val for val in row if val is not None]
        result = []
        i = 0
        while i < len(temp):
            if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                result.append(temp[i] * 2)
                self.score += temp[i] * 2
                i += 2
            else:
                result.append(temp[i])
                i += 1
        return result + [None] * (len(row) - len(result))

    def move_left(self):
        changed = False
        for i in range(4):
            old_row = list(self.board[i])
            new_row = self.merge_row(old_row)
            if old_row != new_row:
                changed = True
            self.board[i] = new_row
        return changed

    def rotate(self):
        n = len(self.board)
        rotated = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = self.board[i][j]
        self.board = rotated

    def can_move(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] is None:
                    return True
                if (i > 0 and self.board[i][j] == self.board[i - 1][j]) or (
                        j > 0 and self.board[i][j] == self.board[i][j - 1]):
                    return True
        return False


# ---------- Виджет игры ----------
class GameView(QWidget):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.best_scores = []  # Лучшие результаты
        self.load_best_scores()
        self.init_ui()

    def load_best_scores(self):
        try:
            with open("best_scores.json", "r") as file:
                data = json.load(file)
                self.best_scores = sorted(data["scores"], reverse=True)[:5]
        except FileNotFoundError:
            pass

    def save_best_scores(self):
        scores_data = {"scores": self.best_scores}
        with open("best_scores.json", "w") as file:
            json.dump(scores_data, file)

    def show_best_scores(self):
        message = "\n".join([f"{score}" for score in self.best_scores])
        QMessageBox.information(self, "Лучшие результаты", message)

    def init_ui(self):
        layout = QVBoxLayout()
        score_label = QLabel(f"Счёт: {self.logic.score}")
        layout.addWidget(score_label)

        grid = QGridLayout()
        self.tiles = [[Tile() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                grid.addWidget(self.tiles[i][j], i, j)
        layout.addLayout(grid)

        # Создаем горизонтальное распределение для двух кнопок
        button_layout = QHBoxLayout()
        restart_btn = QPushButton("Новая игра")
        restart_btn.clicked.connect(self.reset_game)
        button_layout.addWidget(restart_btn)

        best_scores_btn = QPushButton("Лучшие результаты")
        best_scores_btn.clicked.connect(self.show_best_scores)
        button_layout.addWidget(best_scores_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.update_view()

    def on_move(self, direction):
        if direction == 'left':
            self.logic.move_left()
        elif direction == 'right':
            self.logic.rotate();
            self.logic.rotate();
            self.logic.move_left();
            self.logic.rotate();
            self.logic.rotate()
        elif direction == 'up':
            self.logic.rotate();
            self.logic.rotate();
            self.logic.rotate();
            self.logic.move_left();
            self.logic.rotate()
        elif direction == 'down':
            self.logic.rotate();
            self.logic.move_left();
            self.logic.rotate();
            self.logic.rotate();
            self.logic.rotate()
        self.logic.place_new_tile()
        self.update_view()
        if not self.logic.can_move():
            QMessageBox.information(self, "", "Игра закончена!")
            self.save_result()

    def reset_game(self):
        self.logic.reset()
        self.update_view()

    def update_view(self):
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].set_value(self.logic.board[i][j])
        score_label = self.layout().itemAt(0).widget()
        score_label.setText(f"Счёт: {self.logic.score}")

    def save_result(self):
        current_score = self.logic.score
        if current_score > 0:
            self.best_scores.append(current_score)
            self.best_scores.sort(reverse=True)
            self.best_scores = self.best_scores[:5]
            self.save_best_scores()


# ---------- Главное окно приложения ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра 2048")
        # Позволяет оконному менеджеру самостоятельно определять размеры окна
        self.resize(400, 300)
        # Получение фокуса клавиатуры
        self.setFocusPolicy(Qt.StrongFocus)
        self.game_logic = GameLogic()
        self.game_view = GameView(self.game_logic)
        self.setCentralWidget(self.game_view)
        self.game_logic.place_new_tile()
        self.game_logic.place_new_tile()
        self.game_view.update_view()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.game_view.on_move('up')
        elif event.key() == Qt.Key_Left:
            self.game_view.on_move('left')
        elif event.key() == Qt.Key_Right:
            self.game_view.on_move('right')
        elif event.key() == Qt.Key_Down:
            self.game_view.on_move('down')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())