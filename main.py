from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

#! Import Screens
from screens.splash import SplashScreen
from screens.login import LoginSignupScreen
# from screens.patient import PatientScreen
# from screens.doctor import DoctorScreen

#! Example: Mobile screen size (iPhone 14 approx)
Window.size = (250, 540)  # Width x Height in pixels

#! Load KV files (make sure they are inside kv/ folder)
Builder.load_file("kv/splash.kv")
Builder.load_file("kv/login.kv")
# Builder.load_file("kv/patient.kv")
# Builder.load_file("kv/doctor.kv")

#! Global background color (white)
Window.clearcolor = get_color_from_hex("#ffffff")

#! Screen Manager
class HealthcareApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginSignupScreen(name="login"))
        # sm.add_widget(PatientScreen(name="patient"))
        # sm.add_widget(DoctorScreen(name="doctor"))
        return sm


if __name__ == "__main__":
    HealthcareApp().run()
