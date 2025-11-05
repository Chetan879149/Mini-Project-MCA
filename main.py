from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

#! Import Screens
from screens.splash import SplashScreen
from screens.login import LoginSignupScreen
from screens.patient import PatientScreen
from screens.doctor import DoctorScreen

#! Load KV files (make sure they are inside kv/ folder)
Builder.load_file("kv/splash.kv")
Builder.load_file("kv/login.kv")
Builder.load_file("kv/patient.kv")
Builder.load_file("kv/doctor.kv")

#! Global background color (thyme green shade)
Window.clearcolor = get_color_from_hex("#69c769")

#! Screen Manager
class HealthcareApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PatientScreen(name="patient"))
        sm.add_widget(DoctorScreen(name="doctor"))
        return sm

if __name__ == "__main__":
    HealthcareApp().run()

