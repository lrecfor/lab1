import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal
from multiprocessing import Process, Queue
import time


class Planet:
    def __init__(self, name, start_x, start_y, speed_factor, queue, orbit_x, orbit_y):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.angle = 0
        self.speed_factor = speed_factor
        self.queue = queue
        self.orbit_x = orbit_x
        self.orbit_y = orbit_y

    def update_position(self):
        while True:
            self.x = round(self.orbit_x * math.cos(self.angle)) + 1920 // 2
            self.y = round(self.orbit_y * math.sin(self.angle)) + 1051 // 2

            self.angle += 0.05 * self.speed_factor

            if self.angle > 6.28:
                self.angle = 0

            self.queue.put((self.x, self.y))

            time.sleep(0.05)


class PlanetWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Ellipse Animation')
        self.showMaximized()

        self.queues = [Queue() for _ in range(8)]

        speeds = [0.47 * 3, 0.35 * 3, 0.3 * 3, 0.24 * 3, 0.13 * 3, 0.097 * 3, 0.068 * 3,
                  0.054 * 3]

        self.mercury = Planet(name='Mercury', start_x=350, start_y=self.height() // 2,
                              speed_factor=speeds[0],
                              queue=self.queues[0],
                              orbit_x=160,
                              orbit_y=90)
        self.process_mercury = Process(target=self.mercury.update_position)

        self.venus = Planet(name='Venus', start_x=400, start_y=self.height() // 2,
                            speed_factor=speeds[1],
                            queue=self.queues[1],
                            orbit_x=200,
                            orbit_y=130)
        self.process_venus = Process(target=self.venus.update_position)

        self.earth = Planet(name='Earth', start_x=450, start_y=self.height() // 2,
                            speed_factor=speeds[2],
                            queue=self.queues[2],
                            orbit_x=350,
                            orbit_y=250)
        self.process_earth = Process(target=self.earth.update_position)

        self.mars = Planet(name='Mars', start_x=500, start_y=self.height() // 2,
                           speed_factor=speeds[3],
                           queue=self.queues[3],
                           orbit_x=400,
                           orbit_y=300)
        self.process_mars = Process(target=self.mars.update_position)

        self.jupiter = Planet(name='Jupiter', start_x=570, start_y=self.height() // 2,
                              speed_factor=speeds[4],
                              queue=self.queues[4],
                              orbit_x=470,
                              orbit_y=370)
        self.process_jupiter = Process(target=self.jupiter.update_position)

        self.saturn = Planet(name='Saturn', start_x=730, start_y=self.height() // 2,
                             speed_factor=speeds[5],
                             queue=self.queues[5],
                             orbit_x=620,
                             orbit_y=430)
        self.process_saturn = Process(target=self.saturn.update_position)

        self.uranus = Planet(name='Uranus', start_x=830, start_y=self.height() // 2,
                             speed_factor=speeds[6],
                             queue=self.queues[6],
                             orbit_x=650,
                             orbit_y=490)
        self.process_uranus = Process(target=self.uranus.update_position)

        self.neptune = Planet(name='Neptune', start_x=930, start_y=self.height() // 2,
                              speed_factor=speeds[7],
                              queue=self.queues[7],
                              orbit_x=730,
                              orbit_y=515)
        self.process_neptune = Process(target=self.neptune.update_position)

        self.process_mercury.start()
        self.process_venus.start()
        self.process_earth.start()
        self.process_mars.start()
        self.process_jupiter.start()
        self.process_saturn.start()
        self.process_uranus.start()
        self.process_neptune.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), Qt.white)

        sun_x = self.width() // 2 - 70
        sun_y = self.height() // 2 - 70
        painter.setBrush(QColor(255, 255, 0))
        painter.drawEllipse(sun_x, sun_y, 140, 140)

        planet_sizes = {
            'Mercury': 6,
            'Venus': 8,
            'Earth': 10,
            'Mars': 7,
            'Jupiter': 30,
            'Saturn': 25,
            'Uranus': 20,
            'Neptune': 20
        }

        planet_colors = {
            'Mercury': QColor(255, 204, 102),
            'Venus': QColor(255, 153, 51),
            'Earth': QColor(0, 102, 255),
            'Mars': QColor(204, 51, 0),
            'Jupiter': QColor(255, 204, 153),
            'Saturn': QColor(255, 204, 0),
            'Uranus': QColor(0, 153, 204),
            'Neptune': QColor(0, 102, 204)
        }

        # Отображение планет
        for i, queue in enumerate(self.queues):
            if not queue.empty():
                x, y = queue.get()
                planet_name = \
                    ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'][
                        i]
                color = planet_colors[planet_name]
                painter.setBrush(color)
                planet_size = planet_sizes[planet_name]
                painter.drawEllipse(x - planet_size // 2, y - planet_size // 2, planet_size,
                                    planet_size)

    def closeEvent(self, event):
        for process in [self.process_mercury, self.process_venus, self.process_earth,
                        self.process_mars,
                        self.process_jupiter, self.process_saturn, self.process_uranus,
                        self.process_neptune]:
            process.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlanetWidget()
    window.show()
    sys.exit(app.exec())
