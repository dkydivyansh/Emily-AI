import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import threading
import time
import re
import os
from typing import Dict, Any
import requests


class LicenseRegistrationApp:
    # Regular expressions for validation
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    NAME_REGEX = r'^[A-Za-z]+( [A-Za-z]+)?$'
    PHONE_REGEX = r'^\+?\d{10,15}$'  # For phone number validation

    def __init__(self):
        self.root = ttk.Window(themename="superhero")
        self.setup_window()
        self.create_widgets()
        self.setup_layout()

    def setup_window(self) -> None:
        """Initialize window properties"""
        self.root.title("Get License")
        # Set window icon
        self.set_window_icon()

        # Set window size and position
        window_width = 500
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def set_window_icon(self) -> None:
        """Set the window icon"""
        try:
            if os.path.exists("emily.ico"):
                self.root.iconbitmap("emily.ico")
                self.root.iconbitmap(default='emily.ico')
            else:
                print("Warning: Icon file 'emily.ico' not found")
        except Exception as e:
            print(f"Failed to set window icon: {e}")

    def create_widgets(self) -> None:
        """Create all UI widgets"""
        self.title_label = ttk.Label(
            self.root,
            text="Get License Key",
            font=('Arial', 16, 'bold')
        )

        self.name_label = ttk.Label(self.root, text="Name:", font=('Arial', 11))
        self.name_entry = ttk.Entry(self.root, width=30, font=('Arial', 11))

        self.email_label = ttk.Label(self.root, text="Email:", font=('Arial', 11))
        self.email_entry = ttk.Entry(self.root, width=30, font=('Arial', 11))

        self.phone_label = ttk.Label(self.root, text="Mobile Number:", font=('Arial', 11))
        self.phone_entry = ttk.Entry(self.root, width=30, font=('Arial', 11))

        self.country_label = ttk.Label(self.root, text="Country:", font=('Arial', 11))
        self.country_combobox = ttk.Combobox(self.root, width=28, font=('Arial', 11), state="readonly")
        self.country_combobox['values'] = countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia",
    "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic (Czechia)", 
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", 
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. 'Swaziland')", "Ethiopia", "Fiji", 
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", 
    "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", 
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", 
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", 
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", 
    "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", 
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", 
    "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", 
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]
  # Specify available countries

        self.submit_button = ttk.Button(
            self.root,
            text="Submit Registration",
            command=self.submit_form,
            style='primary.TButton',
            width=20
        )

        self.loading_label = ttk.Label(self.root, text="", font=('Arial', 11))

    def setup_layout(self) -> None:
        """Set up the grid layout for all widgets"""
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        self.name_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='e')
        self.name_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')

        self.email_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='e')
        self.email_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky='w')

        self.phone_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky='e')
        self.phone_entry.grid(row=3, column=1, padx=10, pady=(0, 10), sticky='w')

        self.country_label.grid(row=4, column=0, padx=10, pady=(0, 10), sticky='e')
        self.country_combobox.grid(row=4, column=1, padx=10, pady=(0, 10), sticky='w')

        self.submit_button.grid(row=5, column=0, columnspan=2, pady=(10, 20))

    def server_request_id6(self, name: str, email: str, phone: str, country: str) -> Dict[str, Any]:
        from main import unique_id, headers
        api_url = '<apiurl hiddeen>'
        data = {
            "Device_id": unique_id,
            "name": name,
            "email": email,
            "phone": phone,
            "country": country
        }
        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {'status': 'error', 'message': f"Failed to get data. Status code: {response.status_code}"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {'status': 'error', 'message': "An error occurred"}

    def is_valid_email(self, email: str) -> bool:
        """Validate email using regex"""
        return bool(re.match(self.EMAIL_REGEX, email))

    def is_valid_name(self, name: str) -> bool:
        """Validate name using regex"""
        return bool(re.match(self.NAME_REGEX, name))

    def is_valid_phone(self, phone: str) -> bool:
        """Validate phone number using regex"""
        return bool(re.match(self.PHONE_REGEX, phone))

    def submit_form(self) -> None:
        """Handle form submission"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        country = self.country_combobox.get().strip()

        # Validate inputs
        if not name or not email or not phone or not country:
            Messagebox.show_error("Please fill in all the fields.", "Error")
            return

        if not self.is_valid_name(name):
            Messagebox.show_error("Please enter a valid name.", "Invalid Name")
            return

        if not self.is_valid_email(email):
            Messagebox.show_error("Please enter a valid email address.", "Invalid Email")
            return

        if not self.is_valid_phone(phone):
            Messagebox.show_error("Please enter a valid phone number.", "Invalid Phone Number")
            return

        # Hide form and show loading
        self.hide_form()
        self.show_loading()

        # Start server request thread
        thread = threading.Thread(target=self.server_request_thread, args=(name, email, phone, country))
        thread.start()

    def hide_form(self) -> None:
        """Hide all form widgets"""
        for widget in [self.name_label, self.name_entry,
                       self.email_label, self.email_entry,
                       self.phone_label, self.phone_entry,
                       self.country_label, self.country_combobox,
                       self.submit_button]:
            widget.grid_forget()

    def show_loading(self) -> None:
        """Show loading message"""
        self.loading_label.config(text="Submitting, please wait...")
        self.loading_label.grid(row=6, column=0, columnspan=2, pady=(10, 10))

    def server_request_thread(self, name: str, email: str, phone: str, country: str) -> None:
        """Handle server request in separate thread"""
        response = self.server_request_id6(name, email, phone, country)
        self.root.after(0, self.process_server_response, response)

    def process_server_response(self, response: Dict[str, Any]) -> None:
        from main import start_actvation_process
        """Process server response and update UI accordingly"""
        if response['status'] == 'error':
            Messagebox.show_error(response['message'], "Error")
            self.reset_form()  # Reset the form if there is an error
        elif response['status'] == 'found':
            Messagebox.ok("Activating with key: " + response['message'], "License Found")
            self.root.destroy()
            start_actvation_process(response['message'])
        elif response['status'] == 'ok':
            Messagebox.ok(response['message'], "Registered")
            self.root.destroy()
        else:
            Messagebox.show_error(response['message'], "Error")
            self.reset_form()  # Reset the form in case of an unknown error

    def reset_form(self) -> None:
        """Reset the form to its original state after an error"""
        self.loading_label.grid_forget()
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.country_combobox.set('')  # Reset country selection
        self.show_form()  # Show the form again for resubmission

    def show_form(self) -> None:
        """Display form fields again after reset"""
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))
        self.name_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='e')
        self.name_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')
        self.email_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='e')
        self.email_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky='w')
        self.phone_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky='e')
        self.phone_entry.grid(row=3, column=1, padx=10, pady=(0, 10), sticky='w')
        self.country_label.grid(row=4, column=0, padx=10, pady=(0, 10), sticky='e')
        self.country_combobox.grid(row=4, column=1, padx=10, pady=(0, 10), sticky='w')
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=(10, 20))

    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = LicenseRegistrationApp()
    app.run()
