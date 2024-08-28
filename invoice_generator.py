import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar, Entry, Button, Label, END
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from cryptography.fernet import Fernet

# Utility functions for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Function to store email credentials securely
def save_credentials(email, password):
    with open("credentials.txt", "wb") as cred_file:
        cred_file.write(encrypt_message(email) + b"\n" + encrypt_message(password))

# Function to load email credentials
def load_credentials():
    try:
        with open("credentials.txt", "rb") as cred_file:
            lines = cred_file.readlines()
            email = decrypt_message(lines[0].strip())
            password = decrypt_message(lines[1].strip())
            return email, password
    except Exception as e:
        print(f"Failed to load credentials: {e}")
        return None, None

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_invoice(data, file_path, amount, invoice_number, additional_items=[]):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    left_margin = 0.75 * inch
    top_margin = 0.75 * inch
    y_position = height - top_margin

    c.setStrokeColorRGB(0, 0.5, 0) 
    c.setLineWidth(4)
    c.rect(0.5 * inch, 0.5 * inch, width - inch, height - inch)

    c.setLineWidth(2)
    c.rect(0.6 * inch, 0.6 * inch, width - 1.2 * inch, height - 1.2 * inch)

    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0, 0.5, 0)  
    c.drawCentredString(width / 2, y_position - 0.5 * inch, "Persnickety Cleaning Company")

    y_position -= 1 * inch  
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0) 

    current_date = datetime.now().strftime("%B %d, %Y")
    c.drawString(left_margin, y_position, f"Date: {current_date}")
    c.drawRightString(width - left_margin, y_position, f"Invoice #: {invoice_number}")
    c.drawRightString(width - left_margin, y_position - 0.2 * inch, "Terms: Net 15 days")

    y_position -= 1 * inch  
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_position, "Bill To:")

    y_position -= 0.25 * inch  
    c.setFont("Helvetica", 12)
    
    # Check and clean the Customer Name
    customer_name = data.get('Customer Name', '').strip()
    if not customer_name:
        customer_name = "Unknown Customer"
    
    c.drawString(left_margin + 0.1 * inch, y_position, customer_name)

    y_position -= 0.25 * inch  
    customer_address = data.get('Customer Address', '').strip('"')
    c.drawString(left_margin + 0.1 * inch, y_position, customer_address)

    y_position -= 1 * inch  
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0.5, 0)  
    c.drawString(left_margin, y_position, "DESCRIPTION")
    c.drawRightString(width - left_margin, y_position, "AMOUNT")

    y_position -= 0.05 * inch
    c.setLineWidth(1)
    c.line(left_margin, y_position, width - left_margin, y_position)

    y_position -= 0.5 * inch  
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  

    c.drawString(left_margin, y_position, "Cleaning Service for Current Month")
    c.drawRightString(width - left_margin, y_position, f"${amount:.2f}")

    for description, additional_amount in additional_items:
        y_position -= 0.3 * inch 
        c.drawString(left_margin, y_position, description)
        if additional_amount:
            c.drawRightString(width - left_margin, y_position, f"${additional_amount:.2f}")
            amount += additional_amount 

    tax_amount = amount * data['Tax Rate'] / 100
    y_position -= 0.5 * inch  
    c.drawString(left_margin, y_position, f"Sales Tax ({data['Tax Rate']}%)")
    c.drawRightString(width - left_margin, y_position, f"${tax_amount:.2f}")

    y_position -= 0.1 * inch  
    c.line(left_margin, y_position, width - left_margin, y_position)

    total_due = amount + tax_amount
    y_position -= 0.5 * inch  
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_position, "TOTAL DUE")
    c.drawRightString(width - left_margin, y_position, f"${total_due:.2f}")

    y_position -= 0.05 * inch
    c.setLineWidth(1)
    c.line(left_margin, y_position, width - left_margin, y_position)
    y_position -= 0.02 * inch
    c.line(left_margin, y_position, width - left_margin, y_position)

    y_position -= 1 * inch  
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)  
    c.drawString(left_margin, y_position, "Remit Payment To:")

    y_position -= 0.25 * inch  
    c.setFont("Helvetica", 12)
    c.drawString(left_margin + 0.1 * inch, y_position, "Persnickety Cleaning Company")

    y_position -= 0.25 * inch  
    c.drawString(left_margin + 0.1 * inch, y_position, "P.O. Box 428803")

    y_position -= 0.25 * inch  
    c.drawString(left_margin + 0.1 * inch, y_position, "Cincinnati, OH 45242-8803")

    y_position = 1 * inch  
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0.5, 0)  
    c.drawCentredString(width / 2, y_position + 0.4 * inch, "Persnickety Cleaning Company")

    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  
    c.drawCentredString(width / 2, y_position + 0.2 * inch, "Phone: 513-850-0615")

    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, y_position, "Thank you for your business!")

    c.save()

