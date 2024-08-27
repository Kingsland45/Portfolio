import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar, Entry, Button, Label, END
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_invoice(data, file_path, amount, invoice_number, additional_items=[]):
    # Create a new PDF canvas object
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Get the dimensions of the page
    width, height = letter

    # -----------------------------
    # Set Initial Position and Margins
    # -----------------------------
    left_margin = 0.75 * inch
    top_margin = 0.75 * inch
    y_position = height - top_margin  # Start position below the top margin

    # -----------------------------
    # Draw Borders
    # -----------------------------
    # Outer border
    c.setStrokeColorRGB(0, 0.5, 0)  # Green color
    c.setLineWidth(4)
    c.rect(0.5 * inch, 0.5 * inch, width - inch, height - inch)

    # Inner border
    c.setLineWidth(2)
    c.rect(0.6 * inch, 0.6 * inch, width - 1.2 * inch, height - 1.2 * inch)

    # -----------------------------
    # Company Name Header
    # -----------------------------
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0, 0.5, 0)  # Green color
    c.drawCentredString(width / 2, y_position - 0.5 * inch, "Persnickety Cleaning Company")

    # -----------------------------
    # Date and Invoice Number
    # -----------------------------
    y_position -= 1 * inch  # Space below the header
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)  # Black color

    # Formatting current date
    current_date = datetime.now().strftime("%B %d, %Y")
    c.drawString(left_margin, y_position, f"Date: {current_date}")
    c.drawRightString(width - left_margin, y_position, f"Invoice #: {invoice_number}")

    c.drawRightString(width - left_margin, y_position - 0.2 * inch, "Terms: Net 15 days")

    # -----------------------------
    # Customer Details
    # -----------------------------
    y_position -= 1 * inch  # Space below the date and invoice number
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_position, "Bill To:")

    y_position -= 0.25 * inch  # Space below "Bill To:"
    c.setFont("Helvetica", 12)
    c.drawString(left_margin + 0.1 * inch, y_position, data['Customer Name'])

    y_position -= 0.25 * inch  # Space below the customer name
    c.drawString(left_margin + 0.1 * inch, y_position, data['Customer Address'].split(',')[0])

    y_position -= 0.25 * inch  # Space below the street address
    c.drawString(left_margin + 0.1 * inch, y_position, ', '.join(data['Customer Address'].split(',')[1:]).strip())

    # -----------------------------
    # Description of Charges
    # -----------------------------
    y_position -= 1 * inch  # Space below the customer details
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0.5, 0)  # Green color
    c.drawString(left_margin, y_position, "DESCRIPTION")
    c.drawRightString(width - left_margin, y_position, "AMOUNT")

    # Horizontal line under headers
    y_position -= 0.05 * inch
    c.setLineWidth(1)
    c.line(left_margin, y_position, width - left_margin, y_position)

    # -----------------------------
    # Line Items
    # -----------------------------
    y_position -= 0.5 * inch  # Space below the header line
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  # Black color

    # Service Charge
    c.drawString(left_margin, y_position, "Cleaning Service for Current Month")
    c.drawRightString(width - left_margin, y_position, f"${amount:.2f}")

    # Additional Line Items (if any)
    for description, additional_amount in additional_items:
        y_position -= 0.3 * inch  # Space below the previous item
        c.drawString(left_margin, y_position, description)
        if additional_amount:
            c.drawRightString(width - left_margin, y_position, f"${additional_amount:.2f}")
            amount += additional_amount  # Add to total amount

    # Tax Calculation
    tax_amount = amount * data['Tax Rate'] / 100
    y_position -= 0.5 * inch  # Space below the last line item
    c.drawString(left_margin, y_position, f"Sales Tax ({data['Tax Rate']}%)")
    c.drawRightString(width - left_margin, y_position, f"${tax_amount:.2f}")

    # Subtotal Line
    y_position -= 0.1 * inch  # Space below the tax line
    c.line(left_margin, y_position, width - left_margin, y_position)

    # Total Due
    total_due = amount + tax_amount
    y_position -= 0.5 * inch  # Space below the subtotal line
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_position, "TOTAL DUE")
    c.drawRightString(width - left_margin, y_position, f"${total_due:.2f}")

    # Double underline for Total Due
    y_position -= 0.05 * inch
    c.setLineWidth(1)
    c.line(left_margin, y_position, width - left_margin, y_position)
    y_position -= 0.02 * inch
    c.line(left_margin, y_position, width - left_margin, y_position)

    # -----------------------------
    # Remit To Address
    # -----------------------------
    y_position -= 1 * inch  # Space below the total due
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.drawString(left_margin, y_position, "Remit Payment To:")

    y_position -= 0.25 * inch  # Space below "Remit Payment To:"
    c.setFont("Helvetica", 12)
    c.drawString(left_margin + 0.1 * inch, y_position, "Persnickety Cleaning Company")

    y_position -= 0.25 * inch  # Space below the company name
    c.drawString(left_margin + 0.1 * inch, y_position, "P.O. Box 428803")

    y_position -= 0.25 * inch  # Space below the PO Box address
    c.drawString(left_margin + 0.1 * inch, y_position, "Cincinnati, OH 45242-8803")

    # -----------------------------
    # Footer with Thank You Note
    # -----------------------------
    y_position = 1 * inch  # Position footer above bottom margin
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0.5, 0)  # Green color
    c.drawCentredString(width / 2, y_position + 0.4 * inch, "Persnickety Cleaning Company")

    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.drawCentredString(width / 2, y_position + 0.2 * inch, "Phone: 513-850-0615")

    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, y_position, "Thank you for your business!")

    # Save the PDF document
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
        data.to_csv(csv_file, index=False)
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
    # Update the CSV file path to use the get_resource_path function
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

