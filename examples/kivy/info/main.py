import threading

from kivy.uix.rst import RstDocument
from kivy.app import App
from kivy.clock import Clock

try:
    from jnius import detach
except:
    def detach():
        pass

import nxt
import nxt.bluesock
import nxt.brick

class InfoApp(App):

    def build(self):
        self._logbuffer = ['NXT Demo',
                           '========',
                           '::',
                           '']
        self._doc = RstDocument(text=__doc__)
        return self._doc

    def on_start(self):
        self._brick = None
        self._connect_thread = threading.Thread(target=self.find_brick)
        self._connect_thread.start()

        Clock.schedule_interval(self.update_displayed_text, 0.5)
        Clock.schedule_interval(self.check_brick_connection, 1.5)


    def check_brick_connection(self,dt):
        self.log(' Finding the brick...')
        self._connect_thread.join(timeout=0.5)
        if not self._connect_thread.isAlive():
            Clock.unschedule(self.check_brick_connection)
            if self._brick:
                self.log(' brick found :-)')
                info = self._brick.get_device_info()
                self.log(' Name:{}'.format(info[0].strip('\x00')))
                self.log(' Address:{}'.format(info[1]))
                self.log(' Firmware:{}'.format(self._brick.get_firmware_version()))
                self.log(' Battery:{}mV'.format(self._brick.get_battery_level()))
            else:
                self.log(' brick not found :-(')
                self.log(' Check brick is powered on and paired.')


    def find_brick(self):
        try:
            self._brick = nxt.find_one_brick(name='lloyd',debug=True,method=nxt.Method(bluetooth=True,usb=False))
        finally:
            # kivy/android will crash here if we don't detach
            print('detaching thread')
            detach()


    def update_displayed_text(self,dt):
        self._doc.text = '\n'.join(self._logbuffer)
        self._doc.scroll_y = 0  # scroll to bottom

    def log(self,message):
        """lod a message to the console and gui"""
        print(message)
        self._logbuffer.append(message)


if __name__ == '__main__':
    InfoApp().run()