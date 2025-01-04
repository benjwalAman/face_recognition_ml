import customtkinter

# Set appearance and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Create the main window
root = customtkinter.CTk()  # Corrected class name
root.geometry("500x350")

def login():
    print("Login button pressed")

# Create a frame
frame = customtkinter.CTkFrame(master=root)  # Correct class name is CTkFrame
frame.pack(pady=20, padx=60, fill="both", expand=True)  # Expands to fill available space

# Add a label
label = customtkinter.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))  # Correct attribute name 'font'
label.pack(pady=12, padx=10)

# Add username entry
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

# Add password entry
entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

# Add a login button
button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

# Add a "Remember Me" checkbox
checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

# Run the application
root.mainloop()
