from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import Clock

class LoginSignupScreen(Screen):
    mode = StringProperty("login")  # default login
    role_selected = StringProperty("Select Role ▼")
    title_text = StringProperty("Login")
    switch_text = StringProperty("Don't have an account? Sign up")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signup_fields = {}
        self.role_popup = None
        self.mode = "login"

    def switch_form(self):
        """Switch between login and signup safely"""
        if self.mode == "login":
            self.build_signup()
        else:
            self.build_login()

    def build_login(self):
        self.mode = "login"
        self.title_text = "Login"
        self.switch_text = "Don't have an account? Sign up"

        # Remove any dynamic signup fields
        for field in self.signup_fields.values():
            if field.parent:
                self.ids.form_layout.remove_widget(field)
        self.signup_fields.clear()

    def build_signup(self):
        self.mode = "signup"
        self.title_text = "Sign Up"
        self.switch_text = "← Back to Login"

        # First, remove previous signup fields if any
        for field in self.signup_fields.values():
            if field.parent:
                self.ids.form_layout.remove_widget(field)
        self.signup_fields.clear()

        # Add signup fields dynamically above the bottom buttons
        bottom_buttons_count = 2  # Login/Signup switch buttons already in kv
        field_names = ["First Name", "Last Name", "Email", "Contact Number",
                       "DOB", "Aadhaar", "Password", "Role"]

        for i, name in enumerate(field_names):
            ti = TextInput(
                hint_text=name,
                multiline=False,
                size_hint_y=None,
                height=45,
                background_normal='',
                background_color=(0.95,0.95,0.95,1),
                foreground_color=(0,0,0,1),
                padding=[10,10]
            )
            self.signup_fields[name] = ti
            # Insert **above the bottom buttons** (last 2 widgets in kv)
            insert_index = len(self.ids.form_layout.children) - bottom_buttons_count
            self.ids.form_layout.add_widget(ti, index=insert_index)

    def toggle_role_dropdown(self):
        if self.role_popup and self.role_popup.parent:
            self.role_popup.dismiss()
            self.role_popup = None
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        for role in ["Admin","Doctor","Patient"]:
            btn = Button(text=role, size_hint_y=None, height=40)
            btn.bind(on_release=lambda x, r=role: self.select_role(r))
            layout.add_widget(btn)

        from kivy.uix.popup import Popup
        self.role_popup = Popup(title="Select Role", content=layout, size_hint=(0.5,0.4), auto_dismiss=True)
        self.role_popup.open()

    def select_role(self, role):
        self.role_selected = f"{role} ▼"
        if self.role_popup:
            self.role_popup.dismiss()
            self.role_popup = None

    def validate_login(self):
        adhar = self.ids.adhar_input.text.strip()
        password = self.ids.password_input.text.strip()
        role = self.role_selected.replace(" ▼","")

        if not adhar or not password or role not in ["Admin","Doctor","Patient"]:
            self.show_popup("Error", "All fields are required")
            return

        if adhar=="123456789012" and password=="admin":
            self.show_popup("Success", f"Login successful as {role}!")
        else:
            self.show_popup("Error","Invalid Aadhaar or Password")

    def show_popup(self,title,message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.4,0.4))
        popup.open()
