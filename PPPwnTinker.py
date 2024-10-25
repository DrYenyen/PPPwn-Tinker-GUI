import tkinter as tk
from tkinter import ttk 
import os 
import subprocess
import re
from tkinter import filedialog
import platform

def get_network_interfaces_unified():
    if platform.system() == "Windows":
        #powershell command to get net adapters
        localPSCommand = ["powershell", "-Command", "Get-NetAdapter | Select-Object InterfaceDescription, InterfaceGuid"]
        result = subprocess.run(localPSCommand, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

        #split the output into lines and remove the header lines
        lines = result.stdout.strip().splitlines()[2:]
        ifNames = []
        ifIds = []

        # Regex pattern to match lines with the format: <description> <guid>
        pattern = re.compile(r"^(.*)\s+({[A-F0-9-]+})$")

        for line in lines:
            match = pattern.match(line)
            if match:
                # add the interface name and GUID to respective lists
                ifNames.append(match.group(1).strip())
                # Prepend the string "\Device\NPF_" to each GUID so it's all nice for the pppwn command
                ifIds.append(r"\Device\NPF_" + match.group(2).strip())
        # Bundle the names and GUIDs into a dictionary
        interface_dict = dict(zip(ifNames, ifIds))

    elif platform.system() == "Linux":   
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.splitlines():
            if ':' in line:
                interface = line.split(':')[1].strip()
                interfaces.append(interface)
        return interfaces

    else:   #macos
        notSupported = ["Platform not supported."]
        interface_dict = dict(zip(notSupported,notSupported))

    return interface_dict

def update_dropdown(event):
    selected_interface = interface_var.get()
    print(f'Selected Interface: {selected_interface}')

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

# Builds the CMD command across Windows and Linux checks for OS and etc along the way ;/
# To wait or not to wait that is the PADI :0
def run_command():
    if tick_padi.get() == 1:
        doNoWaitPadi = "--no-wait-padi"
    else:
        doNoWaitPadi = ""   
    # IPv6 custom by user or new by Borris      
    use_ipv6_str = cipv6.get() or "9f9f:41ff:9f9f:41ff"
    
    # Console firmware selection 
    firmware_to_use = fw_select_as_text.get()
    selected_version = version_as_text.get()
    bin_selection = fw_select_as_text.get()[:-2] + '' + fw_select_as_text.get()[-2:]
    
    # Inserts chosen Num values or uses default 
    spray = spray_num.get() or "4096"
    pin = pin_num.get() or "4096"
    corrupt = corrupt_num.get() or "1"
    
    # First check is if its running on windows 
    if platform.system() == "Windows":
        if selected_version == "C++":
            command = f"pppwn --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
            subprocess.call(["start", "cmd", "/k", command], shell=True)
            print(command)
        elif selected_version == "Python":
            command = f"python pppwn.py --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage1=bins/{bin_selection}/stage1/stage1.bin --stage2=bins/{bin_selection}/stage2/stage2.bin"
            subprocess.call(["start", "cmd", "/k", command], shell=True)
            print(command)
    elif platform.system() == "Linux":
        #check for terminal type
        terminal_type = None
        if os.path.exists("/usr/bin/konsole") or os.path.exists("/usr/local/bin/konsole"):
            terminal_type = "konsole"
        elif os.path.exists("/usr/bin/gnome-terminal") or os.path.exists("/usr/local/bin/gnome-terminal"):
            terminal_type = "gnome"
        elif os.path.exists("/usr/bin/xfce4-terminal") or os.path.exists("/usr/local/bin/xfce4-terminal"):
            terminal_type = "xfce4"

        if selected_version == "C++":
            current_directory = os.path.dirname(os.path.abspath(__file__))
            command = f"./pppwn --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
                
            if terminal_type == "gnome":  
                subprocess.Popen(['gnome-terminal', '--working-directory', current_directory, '--', 'bash', '-c', command + '; exec bash'])
            elif terminal_type == "konsole":
                subprocess.Popen(['konsole', '--hold', '-e', command])
            elif terminal_type == "xfce4":
                subprocess.Popen(['xfce4-terminal', '--hold', '-e', command])
            else:
                print("No supported terminal found, launching in background...")    ##untested
                subprocess.Popen(['bash', command])
        elif selected_version == "Python":
            current_directory = os.path.dirname(os.path.abspath(__file__))
            command = f"python3 pppwn.py --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage1 bins/{bin_selection}/stage1/stage1.bin --stage2 bins/{bin_selection}/stage2/stage2.bin"
                
            if terminal_type == "gnome":  
                subprocess.Popen(['gnome-terminal', '--working-directory', current_directory, '--', 'bash', '-c', command + '; exec bash'])
            elif terminal_type == "konsole":
                subprocess.Popen(['konsole', '--hold', '-e', command])
            elif terminal_type == "xfce4":
                subprocess.Popen(['xfce4-terminal', '--hold', '-e', command])
            else:
                print("No supported terminal found, launching in background...")    ##untested
                subprocess.Popen(['bash', command])
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

# Interface Selection Windows loaded if on Windows
if platform.system() == "Windows":
    interface_dict = get_network_interfaces_unified()
    interfaces = list(interface_dict.keys())
    interface_text = tk.StringVar(root)
    interface_label = tk.Label(root, text="Select Interface:")
    interface_label.pack()
    interface_dropdown = ttk.Combobox(root, values=interfaces, textvariable=interface_text, state="readonly", width=50)
    interface_dropdown.bind("<<ComboboxSelected>>", on_select)
    interface_dropdown.pack(pady=(0, 5))  # Added padding for better spacing
elif platform.system() == "Linux":
    interface_dict = get_network_interfaces_unified()
    interface_var = tk.StringVar()
    interfaces = get_network_interfaces_unified()
    
    interface_dropdown = ttk.Combobox(root, textvariable=interface_var, values=interfaces, state="readonly")
    interface_dropdown.bind("<<ComboboxSelected>>", update_dropdown)
    interface_dropdown.pack(pady=20)    

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

#If Windows is the current OS allows for some additional options in the GUI
if platform.system() == "Windows":
    # Open Network Connections 
    net_button = tk.Button(root, text="Open Network Settings", command=net_command)
    net_button.pack(pady=(0, 10))  # Added padding for better spacing

    # Open ipconfig 
    ip_button = tk.Button(root, text="Show current IP info", command=ip_command)
    ip_button.pack(pady=(0, 10))  # Added padding for better spacing


# Load user choices on startup
load_user_choices()

root.mainloop()
