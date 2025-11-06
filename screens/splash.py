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

        # Logo
        self.logo = Image(
            source=LOGO_FILE,
            size_hint=(0.5, 0.5),
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.logo)

        # Animate properties correctly
        anim = Animation(
            opacity=1,
            size_hint_x=0.6,
            size_hint_y=0.6,
            center_y=self.logo.center_y + 150,  # slide up
            duration=2.0,
            t='out_quad'
        )

        # Bounce effect
        bounce = Animation(
            size_hint_x=0.65,
            size_hint_y=0.65,
            duration=0.2,
            t='out_quad'
        ) + Animation(
            size_hint_x=0.6,
            size_hint_y=0.6,
            duration=0.2,
            t='out_quad'
        )

        # Chain main animation + bounce
        full_anim = anim + bounce
        full_anim.start(self.logo)

        # Switch to login after 4 seconds
        Clock.schedule_once(self.switch_to_next, 4)

    def switch_to_next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'login'
