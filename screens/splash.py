from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock

LOGO_FILE = "assets/logo.png"

class SplashScreen(Screen):
    def on_enter(self):
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        #! Circular logo (radius 50%)
        self.logo = Image(
            source=LOGO_FILE,
            size_hint=(0.5, 0.5),
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.logo)

        #! Animation: Fade-in + Zoom + Slide-up
        anim = (Animation(opacity=1, size_hint=(0.7, 0.7), duration=2.0, t='out_quad') +
                Animation(pos_hint={'center_y': 0.8}, size_hint=(0.4, 0.4), duration=2.0, t='out_quad'))
        anim.start(self.logo)

        #! Switch to login after 4 seconds
        Clock.schedule_once(self.switch_to_next, 4)

    def switch_to_next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'login'