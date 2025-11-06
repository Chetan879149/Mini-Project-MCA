from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
import os

# Load KV file
Builder.load_file(os.path.join("kv", "splash.kv"))

class CircularImageStencil(Screen):
    source = StringProperty("")  # Add this property for KV binding

class SplashScreen(Screen):
    def on_enter(self):
        logo = self.ids.logo

        # Smooth fade + zoom + slide + spring animation
        anim = Animation(
            opacity=0.7,
            size_hint_x=0.65,
            size_hint_y=0.65,
            center_y=logo.center_y + 50,
            duration=1.5,
            t='out_elastic'
        )
        anim.start(logo)

        # Switch to login after 3 seconds
        Clock.schedule_once(self.switch_to_next, 3)

    def switch_to_next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'login'
