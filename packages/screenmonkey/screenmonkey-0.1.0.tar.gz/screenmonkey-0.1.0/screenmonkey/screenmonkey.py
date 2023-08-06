import pandas
import datetime
import openpyxl
import time
from pynput import mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController


class Sequence:
    def __init__(self):
        self.actions = pandas.DataFrame(columns=['X', 'Y', 'Action', 'Button', 'Seconds', 'Type'])
        self.steps = []
        self.timestamp = datetime.datetime.now()
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def checkTime(self, prev):
        timeDif = datetime.datetime.now() - prev
        return round(timeDif.total_seconds(), 3)

    def on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        buttonStr = 'Left' if str(button) == 'Button.left' else 'Right'
        print('{0} at {1} on {2}'.format(action, (x, y), buttonStr))
        current = {'X': x, 'Y': y, 'Action': action, 'Button': buttonStr, 'Seconds': self.checkTime(self.timestamp), 'Type': 'Mouse'}
        self.steps.append(current)  # add steps
        self.timestamp = datetime.datetime.now()  # update timestamp
        if (x <= 0) and (y <= 0) and (action == 'Released'):
            # Stop listener
            print('Recording Finished')
            self.actions = pandas.DataFrame(self.steps, columns=['X', 'Y', 'Action', 'Button', 'Seconds', 'Type'])
            return False

    def record(self):
        print('Allowing 10 seconds to prepare screen')
        time.sleep(10)
        self.timestamp = datetime.datetime.now()
        print('Recording ready, please start actions. Click top left corner of screen to exit recording')
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

    def save_excel(self, filepath):
        self.actions.to_excel(filepath, index=False)

    def run(self):
        print('Allowing 10 seconds to prepare screen')
        time.sleep(10)
        print('Actions starting, please do not touch mouse/keyboard during actions')
        len = self.actions.shape[0]
        for i in range(0, len):
            time.sleep(self.actions['Seconds'][i])
            if self.actions['Type'][i] == 'Mouse':
                self.mouse.position = (self.actions['X'][i], self.actions['Y'][i])
                button = Button.left if self.actions['Button'][i] == 'Left' else Button.right
                if self.actions['Action'][i] == 'Pressed':
                    self.mouse.press(button)
                elif self.actions['Action'][i] == 'Released':
                    self.mouse.release(button)
                print('The current pointer position is {0}'.format(
                    self.mouse.position))
        print('Actions Finished')

    def load_excel(self, filepath):
        self.actions = pandas.read_excel(filepath)

