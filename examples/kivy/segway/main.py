import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.lang import Builder

import nxt.motor

from common.brickfinder import popup_finder

class SegwayWidget(BoxLayout):
    def __init__(self,**kwargs):
        self.brick = None
        super(SegwayWidget, self).__init__(**kwargs)


Builder.load_string("""
<OrientLabel@Label>
    halign: 'left'
    size_hint_x: 1.
    text_size: self.size

<OrientBar@ProgressBar>
    value: 100
    min: 0
    max: 360

<SegwayWidget>:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_0_label
                text: 'Axis 0:'
            OrientBar:
                id: orient_axis_0_bar
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_1_label
                text: 'Axis 1:'
            OrientBar:
                id: orient_axis_1_bar
        BoxLayout:
            orientation: 'vertical'
            OrientLabel:
                id: orient_axis_2_label
                text: 'Axis 2:'
            OrientBar:
                id: orient_axis_2_bar
""")


class SegwayApp(App):
    def build(self):
        self._segway = SegwayWidget()
        return self._segway

    def on_start(self):
        pass
        #popup_finder(self.brickfound_callback)

    def brickfound_callback(self, brick):
        if brick:
            print('we found it :-)')
            self._tank.brick = brick
            #Clock.schedule_once(self._tank.start_tank,1.0)
        else:
            print('no brick :-(')
            self.stop()


if __name__ == '__main__':
    SegwayApp().run()