def list_customers():
    # Update the CSV file path to use the get_resource_path function
    csv_file = get_resource_path('pccCustomerInvoicingData.csv')
    data = load_data(csv_file)
    if data is None:
        messagebox.showerror("Error", f"Failed to load {csv_file}")
        return

    # Create a new window to display the customer list
    customer_window = Toplevel(app)
    customer_window.title("Customer List")

    # Listbox to display customers
    listbox = Listbox(customer_window, width=80, height=20)
    listbox.pack(side="left", fill="y")

    # Scrollbar for the listbox
    scrollbar = Scrollbar(customer_window, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # Add customers to the listbox
    for idx, row in data.iterrows():
        listbox.insert(END, f"{row['CustomerID']}: {row['Customer Name']} - {row['Customer Address']}")

    def add_customer():
        def save_new_customer():
            new_id = id_entry.get().strip()
            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()
            new_tax_rate = tax_rate_entry.get().strip()

            if not (new_id and new_name and new_address and new_tax_rate):
                messagebox.showerror("Input Error", "All fields are required.")
                return

            try:
                new_tax_rate = float(new_tax_rate)
            except ValueError:
                messagebox.showerror("Input Error", "Tax Rate must be a numeric value.")
                return

            # Add the new customer to the DataFrame
            data.loc[len(data)] = [new_name, new_address, new_id, new_tax_rate]
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

        Button(add_window, text="Save", command=save_new_customer).grid(row=4, columnspan=2)

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

            if not (new_name and new_address and new_tax_rate):
                messagebox.showerror("Input Error", "All fields are required.")
                return

            try:
                new_tax_rate = float(new_tax_rate)
            except ValueError:
                messagebox.showerror("Input Error", "Tax Rate must be a numeric value.")
                return

            # Update the DataFrame
            data.at[selected_idx, 'Customer Name'] = new_name
            data.at[selected_idx, 'Customer Address'] = new_address
            data.at[selected_idx, 'Tax Rate'] = new_tax_rate
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

        Button(edit_window, text="Save", command=save_edited_customer).grid(row=3, columnspan=2)

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

    # Buttons to add, edit, and delete customers
    Button(customer_window, text="Add Customer", command=add_customer).pack(side="top", fill="x")
    Button(customer_window, text="Edit Customer", command=edit_customer).pack(side="top", fill="x")
    Button(customer_window, text="Delete Customer", command=delete_customer).pack(side="top", fill="x")

# Setting up the Tkinter GUI
app = tk.Tk()
app.title("Invoice Generator")

# Create a frame to hold the buttons
frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

# Create buttons to trigger invoice generation and customer listing
generate_button = tk.Button(frame, text="Generate Invoices", command=generate_invoices)
generate_button.pack(pady=10)

list_customers_button = tk.Button(frame, text="List Customers", command=list_customers)
list_customers_button.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()