def load_data(csv_file):
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

def save_data(csv_file, data):
    try:
        # Save the data to the CSV file with quoting for all fields
        data.to_csv(csv_file, index=False, quoting=1, quotechar='"')
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        messagebox.showerror("Error", "Failed to save data to CSV file.")

def create_monthly_directory():
    now = datetime.now()
    month_dir = now.strftime("%Y-%m")
    if not os.path.exists(month_dir):
        try:
            os.makedirs(month_dir)
        except Exception as e:
            print(f"An error occurred while creating the directory: {e}")
            return None
    return month_dir

def generate_invoices():
    csv_file = get_resource_path('pccCustomerInvoicingData.csv')
    data = load_data(csv_file)
    if data is None:
        messagebox.showerror("Error", f"Failed to load {csv_file}")
        return
    
    month_dir = create_monthly_directory()
    if month_dir is None:
        messagebox.showerror("Error", "Failed to create directory for storing invoices.")
        return
    
    current_month = datetime.now().strftime("%m")
    current_year = datetime.now().strftime("%y")
    
    for _, row in data.iterrows():
        try:
            amount = float(simpledialog.askstring("Billing Amount", f"Enter the billing amount for {row['Customer Name']}:"))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric value for the amount.")
            return
        
        additional_items = []
        for _ in range(3):  # Allow up to 3 additional items
            add_extra = messagebox.askyesno("Additional Line", "Would you like to add an extra line?")
            if not add_extra:
                break
            description = simpledialog.askstring("Line Description", "Enter the description (max 50 characters):")[:50]
            additional_amount = None
            add_amount = messagebox.askyesno("Additional Charge", "Is there an additional charge for this?")
            if add_amount:
                try:
                    additional_amount = float(simpledialog.askstring("Additional Amount", "Enter the additional amount:"))
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid numeric value for the additional amount.")
                    return
            additional_items.append((description, additional_amount))

        invoice_number = f"{row['CustomerID']}{current_month}{current_year}"
        invoice_file = os.path.join(month_dir, f"invoice_{invoice_number}.pdf")
        create_invoice(row, invoice_file, amount, invoice_number, additional_items)
        messagebox.showinfo("Invoice Created", f"Invoice created: {invoice_file}")

def email_invoice_to_customer(row):
    month_dir = create_monthly_directory()
    if month_dir is None:
        messagebox.showerror("Error", "Failed to create directory for storing invoices.")
        return

    current_month = datetime.now().strftime("%m")
    current_year = datetime.now().strftime("%y")
    invoice_number = f"{row['CustomerID']}{current_month}{current_year}"
    invoice_file = os.path.join(month_dir, f"invoice_{invoice_number}.pdf")
    recipient = row['Email1']

    if row['Email2'].strip().lower() != 'void':
        recipient += f",{row['Email2']}"

    if not os.path.exists(invoice_file):
        messagebox.showerror("Error", f"Invoice file not found for {row['Customer Name']}. Please generate the invoices first.")
        return
    
    subject = f"Invoice {invoice_number} from Persnickety Cleaning Company"
    body = f"Dear {row['Customer Name']},\n\nPlease find attached the invoice {invoice_number} for your recent service.\n\nThank you for your business.\n\nPersnickety Cleaning Company"
    
    if send_email(recipient, subject, body, attachments=[invoice_file]):
        messagebox.showinfo("Email Sent", f"Invoice {invoice_number} sent to {recipient}")
    else:
        messagebox.showerror("Email Failed", f"Failed to send invoice {invoice_number} to {recipient}")

