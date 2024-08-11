import tkinter as tk
from tkinter import ttk 
import os 
import subprocess
import re

# Adapter list
# Function to execute a command in cmd and save the output to a text file
def execute_command_and_save_output(command, output_file):
    os.system(f'{command} > {output_file}')

command = 'pppwn.exe list'
output_file = 'output.txt'

execute_command_and_save_output(command, output_file)


def run_command():
    if tick_var.get() == 1:
        use_ipv6_str = "--use-old-ipv6"
    else:
        use_ipv6_str = ""
    
    #interfaceIndex = interface_dropdown.current()
    firmware_to_use = fw_select_as_text.get()
    selected_version = version_as_text.get()
    bin_selection = fw_select_as_text.get()[:-2] + '' + fw_select_as_text.get()[-2:]

    spray = spray_num.get()
    if not spray:
        spray = "4096"
    pin = pin_num.get()
    if not pin:
        pin = "4096"
    corrupt = corrupt_num.get()
    if not corrupt:
        corrupt = "1"
    #

    # i disagree with the structure for the stage1 & stage2, i think it should be stage1/stage1-11.00.bin, not 11.00/stage1/stage1.bin
    if selected_version == "C++":
        command = f"pppwn --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} {use_ipv6_str} --auto-retry"
        subprocess.call(["start", "cmd", "/k", command], shell=True)
        print(command)
    elif selected_version == "Python": 
        command = f"python3 pppwn.py --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} {use_ipv6_str} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin"
        subprocess.call(["start", "cmd", "/k", command], shell=True)
        print(command)


def on_select(event):
    selected_name = interface_dropdown.get()
    selected_id = interface_dict.get(selected_name)
    print(f"Selected Interface: {selected_name}, ID: {selected_id}")
    


root = tk.Tk()
root.geometry('460x605')
root.title("PPPwn Tinker")

# Interface Selection
with open('output.txt', 'r') as file:
    text = file.read()
    ids = re.findall(r'\\Device\\NPF_\{[^}]+\}', text)
    names = re.findall(r'\\Device\\NPF_[^}]+\} (.+)', text)

interface_dict = dict(zip(names, ids))

interfaces = list(interface_dict.keys())
interface_text = tk.StringVar(root)
#interface_text.set(interfaces[0].keys())       
interface_label = tk.Label(root, text="Select Interface:")
interface_label.grid(pady=(1000,100))
interface_label.pack()
# interface dropdown
interface_dropdown = ttk.Combobox(root, values=interfaces, textvariable=interface_text, state="readonly", width=50)
interface_dropdown.bind("<<ComboboxSelected>>", on_select)
interface_dropdown.pack()
# Firmware Selection
firmwaresList = ["1100", "1071", "1050", "1001", "1000", "960", "951", "950", "904", "903", "902", "900", "852", "850", "803", "801", "800", "755", "751", "750", "702", "700"]
sel_fw_label = tk.Label(root, text="Select Firmware:")
sel_fw_label.pack()
fw_select_as_text = tk.StringVar(root)
fw_select_as_text.set(firmwaresList[0])  # Default selection
fw_dropdown = ttk.Combobox(root, textvariable=fw_select_as_text, values=firmwaresList, state="readonly", width=10)
fw_dropdown.pack()
# Version Selection
versionsList = ["C++", "Python"]
version_as_text = tk.StringVar(root)
version_as_text.set(versionsList[0])  # Default selection
version_label = tk.Label(root, text="Select PPPwn Version")
version_label.pack()
version_dropdown = ttk.Combobox(root, textvariable=version_as_text, values=versionsList, state="readonly", width=5)
version_dropdown.pack()
# Old IPV6 selection
tick_var = tk.IntVar()
tickbox = tk.Checkbutton(root, text="Tick to use old IPv6", variable=tick_var)
tickbox.pack()
# Corrupt Num Setting
corruptLabel = tk.Label(root, text="Corrupt Num (Default 0x1000)")
corruptLabel.pack()
corrupt_num = tk.Entry(root)
corrupt_num.pack()
# Pin Setting 
pinLabel = tk.Label(root, text="Pin Num (Default 0x1000)")
pinLabel.pack()
pin_num = tk.Entry(root)
pin_num.pack()
# Spray Setting 
sprayLabel = tk.Label(root, text="Spray Num (Default 0x1)")
sprayLabel.pack()
spray_num = tk.Entry(root)
spray_num.pack()
#Run Button
run_button = tk.Button(root, text="Run PPPwn", command=run_command)
run_button.pack()
root.mainloop()