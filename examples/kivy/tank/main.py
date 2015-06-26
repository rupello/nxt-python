import threading
import time

from kivy.uix.rst import RstDocument
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.animation import Animation

from brickfinder import BrickFinderWidget
try:
    from jnius import detach
except:
    def detach():
        pass

import nxt
import nxt.bluesock
import nxt.brick
import nxt.motor


class SelfCenteringSlider(Slider):
    """center the center automatically if released"""
    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Animation(value=0,duration=.2,t='out_back').start(self)


class TankApp(App):

    def build(self):
        self.manager = ScreenManager(transition=SlideTransition(
            duration=.15))

        bfw = BrickFinderWidget(title='Tank Demo', start=True)
        bfw.bind(brick=self.brickfound_callback)
        search_screen = Screen(name='search')
        search_screen.add_widget(bfw)
        self.manager.add_widget(search_screen)

        tank_screen = Screen(name='tank')
        layout = BoxLayout(orientation='horizontal')
        self._leftSlider = SelfCenteringSlider(min=-100, max=100, value=0,orientation='vertical')
        self._rightSlider = SelfCenteringSlider(min=-100, max=100, value=0,orientation='vertical')
        layout.add_widget(self._leftSlider)
        layout.add_widget(self._rightSlider)
        tank_screen.add_widget(layout)
        self.manager.add_widget(tank_screen)

        self.manager.current = 'search'
        return self.manager

    def brickfound_callback(self, instance, brick):
        if brick:
            print('we found it :-)')
            self._brick = brick
            Clock.schedule_once(self.start_tank,1.0)
        else:
            print('no brick :-(')
            self.c

    def start_tank(self,dt):
        self._motleft = nxt.motor.Motor(self._brick, nxt.motor.PORT_B)
        self._motright = nxt.motor.Motor(self._brick, nxt.motor.PORT_C)
        self.manager.current = 'tank'
        Clock.schedule_interval(self.update_motors, 0.1)

    def update_motors(self,dt):
        start = time.time()
        self._motleft.run(power=self._leftSlider.value)
        self._motright.run(power=self._rightSlider.value)
        interval = time.time()-start
        print('updated in:{:.03}'.format(interval))

    def on_touch_down(self, touch):
        print touch

if __name__ == '__main__':
    TankApp().run()