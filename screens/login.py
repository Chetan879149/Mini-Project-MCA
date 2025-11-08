# ==========================================
# LOGIN & SIGNUP SYSTEM WITH SQLITE + OTP RESET
# ==========================================

import sqlite3
import random
import smtplib  # For Gmail OTP sending (optional)
from email.mime.text import MIMEText
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.behaviors import ButtonBehavior

class ClickableLabel(ButtonBehavior, Label):
    pass

class ForgotPasswordScreen(Screen):
    """(Kept for completeness if you want a separate screen later)"""
    pass

class LoginSignupScreen(Screen):
    mode = StringProperty("login")
    role_selected = StringProperty("")  # will be set from spinner
    title_text = StringProperty("Login")
    switch_text = StringProperty("Don't have an account? Sign up")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signup_fields = {}
        self.temp_otp = None
        self.temp_email = None
        self.temp_aadhaar = None
        self.create_database()

    # ----------------------------------------------------
    # DATABASE SETUP
    # ----------------------------------------------------
    def create_database(self):
        """Creates the SQLite database and users table if not exists"""
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    contact TEXT,
                    dob TEXT,
                    aadhaar TEXT UNIQUE,
                    password TEXT,
                    role TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Logger.exception(f"DB Create Error: {e}")

    # ----------------------------------------------------
    # FORM SWITCHING
    # ----------------------------------------------------
    def switch_form(self):
        """Switch between Login and Signup form"""
        if self.mode == "login":
            self.build_signup()
        else:
            self.build_login()

    def build_login(self):
        """Rebuilds login form view"""
        self.mode = "login"
        self.title_text = "Login"
        self.switch_text = "Don't have an account? Sign up"

        # Remove any dynamic signup fields if present
        if hasattr(self, "signup_fields"):
            for field in list(self.signup_fields.values()):
                try:
                    if field.parent:
                        self.ids.form_layout.remove_widget(field)
                except Exception:
                    pass
            self.signup_fields.clear()

        # Reset role_selected to whatever spinner currently shows
        try:
            self.role_selected = self.ids.role_spinner.text if hasattr(self.ids, "role_spinner") else ""
        except Exception:
            self.role_selected = ""

    def build_signup(self):
        self.mode = "signup"
        self.title_text = "Sign Up"
        self.switch_text = "← Back to Login"

        # Clear previous dynamic fields
        for field in list(self.signup_fields.values()):
            if field.parent:
                self.ids.form_layout.remove_widget(field)
        self.signup_fields.clear()

        bottom_buttons_count = 4
        field_names = ["First Name", "Last Name", "Email", "Contact Number", "DOB",
                       "Aadhaar", "Password", "Role"]

        for name in field_names:
            if name == "Role":
                widget = Spinner(text="Patient", values=["Doctor", "Patient"], size_hint_y=None, height=40)
                widget.bind(text=lambda inst, val: setattr(self, "role_selected", val))
            elif name == "Password":
                widget = TextInput(
                    hint_text=name,
                    password=True,
                    multiline=False,
                    size_hint_y=None,
                    height=45,
                    background_normal='',
                    background_color=(0.95, 0.95, 0.95, 1),
                    foreground_color=(0, 0, 0, 1),
                    padding=[10, 10]
                )
            else:
                widget = TextInput(
                    hint_text=name,
                    multiline=False,
                    size_hint_y=None,
                    height=45,
                    background_normal='',
                    background_color=(0.95, 0.95, 0.95, 1),
                    foreground_color=(0, 0, 0, 1),
                    padding=[10, 10]
                )

            self.signup_fields[name] = widget
            try:
                insert_index = max(0, len(self.ids.form_layout.children) - bottom_buttons_count)
                self.ids.form_layout.add_widget(widget, index=insert_index)
            except Exception as e:
                Logger.error(f"Add signup widget error: {e}")
                try:
                    self.ids.form_layout.add_widget(widget)
                except Exception as ex:
                    Logger.error(f"Add fallback failed: {ex}")

    # ----------------------------------------------------
    # LOGIN VALIDATION
    # ----------------------------------------------------
    def validate_login(self):
        """Check login credentials"""
        try:
            adhar = self.ids.adhar_input.text.strip().replace(" ", "")
            password = self.ids.password_input.text.strip()
            # read from spinner directly if possible
            role = ""
            try:
                role = self.ids.role_spinner.text.strip()
            except Exception:
                role = self.role_selected.strip()

            if not adhar or not password or role not in ["Admin", "Doctor", "Patient"]:
                self.show_popup("Error", "All fields are required (and role must be selected).")
                return

            # Admin login (developer-only access)
            if role == "Admin" and adhar == "9999" and password == "admin123":
                self.show_popup("Success", "Admin login successful!")
                return

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE aadhaar=? AND password=? AND role=?",
                           (adhar, password, role))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.show_popup("Success", f"Welcome back, {result[1]} ({role})!")
            else:
                self.show_popup("Error", "Invalid credentials. Please try again.")

        except Exception as e:
            self.show_popup("Error", f"Unexpected error: {e}")
            Logger.error(f"Login Error: {e}")

    # ----------------------------------------------------
    # SIGNUP HANDLER
    # ----------------------------------------------------
    def validate_signup(self):
        """Create a new account (Signup with proper validation)"""
        try:
            if self.mode != "signup":
                self.show_popup("Error", "Not in signup mode.")
                return

            required_order = ["First Name", "Last Name", "Email", "Contact Number",
                              "DOB", "Aadhaar", "Password", "Role"]
            data = []

            for key in required_order:
                widget = self.signup_fields.get(key)
                if not widget:
                    self.show_popup("Error", f"Missing field: {key}")
                    return

                # Spinner ke liye alag handling
                if isinstance(widget, Spinner):
                    val = widget.text.strip()
                else:
                    val = widget.text.strip()

                if not val:
                    self.show_popup("Error", f"{key} cannot be empty.")
                    return

                data.append(val)

            # Role validation
            if data[-1] not in ["Doctor", "Patient"]:
                self.show_popup("Error", "Please select a valid Role (Doctor/Patient).")
                return

            # Insert into DB
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, contact, dob, aadhaar, password, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(data))
            conn.commit()
            conn.close()

            self.show_popup("Success", "Account created successfully!")
            self.build_login()

        except sqlite3.IntegrityError:
            self.show_popup("Error", "Aadhaar already registered.")
        except Exception as e:
            Logger.error(f"Signup Error: {e}")
            self.show_popup("Error", f"Signup error: {e}")

    # ----------------------------------------------------
    # FORGOT PASSWORD - EMAIL OTP (popup based)
    # ----------------------------------------------------
    def forgot_password(self):
        """Forgot password popup - sends OTP to user email"""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        aadhaar_input = TextInput(hint_text="Enter Aadhaar Number", multiline=False)
        send_otp_btn = Button(text="Send OTP", size_hint_y=None, height=40)
        layout.add_widget(aadhaar_input)
        layout.add_widget(send_otp_btn)
        popup = Popup(title="Forgot Password", content=layout, size_hint=(0.8, 0.5))
        popup.open()

        def send_otp(instance):
            aadhaar = aadhaar_input.text.strip()
            if not aadhaar:
                self.show_popup("Error", "Please enter Aadhaar.")
                return

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE aadhaar=?", (aadhaar,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                self.show_popup("Error", "No user found with this Aadhaar.")
                return

            email = result[0]
            self.temp_email = email
            self.temp_otp = random.randint(100000, 999999)
            self.temp_aadhaar = aadhaar

            # Optionally send OTP via Gmail (requires app password) - disabled by default
            # If you want to enable, replace sender & app_password. For safety, it's commented.
            try:
                sender = "your_email@gmail.com"  # 👈 Replace this
                app_password = "your_app_password_here"  # 👈 Replace this
                msg = MIMEText(f"Your OTP for password reset is: {self.temp_otp}")
                msg["Subject"] = "Password Reset OTP"
                msg["From"] = sender
                msg["To"] = email

                # Uncomment to actually send email (make sure credentials are correct)
                # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                #     server.login(sender, app_password)
                #     server.send_message(msg)

                popup.dismiss()
                self.show_popup("Success", f"OTP generated and (optionally) sent to {email}.")
                Clock.schedule_once(lambda dt: self.otp_verification_popup(), 0.3)

            except Exception as e:
                self.show_popup("Error", f"Failed to send OTP: {e}")
                Logger.error(f"Email OTP Error: {e}")

        send_otp_btn.bind(on_release=send_otp)

    # ----------------------------------------------------
    # OTP VERIFICATION
    # ----------------------------------------------------
    def otp_verification_popup(self):
        """Verify OTP and reset password"""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        otp_input = TextInput(hint_text="Enter OTP", multiline=False)
        new_pass_input = TextInput(hint_text="New Password", password=True, multiline=False)
        submit_btn = Button(text="Reset Password", size_hint_y=None, height=40)
        layout.add_widget(otp_input)
        layout.add_widget(new_pass_input)
        layout.add_widget(submit_btn)
        popup = Popup(title="Verify OTP", content=layout, size_hint=(0.8, 0.5))
        popup.open()

        def reset_password(instance):
            if not self.temp_otp or not self.temp_aadhaar:
                self.show_popup("Error", "No OTP request in progress.")
                return
            if otp_input.text.strip() == str(self.temp_otp):
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=? WHERE aadhaar=?",
                               (new_pass_input.text.strip(), self.temp_aadhaar))
                conn.commit()
                conn.close()
                popup.dismiss()
                self.show_popup("Success", "Password reset successfully!")
                # clear temps
                self.temp_otp = None
                self.temp_aadhaar = None
                self.temp_email = None
            else:
                self.show_popup("Error", "Incorrect OTP!")

        submit_btn.bind(on_release=reset_password)

    # ----------------------------------------------------
    # POPUP CREATOR
    # ----------------------------------------------------
    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.4, 0.4))
        popup.open()
