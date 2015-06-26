from kivy.app import App

from examples.kivy.common.brickfinder import BrickFinderWidget

class InfoApp(App):
    def build(self):
        bfw = BrickFinderWidget(title='NXT Demo',start=True)
        bfw.bind(brick=self.brickfound_callback)
        return bfw

    def brickfound_callback(self, instance, brick):
        if brick:
            print('we found it :-)')
        else:
            print('no brick :-(')


if __name__ == '__main__':
    InfoApp().run()