from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Load KV files (make sure they are inside kv/ folder)
Builder.load_file("kv/splash.kv")
Builder.load_file("kv/login.kv")
Builder.load_file("kv/patient.kv")
Builder.load_file("kv/doctor.kv")

# Define Screen classes
class SplashScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class PatientScreen(Screen):
    pass

class DoctorScreen(Screen):
    pass

# Screen Manager
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
