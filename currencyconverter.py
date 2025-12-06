import requests
import customtkinter as ctk
from tkinter import messagebox


def animate_result():
    
    for i in range(0, 11):
        result_label.update()
        root.after(30)   



def convert_currency():
    amount_inr = amount_entry.get()

    if not amount_inr:
        messagebox.showwarning("Input Error", "Please enter an amount in INR")
        return

    try:
        amount_inr = float(amount_inr)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return

    try:
      
        api_url = "https://api.frankfurter.app/latest?from=INR&to=USD"
        response = requests.get(api_url, timeout=5).json()

        usd_rate = response["rates"]["USD"]
        amount_usd = amount_inr * usd_rate

        result_label.configure(
            text=f"₹ {amount_inr:.2f} INR =  {amount_usd:.2f} USD\n\n"
                 f"Live Rate: 1 INR = {usd_rate:.4f} USD"
        )

        animate_result() 

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Internet connection issue.")
    except KeyError:
        messagebox.showerror("Error", "API response format changed.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title(" Cloud Currency Converter (Animated Theme)")
root.geometry("600x600")
root.configure(fg_color="#ffebf3")

frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#ffc1d9")
frame.pack(pady=20, padx=20, fill="both", expand=True)

title_label = ctk.CTkLabel(
    frame,
    text=" Cloud Currency Converter\n(INR → USD)",
    font=("Arial Rounded MT Bold", 26),
    text_color="white"
)
title_label.pack(pady=40)

amount_entry = ctk.CTkEntry(
    frame,
    placeholder_text="Enter amount in INR",
    width=300,
    height=45,
    font=("Arial", 17),
    fg_color="white",
    text_color="black",
    placeholder_text_color="#ff69b4",
    border_color="#ff80ab"
)
amount_entry.pack(pady=15)

convert_button = ctk.CTkButton(
    frame,
    text="Convert",
    width=220,
    height=50,
    font=("Arial", 18, "bold"),
    fg_color="#ff80ab",
    hover_color="#ff5c8a",
    text_color="white",
    command=convert_currency
)
convert_button.pack(pady=15)

result_label = ctk.CTkLabel(
    frame,
    text="",
    font=("Arial", 20),
    text_color="white"
)
result_label.pack(pady=30)


root.mainloop()
