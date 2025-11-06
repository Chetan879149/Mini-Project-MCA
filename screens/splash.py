from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock

LOGO_FILE = "assets/Logo.png"

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

        #! Main animation: fade-in + zoom + slide-up
        main_anim = Animation(
            opacity=1,
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            duration=2.0,
            t='out_quad'
        )

        #! Bounce effect: slightly enlarge then return
        bounce_anim = Animation(
            size_hint=(0.65, 0.65),
            duration=0.2,
            t='out_quad'
        ) + Animation(
            size_hint=(0.6, 0.6),
            duration=0.2,
            t='out_quad'
        )

        #! Chain animations
        full_anim = main_anim + bounce_anim
        full_anim.start(self.logo)

        #! Switch to login after 4 seconds
        Clock.schedule_once(self.switch_to_next, 4)

    def switch_to_next(self, *args):
        self.manager.transition.direction = 'up'
        self.manager.current = 'login'
