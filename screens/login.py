import sqlite3
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from vonage import Auth, Vonage


class LoginSignupScreen(Screen):
    temp_otp = StringProperty('')
    current_reset_adhar = ''  # Track Aadhaar for resetting password

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_users_table()

        # Initialize Vonage client for SMS sending
        auth = Auth(api_key="a84ac8a4", api_secret="ewblnZhSoTVz4H4V")
        self.vonage_client = Vonage(auth)
        self.sms = self.vonage_client.sms  # Assign SMS client for sending messages

    def create_users_table(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                aadhaar TEXT UNIQUE,
                phone TEXT,
                password TEXT,
                role TEXT
            )
        """)
        conn.commit()
        conn.close()

    def on_otp_text(self, instance, value):
        if len(value) > 1:
            instance.text = value[:1]
        if len(instance.text) == 1:
            try:
                current_id = instance.id  # eg otp1
                next_index = int(current_id[-1]) + 1
                next_id = f'otp{next_index}'
                if next_id in self.ids:
                    self.ids[next_id].focus = True
            except Exception:
                pass

    def validate_login(self):
        adhar = self.ids.adhar_input.text.strip().replace(" ", "")
        password = self.ids.password_input.text.strip()
        role = self.ids.role_spinner.text.strip()

        if not adhar or not password or role not in ['Admin', 'Doctor', 'Patient']:
            self.show_popup("Error", "Please fill all details and select a valid role.")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE aadhaar=? AND password=? AND role=?", (adhar, password, role))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.show_popup("Success", f"Welcome back, {role}!")
            # Add navigation logic here if needed
        else:
            self.show_popup("Error", "Invalid credentials.")

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

    def send_otp(self):
        adhar = self.ids.forgot_adhar_input.text.strip().replace(" ", "")
        if not adhar:
            self.show_popup("Error", "Please enter Aadhaar number.")
            return

        # Verify Aadhaar exists and get phone number
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT phone FROM users WHERE aadhaar=?", (adhar,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            self.show_popup("Error", "Aadhaar not found. Please check and try again.")
            return

        phone_number = user[0]
        otp = str(random.randint(1000, 9999))
        self.temp_otp = otp

        # Send OTP SMS
        response = self.sms.send(
            {
                "from_": "trackhealth",
                "to": phone_number,
                "text": f"Dear customer, the one time password to reset your password at trackhealth is {otp}. This OTP will expire in 5 minutes.",
            }
        )

        #! Check status from response object
        if response.messages[0].status == "0":
           self.show_popup("OTP Sent", "OTP sent to your registered mobile number.")
        else:
            error = response.messages[0].error_text
            self.show_popup("Error", f"Failed to send OTP: {error}")


    def verify_otp(self):
        entered_otp = ''.join([self.ids[f'otp{i}'].text for i in range(1, 5)])
        if entered_otp == self.temp_otp:
            self.show_popup("Success", "OTP verified. Please reset your password.")
            self.current_reset_adhar = self.ids.forgot_adhar_input.text.strip().replace(" ", "")
            self.screen_switch("reset_password_view")
        else:
            self.show_popup("Error", "Incorrect OTP.")

    def reset_password(self):
        new_password = self.ids.new_password_input.text.strip()
        confirm_password = self.ids.confirm_password_input.text.strip()

        if not new_password or not confirm_password:
            self.show_popup("Error", "Please fill all password fields.")
            return

        if new_password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE aadhaar=?", (new_password, self.current_reset_adhar))
            conn.commit()
            conn.close()
            self.show_popup("Success", "Password reset successfully. Please login.")
            self.screen_switch("login_view")
            self.ids.new_password_input.text = ""
            self.ids.confirm_password_input.text = ""
        except Exception as e:
            self.show_popup("Error", f"Failed to reset password: {e}")

    def screen_switch(self, target):
        self.ids.login_views.current = target
        # Optionally clear inputs here if needed

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4)).open()
