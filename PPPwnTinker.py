import tkinter as tk
from tkinter import ttk 
import os 
import subprocess
import re

# Function to execute a command in cmd and save the output to a text file
def execute_command_and_save_output(command, output_file):
    os.system(f'{command} > {output_file}')

command = 'pppwn.exe list'
output_file = 'interfaces.txt'

execute_command_and_save_output(command, output_file)

#Choose which choices get saved
def save_user_choices():
    with open('user_choices.txt', 'w') as file:
        file.write(f"{fw_select_as_text.get()}\n")
        file.write(f"{version_as_text.get()}\n")
        file.write(f"{spray_num.get()}\n")
        file.write(f"{pin_num.get()}\n")
        file.write(f"{corrupt_num.get()}\n")
        file.write(f"{interface_dropdown.get()}\n")
        file.write(f"{cipv6.get()}\n")
        file.write(f"{tick_padi.get()}\n")
        file.close()

#Load saved choises
def load_user_choices():
    if os.path.exists('user_choices.txt'):
        with open('user_choices.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 8:
                fw_select_as_text.set(lines[0].strip())
                version_as_text.set(lines[1].strip())
                spray_num.insert(0, lines[2].strip())
                pin_num.insert(0, lines[3].strip())
                corrupt_num.insert(0, lines[4].strip())
                interface_dropdown.set(lines[5].strip())
                cipv6.insert(0, lines[6].strip())
                tick_padi.set(int(lines[7].strip()))
                file.close()

# Builds the CMD command ;/
# To wait or not to wait that is the PADI :0
def run_command():
    if tick_padi.get() == 1:
        Nowait = "--no-wait-padi"
    else:
        Nowait = ""
#ipv6 custom by user or new by Borris      
    use_ipv6_str = cipv6.get() or "9f9f:41ff:9f9f:41ff"
#Console firmare selection    
    firmware_to_use = fw_select_as_text.get()
    selected_version = version_as_text.get()
    bin_selection = fw_select_as_text.get()[:-2] + '' + fw_select_as_text.get()[-2:]
#Inserts chosen Num values or uses default 
    spray = spray_num.get() or "4096"
    pin = pin_num.get() or "4096"
    corrupt = corrupt_num.get() or "1"
#C++ command
    if selected_version == "C++":
        command = f"pppwn --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} --auto-retry {Nowait}"
        subprocess.call(["start", "cmd", "/k", command], shell=True)
        print(command)
#Python command
    elif selected_version == "Python": 
        command = f"python pppwn.py --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin"
        subprocess.call(["start", "cmd", "/k", command], shell=True)
        print(command)


# Open Network Connections command idk just if someone wants it
def net_command():
    command = f"ncpa.cpl"
    subprocess.Popen('ncpa.cpl', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    print(command)

# Open CMD ipconfig just cuz
def ip_command():
    command = f"ipconfig"
    subprocess.call(["start", "cmd", "/k", command], shell=True)
    print(command)

#Select interface
def on_select(event):
    selected_name = interface_dropdown.get()
    selected_id = interface_dict.get(selected_name)
    print(f"Selected Interface: {selected_name}, ID: {selected_id}")

# Builds the GUI window and sets a window icon
root = tk.Tk()
root.geometry('600x700')
root.title("PPPwn Tinker")
root.iconbitmap('imgs/icon.ico')

# Load background image
if os.path.exists("imgs/background.png"):
    background_image = tk.PhotoImage(file="imgs/background.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

# Interface Selection
with open('interfaces.txt', 'r') as file:
    text = file.read()
    ids = re.findall(r'\\Device\\NPF_\{[^}]+\}', text)
    names = re.findall(r'\\Device\\NPF_[^}]+\} (.+)', text)

interface_dict = dict(zip(names, ids))

interfaces = list(interface_dict.keys())
interface_text = tk.StringVar(root)
interface_label = tk.Label(root, text="Select Interface:")
interface_label.pack()
interface_dropdown = ttk.Combobox(root, values=interfaces, textvariable=interface_text, state="readonly", width=50)
interface_dropdown.bind("<<ComboboxSelected>>", on_select)
interface_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

# Firmware Selection
firmwaresList = ["1100", "1071", "1070", "1050", "1001", "1000", "960", "951", "950", "904", "903", "900", "852", "850", "803", "801", "800", "755", "751", "750", "702", "700"]
sel_fw_label = tk.Label(root, text="Select Firmware:")
sel_fw_label.pack() 
fw_select_as_text = tk.StringVar(root)
fw_select_as_text.set(firmwaresList[0])  # Default selection
fw_dropdown = ttk.Combobox(root, textvariable=fw_select_as_text, values=firmwaresList, state="readonly", width=10)
fw_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

# Version Selection
versionsList = ["C++", "Python"]
version_as_text = tk.StringVar(root)
version_as_text.set(versionsList[0])  # Default selection
version_label = tk.Label(root, text="Select PPPwn Version")
version_label.pack() 
version_dropdown = ttk.Combobox(root, textvariable=version_as_text, values=versionsList, state="readonly", width=8)
version_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

# Corrupt Num Setting
corruptLabel = tk.Label(root, text="Corrupt Num (Default 0x1)(Default will be used if blank)")
corruptLabel.pack()  
corrupt_num = tk.Entry(root)
corrupt_num.pack(pady=(0, 5))  # Added padding for better spacing

# Pin Setting 
pinLabel = tk.Label(root, text="Pin Num (Default 0x1000)(Default will be used if blank)")
pinLabel.pack()  
pin_num = tk.Entry(root)
pin_num.pack(pady=(0, 5))  # Added padding for better spacing

# Spray Setting 
sprayLabel = tk.Label(root, text="Spray Num (Default 0x1000)(Default will be used if blank)")
sprayLabel.pack() 
spray_num = tk.Entry(root)
spray_num.pack(pady=(0, 5))  # Added padding for better spacing

# Custom IPV6
ipv6Label = tk.Label(root, text="Custom ipv6 (Default 9f9f:41ff:9f9f:41ff)(Default will be used if blank)")
ipv6Label.pack() 
cipv6 = tk.Entry(root)
cipv6.pack(pady=(0, 5))  # Added padding for better spacing

# No wait for PADI
tick_padi = tk.IntVar()
tickbox = tk.Checkbutton(root, text="Tick to not wait for one more PADI before starting ", variable=tick_padi)
tickbox.pack(pady=(5, 0))  # Added padding for better spacing

# Run PPPwn and save user choices for next startup
run_button = tk.Button(root, text="Run PPPwn", command=lambda: [run_command(), save_user_choices()])
run_button.pack(pady=(10, 10))  # Added padding for better spacing

# Open Network Connections 
net_button = tk.Button(root, text="Open Network Settings", command=net_command)
net_button.pack(pady=(0, 10))  # Added padding for better spacing)

# Open ipconfig 
ip_button = tk.Button(root, text="Show current IP info", command=ip_command)
ip_button.pack(pady=(0, 10))  # Added padding for better spacing)


# Load user choices on startup
load_user_choices()

root.mainloop()