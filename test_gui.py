#!/usr/bin/env python3
import tkinter as tk

def test_basic_gui():
    root = tk.Tk()
    root.title("Test GUI")

    label = tk.Label(root, text="Test GUI - Click to close")
    label.pack(padx=20, pady=20)

    def close_app():
        root.destroy()

    button = tk.Button(root, text="Close", command=close_app)
    button.pack(pady=10)

    print("Starting GUI...")
    root.mainloop()
    print("GUI closed")

if __name__ == "__main__":
    test_basic_gui()