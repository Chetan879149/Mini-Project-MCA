import sqlite3
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

class LoginSignupScreen(Screen):
    temp_otp = StringProperty('')

    # ---------------------- LOGIN LOGIC ----------------------
    def validate_login(self):
        adhar = self.ids.adhar_input.text.strip().replace(" ", "")
        password = self.ids.password_input.text.strip()
        role = self.ids.role_spinner.text.strip()
        
        if not adhar or not password or role not in ['Admin', 'Doctor', 'Patient']:
            self.show_popup("Error", "Please fill all details and select a valid role.")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE aadhaar=? AND password=? AND role=?", 
                       (adhar, password, role))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.show_popup("Success", f"Welcome back, {role}!")
            # Here, you can redirect to the next screen based on role:
            # if role == 'Doctor':
            #     self.manager.current = 'doctor'
            # elif role == 'Patient':
            #     self.manager.current = 'patient'
        else:
            self.show_popup("Error", "Invalid credentials.")

    # --------------------- SIGNUP LOGIC ----------------------
    def validate_signup(self):
        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        adhar = self.ids.signup_adhar_input.text.strip().replace(" ", "")
        phone = self.ids.phone_input.text.strip()
        password = self.ids.signup_password_input.text.strip()
        role = self.ids.signup_role_spinner.text.strip()

        if not (name and email and adhar and phone and password and role in ["Doctor", "Patient"]):
            self.show_popup("Error", "All fields are required, and a valid role must be selected.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, aadhaar, phone, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, adhar, phone, password, role))
            conn.commit()
            conn.close()
            self.show_popup("Success", "Signup successful! Please login.")
            self.screen_switch('login_view')
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Aadhaar already registered.")
        except Exception as e:
            self.show_popup("Error", f"Signup failed: {e}")

    # --------------- FORGOT PASSWORD (OTP) -------------------
    def send_otp(self):
        adhar = self.ids.forgot_adhar_input.text.strip().replace(" ", "")
        if not adhar:
            self.show_popup("Error", "Please enter Aadhaar number.")
            return
        self.temp_otp = str(random.randint(1000, 9999))
        self.ids.otp_notice.text = f"(Test OTP: {self.temp_otp})"

    def verify_otp(self):
        entered_otp = ''.join([self.ids[f'otp{i}'].text for i in range(1, 5)])
        if entered_otp == self.temp_otp:
            self.show_popup("Success", "OTP verified. Add password reset logic here.")
        else:
            self.show_popup("Error", "Incorrect OTP.")

    # -------------- SCREEN SWITCHING ------------------------
    def screen_switch(self, target):
        self.ids.login_views.current = target
        # Also reset all fields as needed

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message),
              size_hint=(0.6, 0.4)).open()
