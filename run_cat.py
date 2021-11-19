import json
import os
import sys
from functools import partial

import psutil
from PySide6.QtCore import QTimer, QCoreApplication, QSettings
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu


class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)

        self.current_index = 0
        self.current_icons = []

        self.init_setting()
        self.init_ui()

        self.cpu_timer = QTimer(self)
        self.cpu_timer.setInterval(3000)
        self.cpu_timer.timeout.connect(self.cpu_tick)
        self.cpu_timer.start()

        self.animate_timer = QTimer(self)
        self.animate_timer.setInterval(200)
        self.animate_timer.timeout.connect(self.update_animate)
        self.animate_timer.start()

    def init_setting(self):
        self.settings = QSettings('runcat.ini', QSettings.IniFormat)
        if not self.settings.contains("current_theme"):
            self.settings.setValue('current_theme', '白猫')

        self.themes_path = dict()

        scan_path = self.resource_path(os.path.join('resources', 'themes'))
        g = os.walk(scan_path)
        for path, dir_list, file_list in g:
            for dir_name in dir_list:
                self.themes_path[dir_name] = self.resource_path(os.path.join(path, dir_name))

        with open(self.resource_path(os.path.join('resources', 'themes', 'speed.json')), 'r', encoding='utf-8') as f:
            speed_data = f.read()
        self.speed = json.loads(speed_data)

    def init_ui(self):
        self.tp_menu = QMenu()
        self.theme_menu = QMenu()
        self.theme_menu.setTitle('切换主题')
        self.themes_action = dict()

        for item in self.themes_path:
            action = QAction(item, self)
            action.setCheckable(True)
            action.triggered.connect(partial(self.change_theme, action))
            self.themes_action[item] = action
            self.theme_menu.addAction(action)

        self.tp_menu.addMenu(self.theme_menu, )

        self.auto_startup_act = QAction('开机启动')
        self.auto_startup_act.setCheckable(True)
        auto_startup_bool = self.settings.value("auto_startup", True, type=bool)
        self.auto_startup_act.setChecked(auto_startup_bool)
        self.settings.setValue('auto_startup', auto_startup_bool)
        self.settings.sync()

        self.auto_startup_act.triggered[bool].connect(self.auto_startup)

        self.exit_act = QAction('退出', self, triggered=self.quit_app)
        self.tp_menu.addAction(self.auto_startup_act)
        self.tp_menu.addAction(self.exit_act)

        self.setIcon(QIcon(self.resource_path(os.path.join('runcat.ico'))))
        self.setToolTip(u'CPU使用率 ' + str(psutil.cpu_percent(None)) + '%')

        self.change_theme(None)
        self.setContextMenu(self.tp_menu)

    def update_animate(self):
        if len(self.current_icons) == 0:
            return
        if len(self.current_icons) <= self.current_index:
            self.current_index = 0
        self.setIcon(self.current_icons[self.current_index])
        self.current_index = (self.current_index + 1) % len(self.current_icons)

    def cpu_tick(self):
        cpu_usage = self.get_cpu_usage()
        self.setToolTip(cpu_usage[1])

        interval = 200.0 / max(1, min(20, cpu_usage[0] / 5))

        current_theme = self.settings.value('current_theme')
        speed_rate = 1
        if current_theme in self.speed.keys():
            speed_rate = self.speed[current_theme]

        speed_fps = int(interval * speed_rate)

        self.animate_timer.stop()
        self.animate_timer.setInterval(speed_fps)
        self.animate_timer.start()

    def change_theme(self, action):
        new_theme = self.settings.value('current_theme')
        if action is not None:
            new_theme = action.text()

        self.settings.setValue('current_theme', new_theme)
        self.settings.sync()

        for (name, _action) in self.themes_action.items():
            _action.setChecked(new_theme == name)

        g = os.walk(self.resource_path(self.themes_path[new_theme]))
        self.current_icons = []
        for path, dir_list, file_list in g:
            for file_name in file_list:
                icon_path = self.resource_path(os.path.join(path, file_name))
                self.current_icons.append(QIcon(icon_path))

    def get_cpu_usage(self):
        percent = psutil.cpu_percent(None)
        return (percent, str(percent) + '%',)

    def auto_startup(self, checked):
        self.auto_startup_act.setChecked(checked)
        self.settings.setValue('auto_startup', checked)
        self.settings.sync()

    def quit_app(self):
        self.cpu_timer.stop()
        self.animate_timer.stop()
        QCoreApplication.instance().quit()
        self.setVisible(False)

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):  # 是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            # base_path = os.path.abspath(".")
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    QApplication.setQuitOnLastWindowClosed(False)

    w = QWidget()
    tray = TrayIcon(w)
    tray.show()

    sys.exit(app.exec())
