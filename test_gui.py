#!/usr/bin/env python3
import tkinter as tk
import pytest
import os

@pytest.mark.skipif(os.environ.get("DISPLAY") is None, reason="requires a display")
def test_basic_gui():
    root = tk.Tk()
    root.title("Test GUI")

    label = tk.Label(root, text="Test GUI - Click to close")
    label.pack(padx=20, pady=20)

    def close_app():
        root.destroy()

    button = tk.Button(root, text="Close", command=close_app)
    button.pack(pady=10)

    # Close the window after a short time
    root.after(100, close_app)

    root.mainloop()