def email_invoices_window():
    csv_file = get_resource_path('pccCustomerInvoicingData.csv')
    data = load_data(csv_file)
    if data is None:
        messagebox.showerror("Error", f"Failed to load {csv_file}")
        return

    # Create a new window to display the customer list for emailing invoices
    email_window = Toplevel(app)
    email_window.title("Email Invoices")

    listbox = Listbox(email_window, width=80, height=20)
    listbox.pack(side="left", fill="y")

    scrollbar = Scrollbar(email_window, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    for idx, row in data.iterrows():
        listbox.insert(END, f"{row['CustomerID']}: {row['Customer Name']} - {row['Customer Address']}")

    def send_selected_invoice():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a customer to email the invoice.")
            return
        selected_idx = selected[0]
        selected_customer = data.iloc[selected_idx]
        email_invoice_to_customer(selected_customer)

    def email_all_invoices():
        for _, row in data.iterrows():
            email_invoice_to_customer(row)

    # Button to send selected invoice
    Button(email_window, text="Send Invoice", command=send_selected_invoice).pack(side="top", fill="x")

    # Button to send all invoices
    Button(email_window, text="Email All Invoices", command=email_all_invoices).pack(side="top", fill="x")

def list_customers():
    csv_file = get_resource_path('pccCustomerInvoicingData.csv')
    data = load_data(csv_file)
    if data is None:
        messagebox.showerror("Error", f"Failed to load {csv_file}")
        return

    customer_window = Toplevel(app)
    customer_window.title("Customer List")

    listbox = Listbox(customer_window, width=80, height=20)
    listbox.pack(side="left", fill="y")

    scrollbar = Scrollbar(customer_window, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    for idx, row in data.iterrows():
        listbox.insert(END, f"{row['CustomerID']}: {row['Customer Name']} - {row['Customer Address']}")

    def add_customer():
        def save_new_customer():
            new_id = id_entry.get().strip()
            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()
            new_tax_rate = tax_rate_entry.get().strip()
            new_email1 = email1_entry.get().strip()
            new_email2 = email2_entry.get().strip()

            if not (new_id and new_name and new_address and new_tax_rate and new_email1):
                messagebox.showerror("Input Error", "All fields except Email2 are required.")
                return

            try:
                new_tax_rate = float(new_tax_rate)
            except ValueError:
                messagebox.showerror("Input Error", "Tax Rate must be a numeric value.")
                return

            # Set default value for Email2 if left blank
            if not new_email2:
                new_email2 = "void"

            data.loc[len(data)] = [new_name, new_address, new_id, new_tax_rate, new_email1, new_email2]
            save_data(csv_file, data)
            listbox.insert(END, f"{new_id}: {new_name} - {new_address}")
            add_window.destroy()

        add_window = Toplevel(customer_window)
        add_window.title("Add New Customer")

        Label(add_window, text="Customer ID:").grid(row=0, column=0)
        id_entry = Entry(add_window)
        id_entry.grid(row=0, column=1)

        Label(add_window, text="Customer Name:").grid(row=1, column=0)
        name_entry = Entry(add_window)
        name_entry.grid(row=1, column=1)

        Label(add_window, text="Customer Address:").grid(row=2, column=0)
        address_entry = Entry(add_window)
        address_entry.grid(row=2, column=1)

        Label(add_window, text="Tax Rate:").grid(row=3, column=0)
        tax_rate_entry = Entry(add_window)
        tax_rate_entry.grid(row=3, column=1)

        Label(add_window, text="Email1:").grid(row=4, column=0)
        email1_entry = Entry(add_window)
        email1_entry.grid(row=4, column=1)

        Label(add_window, text="Email2:").grid(row=5, column=0)
        email2_entry = Entry(add_window)
        email2_entry.grid(row=5, column=1)

        Button(add_window, text="Save", command=save_new_customer).grid(row=6, columnspan=2)

    def edit_customer():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a customer to edit.")
            return

        selected_idx = selected[0]
        selected_customer = data.iloc[selected_idx]

        def save_edited_customer():
            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()
            new_tax_rate = tax_rate_entry.get().strip()
            new_email1 = email1_entry.get().strip()
            new_email2 = email2_entry.get().strip()

            if not (new_name and new_address and new_tax_rate and new_email1):
                messagebox.showerror("Input Error", "All fields except Email2 are required.")
                return

            try:
                new_tax_rate = float(new_tax_rate)
            except ValueError:
                messagebox.showerror("Input Error", "Tax Rate must be a numeric value.")
                return

            # Set default value for Email2 if left blank
            if not new_email2:
                new_email2 = "void"

            data.at[selected_idx, 'Customer Name'] = new_name
            data.at[selected_idx, 'Customer Address'] = new_address
            data.at[selected_idx, 'Tax Rate'] = new_tax_rate
            data.at[selected_idx, 'Email1'] = new_email1
            data.at[selected_idx, 'Email2'] = new_email2
            save_data(csv_file, data)
            listbox.delete(selected_idx)
            listbox.insert(selected_idx, f"{selected_customer['CustomerID']}: {new_name} - {new_address}")
            edit_window.destroy()

        edit_window = Toplevel(customer_window)
        edit_window.title("Edit Customer")

        Label(edit_window, text="Customer Name:").grid(row=0, column=0)
        name_entry = Entry(edit_window)
        name_entry.insert(0, selected_customer['Customer Name'])
        name_entry.grid(row=0, column=1)

        Label(edit_window, text="Customer Address:").grid(row=1, column=0)
        address_entry = Entry(edit_window)
        address_entry.insert(0, selected_customer['Customer Address'])
        address_entry.grid(row=1, column=1)

        Label(edit_window, text="Tax Rate:").grid(row=2, column=0)
        tax_rate_entry = Entry(edit_window)
        tax_rate_entry.insert(0, selected_customer['Tax Rate'])
        tax_rate_entry.grid(row=2, column=1)

        Label(edit_window, text="Email1:").grid(row=3, column=0)
        email1_entry = Entry(edit_window)
        email1_entry.insert(0, selected_customer['Email1'])
        email1_entry.grid(row=3, column=1)

        Label(edit_window, text="Email2:").grid(row=4, column=0)
        email2_entry = Entry(edit_window)
        email2_entry.insert(0, selected_customer['Email2'])
        email2_entry.grid(row=4, column=1)

        Button(edit_window, text="Save", command=save_edited_customer).grid(row=5, columnspan=2)

    def delete_customer():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a customer to delete.")
            return

        selected_idx = selected[0]
        confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this customer?")
        if confirmation:
            data.drop(index=selected_idx, inplace=True)
            save_data(csv_file, data)
            listbox.delete(selected_idx)

    Button(customer_window, text="Add Customer", command=add_customer).pack(side="top", fill="x")
    Button(customer_window, text="Edit Customer", command=edit_customer).pack(side="top", fill="x")
    Button(customer_window, text="Delete Customer", command=delete_customer).pack(side="top", fill="x")

def send_email(recipient, subject, body, attachments=[]):
    email, password = load_credentials()
    if not email or not password:
        messagebox.showerror("Error", "Email credentials are not set.")
        return False

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file)}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, recipient, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Credential Management GUI
def manage_credentials():
    def save_new_credentials():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Input Error", "Both email and password are required.")
            return

        save_credentials(email, password)
        messagebox.showinfo("Success", "Credentials saved successfully.")
        cred_window.destroy()

    cred_window = Toplevel(app)
    cred_window.title("Manage Credentials")

    Label(cred_window, text="Email:").grid(row=0, column=0)
    email_entry = Entry(cred_window)
    email_entry.grid(row=0, column=1)

    Label(cred_window, text="Password:").grid(row=1, column=0)
    password_entry = Entry(cred_window, show="*")
    password_entry.grid(row=1, column=1)

    Button(cred_window, text="Save", command=save_new_credentials).grid(row=2, columnspan=2)

# Setting up the Tkinter GUI
app = tk.Tk()
app.title("Invoice Generator")

frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

generate_button = tk.Button(frame, text="Generate Invoices", command=generate_invoices)
generate_button.pack(pady=10)

list_customers_button = tk.Button(frame, text="List Customers", command=list_customers)
list_customers_button.pack(pady=10)

email_invoices_button = tk.Button(frame, text="Email Invoices", command=email_invoices_window)
email_invoices_button.pack(pady=10)

manage_credentials_button = tk.Button(frame, text="Manage Credentials", command=manage_credentials)
manage_credentials_button.pack(pady=10)

app.mainloop()
