from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup


class LoginSignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "login"
        self.build_login()

    def build_login(self):
        """Build login form layout"""
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)
        layout.add_widget(Label(text="Login using Aadhaar ID", font_size='28sp', color=get_color_from_hex("#000000")))

        self.adhar_input = TextInput(hint_text="Aadhaar ID", multiline=False, size_hint=(1, None), height=50)
        self.dob_input = TextInput(hint_text="Date of Birth (DD/MM/YYYY)", multiline=False, size_hint=(1, None), height=50)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, size_hint=(1, None), height=50)

        layout.add_widget(self.adhar_input)
        layout.add_widget(self.dob_input)
        layout.add_widget(self.password_input)

        btn_login = Button(text="Login", size_hint=(1, None), height=50, background_color=(0, 0.6, 0.3, 1))
        btn_login.bind(on_release=self.validate_login)
        layout.add_widget(btn_login)

        btn_switch = Button(text="Don’t have an account? Sign up", size_hint=(1, None), height=50,
                            background_color=(0.3, 0.3, 0.3, 1))
        btn_switch.bind(on_release=lambda x: self.build_signup())
        layout.add_widget(btn_switch)

        # back_btn = Button(text="← Back", size_hint=(1, None), height=50,
        #                   background_color=(0.2, 0.1, 0.1, 1), color=(1, 1, 1, 1))
        # back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "splash"))
        # layout.add_widget(back_btn)

        self.add_widget(layout)

    def build_signup(self):
        """Build signup form layout"""
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        layout.add_widget(Label(text="Sign Up", font_size='28sp', color=get_color_from_hex("#000000")))

        # All necessary fields
        self.fields = {
            "First Name": TextInput(hint_text="First Name", multiline=False, size_hint=(1, None), height=45),
            "Last Name": TextInput(hint_text="Last Name", multiline=False, size_hint=(1, None), height=45),
            "Email": TextInput(hint_text="Email", multiline=False, size_hint=(1, None), height=45),
            "Contact": TextInput(hint_text="Contact Number", multiline=False, size_hint=(1, None), height=45),
            "DOB": TextInput(hint_text="Date of Birth (DD/MM/YYYY)", multiline=False, size_hint=(1, None), height=45),
            "Aadhaar": TextInput(hint_text="Aadhaar ID", multiline=False, size_hint=(1, None), height=45),
            "Password": TextInput(hint_text="Password", password=True, multiline=False, size_hint=(1, None), height=45),
            "Role": TextInput(hint_text="Role (Admin / Doctor / Patient)", multiline=False, size_hint=(1, None), height=45)
        }

        for field in self.fields.values():
            layout.add_widget(field)

        signup_btn = Button(text="Sign Up", size_hint=(1, None), height=50, background_color=(0, 0.6, 0.3, 1))
        signup_btn.bind(on_release=self.validate_signup)
        layout.add_widget(signup_btn)

        back_btn = Button(text="← Back to Login", size_hint=(1, None), height=50,
                          background_color=(0.3, 0.3, 0.3, 1))
        back_btn.bind(on_release=lambda x: self.build_login())
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def validate_login(self, instance):
        """Validate login fields"""
        adhar = self.adhar_input.text.strip()
        dob = self.dob_input.text.strip()
        password = self.password_input.text.strip()

        if not adhar or not dob or not password:
            self.show_popup("Error", "All fields are required.")
            return

        try:
            # Dummy validation for now
            if adhar == "123456789012" and password == "admin":
                self.show_popup("Success", "Login successful!")
                Clock.schedule_once(lambda dt: setattr(self.manager, "current", "patient"), 1)
            else:
                self.show_popup("Error", "Invalid Aadhaar or Password.")
        except Exception as e:
            self.show_popup("Exception", f"An unexpected error occurred: {e}")

    def validate_signup(self, instance):
        """Validate signup fields"""
        for label, field in self.fields.items():
            if not field.text.strip():
                self.show_popup("Error", f"{label} is required.")
                return

        try:
            # Simple demo: success popup
            self.show_popup("Success", "Account created successfully! Redirecting to login...")
            Clock.schedule_once(lambda dt: self.build_login(), 2)
        except Exception as e:
            self.show_popup("Exception", f"An unexpected error occurred: {e}")

    def show_popup(self, title, message):
        """Show popup for alerts"""
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.4, 0.4))
        popup.open()
