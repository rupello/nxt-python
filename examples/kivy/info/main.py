import sys

from kivy.uix.rst import RstDocument
from kivy.app import App
from kivy.clock import Clock

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
        Clock.schedule_interval(self.updatetext, 0.5)
        self.log(' Finding the brick...')
        Clock.schedule_once(self.find_brick)

    def find_brick(self,dt):
        try:
            self._brick = nxt.find_one_brick(name='lloyd')
            if self._brick:
                info = self._brick.get_device_info()
                self.log(' brick found :-)')
                self.log(' Name:{}'.format(info[0].strip('\x00')))
                self.log(' Address:{}'.format(info[1]))
                self.log(' Firmware:{}'.format(self._brick.get_firmware_version()))
                self.log(' Battery:{}mV'.format(self._brick.get_battery_level()))
        except Exception as e:
            self.log(' brick not found :-(')
            self.log(' Error:{}'.format(e.message))
            self.log(' Check brick is powered on and paired.')


    def updatetext(self,dt):
        self._doc.text = '\n'.join(self._logbuffer)
        self._doc.scroll_y = 0  # scroll to bottom

    def log(self,message):
        self._logbuffer.append(message)


if __name__ == '__main__':
    InfoApp().run()