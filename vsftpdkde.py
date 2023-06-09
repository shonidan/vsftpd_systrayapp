#!/usr/bin/python
import socket
import subprocess
import pyperclip
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import time

"""
App by C0MODIN
"""
icon_white = ("/opt/vsftpd_systrayapp/icons/vsftpdkde_white.png")
icon_black = ("/opt/vsftpd_systrayapp/icons/vsftpdkde_black.png")
icon_green = ("/opt/vsftpd_systrayapp/icons/vsftpdkde_green.png")
icon_red = ("/opt/vsftpd_systrayapp/icons/vsftpdkde_red.png")

# Obtener el nombre de host de la máquina
hostname = socket.gethostname()

# Obtener la dirección IP local de la máquina
ip_address = socket.gethostbyname(hostname)

def copy_clipboard():
    text_copy = ip_address
    pyperclip.copy(text_copy)

def start_vsftpd():
    result = subprocess.run(['systemctl', 'start', 'vsftpd'])
    if result.returncode == 0:
        tray_icon.setIcon(QIcon(str(icon_green)))
    else:
        tray_icon.setIcon(QIcon(str(icon_red)))

def stop_vsftpd_proccess():
    result = subprocess.run(['systemctl', 'stop', 'vsftpd'])
    if result.returncode == 0:
        tray_icon.setIcon(QIcon(str(icon_red)))
    else:
        tray_icon.setIcon(QIcon(str(icon_green)))

def check_vsftpd():
    # ejecutar el comando "systemctl start vsftpd"
    result = subprocess.run(['systemctl', 'status', 'vsftpd'], capture_output=True)
    # verificar el valor de retorno
    if result.returncode == 0:
        tray_icon.setIcon(QIcon(str(icon_green)))
    else:
        tray_icon.setIcon(QIcon(str(icon_red)))

app = QApplication([])
tray_icon = QSystemTrayIcon(QIcon(str(icon_white)), parent=None)
tray_icon.show()

# crear un objeto QMenu para el menú contextual
menu = QMenu()
tray_icon.setContextMenu(menu)

# mostrar IP actual
my_ip = ip_address
time.sleep(10)
start_action = QAction(str(my_ip), parent=menu)
start_action.triggered.connect(copy_clipboard)
menu.addAction(start_action)

# agregar una acción de menú para iniciar vsftpd
start_action = QAction('Start vsftpd', parent=menu)
start_action.triggered.connect(start_vsftpd)
menu.addAction(start_action)

# agregar una acción de menú para frenar vsftpd
stop_action = QAction('Stop vsftpd', parent=menu)
stop_action.triggered.connect(stop_vsftpd_proccess)
menu.addAction(stop_action)

#agregar una accion para salir
action = QAction("Quit", app)
action.triggered.connect(app.quit)
menu.addAction(action)

# configurar un temporizador para comprobar vsftpd cada 60 segundos
timer = QTimer()
timer.timeout.connect(check_vsftpd)
timer.start(60000)

app.exec_()
