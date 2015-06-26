import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.animation import Animation

import nxt.motor

from examples.kivy.common.brickfinder import popup_finder

class SelfCenteringSlider(Slider):
    """center the center automatically if released"""
    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Animation(value=0,duration=.2,t='out_back').start(self)

class TankWidget(BoxLayout):
    def __init__(self,**kwargs):
        super(TankWidget, self).__init__(**kwargs)
        self.padding = [0, 20, 0, 20]
        self.orientation = 'horizontal'
        self.tank = None
        self._leftSlider = SelfCenteringSlider(min=-100, max=100, value=0,orientation='vertical')
        self._rightSlider = SelfCenteringSlider(min=-100, max=100, value=0,orientation='vertical')
        self.add_widget(self._leftSlider)
        self.add_widget(self._rightSlider)

    def start_tank(self,dt):
        self._motleft = nxt.motor.Motor(self.brick, nxt.motor.PORT_B)
        self._motright = nxt.motor.Motor(self.brick, nxt.motor.PORT_C)
        Clock.schedule_interval(self.update_motors, 0.1)

    def update_motors(self,dt):
        start = time.time()
        self._motleft.run(power=self._leftSlider.value)
        self._motright.run(power=self._rightSlider.value)
        interval = time.time()-start
        print('updated in:{:.03}'.format(interval))

    def on_touch_down(self, touch):
        print touch
        return super(TankWidget, self).on_touch_down(touch)


class TankApp(App):

    def build(self):
        self._tank = TankWidget()
        return self._tank

    def on_start(self):
        popup_finder(self.brickfound_callback)

    def brickfound_callback(self, instance, brick):
        if brick:
            print('we found it :-)')
            self._tank.brick = brick
            Clock.schedule_once(self._tank.start_tank,1.0)
        else:
            print('no brick :-(')
            self.stop()


if __name__ == '__main__':
    TankApp().run()