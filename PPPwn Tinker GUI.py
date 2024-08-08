import tkinter as tk
from tkinter import PhotoImage
from tkinter import Label
import os 
from scapy.arch import get_if_list
import subprocess

def run_command():
    interface = interface_var.get()
    firmware = firmware_var.get()
    selected_version = version_var.get()
    if selected_version == "C++":
        command = f"pppwn --interface \\Device\\NPF_{interface} --fw {firmware}"
        subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    elif selected_version == "Python": 
        command = f"python3 pppwn.py --interface=\\Device\\NPF_{interface} --fw={firmware}"
        subprocess.Popen(["start", "cmd", "/k", command], shell=True)

root = tk.Tk()
root.geometry('460x605')
root.title("PPPwn Tinker")

# Interface Selection
interfaces = get_if_list()
interface_var = tk.StringVar(root)
interface_var.set(interfaces[0])  # Default selection

interface_label = tk.Label(root, text="Select Interface:")
interface_label.pack()

interface_dropdown = tk.OptionMenu(root, interface_var, *interfaces)
interface_dropdown.pack()

# Firmware Selection
firmwares = ["1100", "1001" ,"1000"]
firmware_var = tk.StringVar(root)
firmware_var.set(firmwares[0])  # Default selection

firmware_label = tk.Label(root, text="Select Firmware:")
firmware_label.pack()

firmware_dropdown = tk.OptionMenu(root, firmware_var, *firmwares)
firmware_dropdown.pack()

# Version Selection
versions = ["C++", "Python"]
version_var = tk.StringVar(root)
version_var.set(versions[0]) # Default selection

version_label = tk.Label(root, text="Select PPPwn Version")
version_label.pack()

version_dropdown = tk.OptionMenu(root, version_var, *versions)
version_dropdown.pack()

#Run Button
run_button = tk.Button(root, text="Run PPPwn", command=run_command)
run_button.pack()

root.mainloop()
