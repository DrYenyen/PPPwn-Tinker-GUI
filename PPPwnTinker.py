import tkinter as tk
from tkinter import ttk 
import os 
import subprocess
import re
import sys
from tkinter import filedialog
import platform
from tkinter import PhotoImage

# Reads interfaces based on OS it is slightly repetitive for Windows
def get_network_interfaces_unified():
    if platform.system() == "Windows":
        windows_version = platform.release()  

        if windows_version in ("10","11"):
            # PowerShell command to get net adapters
            localPSCommand = ["powershell", "-Command", "Get-NetAdapter | Select-Object InterfaceDescription, InterfaceGuid"]
            result = subprocess.run(localPSCommand, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Split the output into lines and remove the header lines
            lines = result.stdout.strip().splitlines()[2:]
            ifNames = []
            ifIds = []

            # Regex pattern to match lines with the format: <description> <guid>
            pattern = re.compile(r"^(.*)\s+({[A-F0-9-]+})$")

            for line in lines:
                match = pattern.match(line)
                if match:
                    # Add the interface name and GUID to respective lists
                    ifNames.append(match.group(1).strip())
                    # Prepend the string "\Device\NPF_" to each GUID for compatibility
                    ifIds.append(r"\Device\NPF_" + match.group(2).strip())
            # Bundle the names and GUIDs into a dictionary
            interface_dict = dict(zip(ifNames, ifIds))

        elif windows_version in ("8", "8.1"):
            # PowerShell command to get network adapters 
            localPSCommand = ["powershell", "-Command", "Get-WmiObject Win32_NetworkAdapter | Select-Object Name, GUID"]
            result = subprocess.run(localPSCommand, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Split the output into lines and remove header lines
            lines = result.stdout.strip().splitlines()[2:]
            ifNames = []
            ifIds = []

            # Regex pattern to match lines with the format: <name> <guid>
            pattern = re.compile(r"^(.*?)\s+({[A-F0-9a-f-]+})$")

            for line in lines:
                match = pattern.match(line.strip())
                if match:
                    # Add the interface name and GUID to respective lists
                    ifNames.append(match.group(1).strip())
                    # Prepend the string "\Device\NPF_" to each GUID for compatibility
                    ifIds.append(r"\Device\NPF_" + match.group(2).strip())

            # Bundle the names and GUIDs into a dictionary
            interface_dict = dict(zip(ifNames, ifIds))

        elif windows_version == "7":
            # PowerShell command to get net adapters
            localPSCommand = ["powershell", "-Command", "Get-WmiObject Win32_NetworkAdapter | Select-Object Name, GUID"]
            result = subprocess.run(localPSCommand, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Split the output into lines and remove the header lines
            lines = result.stdout.strip().splitlines()[2:]
            ifNames = []
            ifIds = []

            # Regex pattern to match lines with the format: <description> <guid>
            pattern = re.compile(r"^(.*)\s+({[A-F0-9-]+})\s*$")

            for line in lines:
                match = pattern.match(line)
                if match:
                    # Add the interface name and GUID to respective lists
                    ifNames.append(match.group(1).strip())
                    # Prepend the string "\Device\NPF_" to each GUID for compatibility
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

    elif platform.system() == "Darwin": 
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.splitlines():
            if line.startswith('en') or line.startswith('eth'):
                interfaces.append(line.split(':')[0])
        return interfaces

    else:
        notSupported = ["Platform not supported."]
        interface_dict = dict(zip(notSupported, notSupported))

    return interface_dict

# Select interface Windows
def on_select(event):
    selected_name = interface_dropdown.get()
    selected_id = interface_dict.get(selected_name)
    print(f"Selected Interface: {selected_name}, ID: {selected_id}")

# Select interface Linux and macOS
def update_dropdown(event):
    selected_interface = interface_var.get()
    print(f'Selected Interface: {selected_interface}')


# Gets the home directory path for saving user choices this makes it so that when redownloading the GUI you don't need to set it up again
def get_file_path(filename):
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, filename)

# Saves user choices
def save_user_choices():
    file_path = get_file_path('user_choices.txt')
    with open(file_path, 'w') as file:
        file.write(f"{fw_select_as_text.get()}\n")
        file.write(f"{version_as_text.get()}\n")
        file.write(f"{spray_num.get()}\n")
        file.write(f"{pin_num.get()}\n")
        file.write(f"{corrupt_num.get()}\n")
        file.write(f"{interface_dropdown.get()}\n")
        file.write(f"{cipv6.get()}\n")
        file.write(f"{tick_padi.get()}\n")
        file.write(f"{root.geometry()}\n")
        file.write(f"{theme_var.get()}\n")  

# Loads user choices
def load_user_choices():
    file_path = get_file_path('user_choices.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 10:
                fw_select_as_text.set(lines[0].strip())
                version_as_text.set(lines[1].strip())
                spray_num.insert(0, lines[2].strip())
                pin_num.insert(0, lines[3].strip())
                corrupt_num.insert(0, lines[4].strip())
                interface_dropdown.set(lines[5].strip())
                cipv6.insert(0, lines[6].strip())
                tick_padi.set(int(lines[7].strip()))
                root.geometry(lines[8].strip())
                theme_var.set(lines[9].strip())
                apply_theme()

# Clears PPPwn related settings including interface selection
def clear_pppwn_settings():
    fw_select_as_text.set('')
    version_as_text.set('')
    spray_num.delete(0, tk.END)
    pin_num.delete(0, tk.END)
    corrupt_num.delete(0, tk.END)
    interface_dropdown.set('')
    cipv6.delete(0, tk.END)
    tick_padi.set(0)
    save_user_choices()

# Reset window size based on OS
def set_window_size():
    if platform.system() == "Windows":
        root.geometry('410x530')  
    elif platform.system() == "Linux":
        root.geometry('470x530')  
    elif platform.system() == "Darwin":
        root.geometry('470x545')  
    save_user_choices()

# Clears GUI size settings
def clear_size_settings(): 
    set_window_size()

# Clears all settings
def clear_all_settings():
    fw_select_as_text.set('')
    version_as_text.set('')
    spray_num.delete(0, tk.END)
    pin_num.delete(0, tk.END)
    corrupt_num.delete(0, tk.END)
    interface_dropdown.set('')
    cipv6.delete(0, tk.END)
    tick_padi.set(0)
    theme_var.set("Dark")
    apply_theme()
    set_window_size()

# Builds the command across Windows,Linux and macOS
def run_command():  
    if tick_padi.get() == 1:  # Checks if ticbox is ticked :/
        doNoWaitPadi = "--no-wait-padi"
    else:
        doNoWaitPadi = ""   
    use_ipv6_str = cipv6.get() or "9f9f:41ff:9f9f:41ff" #Checks if a custom ipv6 is set uses default if not (does not check formatting)
    firmware_to_use = fw_select_as_text.get() # Reads firwmware selection
    selected_version = version_as_text.get() # Reads which pppwn method is being used
    bin_selection = fw_select_as_text.get()[:-2] + '' + fw_select_as_text.get()[-2:] # Sets bin selection name and version based on firmware selection
    spray = spray_num.get() or "4096" # Checks if custom spray num is set uses default if not (does not check formatting)
    pin = pin_num.get() or "4096" # Checks if custom pin num is set uses default if not (does not check formatting)
    corrupt = corrupt_num.get() or "1" # Checks if custom corrupt num is set uses default if not (does not check formatting)
    
    if platform.system() == "Windows":
        # Sub folder for pppwn
        subfolder = "pppwn"
        executable_path = os.path.join(subfolder, "pppwn.exe")
        executable_path_legacy = os.path.join(subfolder, "pppwn7.exe")
        yapppwn_path = os.path.join(subfolder, "yapppwn.exe")
        yapppwn_path_legacy = os.path.join(subfolder, "yapppwn7.exe") 
        pppwn_py_path = os.path.join(subfolder, "pppwn.py")
        
        # Checks Windows version 
        windows_version = platform.release()  

        if windows_version == "7": # Windows 7 needs a different executible for pppwn C++ and Rust
            if selected_version == "C++":
                command = f"{executable_path_legacy} --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2 pppwn/bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
                subprocess.call(["start", "cmd", "/k", command], shell=True)
            elif selected_version == "Rust":
                command = f"{yapppwn_path_legacy} --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage-1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage-2 pppwn/bins/{bin_selection}/stage2/stage2.bin -r 100"
                subprocess.call(["start", "cmd", "/k", command], shell=True)
            elif selected_version == "Python":
                command = f"python {pppwn_py_path} --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage1=pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2=pppwn/bins/{bin_selection}/stage2/stage2.bin"
                subprocess.call(["start", "cmd", "/k", command], shell=True)
        else: 
            if selected_version == "C++": # Windows 8-11 runs the same C++ and Rust compiles
                command = f"{executable_path} --interface {interface_dict.get(interface_dropdown.get())} --fw {firmware_to_use} --stage1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2 pppwn/bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
                subprocess.call(["start", "cmd", "/k", command], shell=True)
            elif selected_version == "Rust":
                command = f"{yapppwn_path} --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage-1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage-2 pppwn/bins/{bin_selection}/stage2/stage2.bin -r 100"
                subprocess.call(["start", "cmd", "/k", command], shell=True)
            elif selected_version == "Python":
                command = f"python {pppwn_py_path} --interface={interface_dict.get(interface_dropdown.get())} --fw={firmware_to_use} --stage1=pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2=pppwn/bins/{bin_selection}/stage2/stage2.bin"
                subprocess.call(["start", "cmd", "/k", command], shell=True)  

    elif platform.system() == "Linux": # Linux command for different DE
        terminal_type = None
        if os.path.exists("/usr/bin/konsole") or os.path.exists("/usr/local/bin/konsole"):
            terminal_type = "konsole"
        elif os.path.exists("/usr/bin/gnome-terminal") or os.path.exists("/usr/local/bin/gnome-terminal"):
            terminal_type = "gnome"
        elif os.path.exists("/usr/bin/xfce4-terminal") or os.path.exists("/usr/local/bin/xfce4-terminal"):
            terminal_type = "xfce4"

        if selected_version == "C++":
            command = f"sudo ./pppwn/pppwn --interface {interface_var.get()} --fw {firmware_to_use} --stage1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2 pppwn/bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
            if terminal_type == "gnome":  
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command + '; exec bash'])
            elif terminal_type == "konsole":
                subprocess.Popen(['konsole', '--hold', '-e', command])
            elif terminal_type == "xfce4":
                subprocess.Popen(['xfce4-terminal', '--hold', '-e', command])
            else:
                subprocess.Popen(['bash', command])
        elif selected_version == "Rust":
            command = f"sudo ./pppwn/yapppwn --interface={interface_var.get()} --fw={firmware_to_use} --stage-1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage-2 pppwn/bins/{bin_selection}/stage2/stage2.bin -r 100"     
            if terminal_type == "gnome":  
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command + '; exec bash'])
            elif terminal_type == "konsole":
                subprocess.Popen(['konsole', '--hold', '-e', command])
            elif terminal_type == "xfce4":
                subprocess.Popen(['xfce4-terminal', '--hold', '-e', command])
            else:
                subprocess.Popen(['bash', command])
        elif selected_version == "Python":
            command = f"sudo python3 pppwn/pppwn.py --interface={interface_var.get()} --fw={firmware_to_use} --stage1=pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2=pppwn/bins/{bin_selection}/stage2/stage2.bin"
            if terminal_type == "gnome":  
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command + '; exec bash'])
            elif terminal_type == "konsole":
                subprocess.Popen(['konsole', '--hold', '-e', command])
            elif terminal_type == "xfce4":
                subprocess.Popen(['xfce4-terminal', '--hold', '-e', command])
            else:
                subprocess.Popen(['bash', command])

    elif platform.system() == "Darwin": # macOS command
        os.chdir(os.path.dirname(sys.executable)) # fix path (thanks macOS!)
        if selected_version == "C++":
            command = f"./pppwn/pppwn --interface {interface_var.get()} --fw {firmware_to_use} --stage1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2 pppwn/bins/{bin_selection}/stage2/stage2.bin --spray-num {spray} --pin-num {pin} --corrupt-num {corrupt} --ipv6 fe80::{use_ipv6_str} {doNoWaitPadi} --auto-retry"
        elif selected_version == "Rust":
            command = f"./pppwn/yapppwn --interface={interface_var.get()} --fw={firmware_to_use} --stage-1 pppwn/bins/{bin_selection}/stage1/stage1.bin --stage-2 pppwn/bins/{bin_selection}/stage2/stage2.bin -r 100"
        elif selected_version == "Python":
            result = subprocess.run(["which", "python3"], capture_output=True, text=True)   # get python3 executable and ask it to strip for us
            pypath = result.stdout.strip() + " "
            command = pypath + f"pppwn/pppwn.py --interface={interface_var.get()} --fw={firmware_to_use} --stage1=pppwn/bins/{bin_selection}/stage1/stage1.bin --stage2=pppwn/bins/{bin_selection}/stage2/stage2.bin"
        command = f"sudo " + command
        os.system(command)

# Open Network Connections command idk just if someone wants it :/
def net_command():
    command = f"ncpa.cpl"
    subprocess.Popen('ncpa.cpl', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    print(command)

# Open CMD ipconfig just cuz
def ip_command():
    command = f"ipconfig"
    subprocess.call(["start", "cmd", "/k", command], shell=True)
    print(command)

# Theme doggle
def toggle_theme():
    if theme_var.get() == "Dark":
        theme_var.set("Light")
    else:
        theme_var.set("Dark")
    apply_theme()

# Applies theme
def apply_theme():
    theme = theme_var.get()
    
    bg_color = "#2E2E2E" if theme == "Dark" else "#FFFFFF"
    fg_color = "#FFFFFF" if theme == "Dark" else "#000000"
    button_bg = "#4B4B4B" if theme == "Dark" else "#E0E0E0"

    root.configure(bg=bg_color)
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=button_bg, foreground=fg_color)
    style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
    save_user_choices()

# Builds the GUI window 
root = tk.Tk()
root.bind("<Configure>", lambda event: save_user_choices()) 

# Set window size and title based on OS
if platform.system() == "Windows":
    root.geometry('410x530')
    root.title("PPPwn Tinker")
elif platform.system() == "Linux":
    root.geometry('470x530')
    root.title("PPPwn Tinker")
elif platform.system() == "Darwin": 
    root.geometry('470x545')
    root.title("PPPwn Tinker")

root.configure(bg="#2E2E2E")

# Icon for the GUI window
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgs", "icon.ico")
if os.path.exists(icon_path):
    if sys.platform.startswith("win"):  
        root.iconbitmap(icon_path)
    else: 
        icon_path_png = icon_path.replace(".ico", ".png")
        if os.path.exists(icon_path_png):
            img = PhotoImage(file=icon_path_png)
            root.iconphoto(False, img)

# Background image for the GUI window
if os.path.exists("imgs/background.png"):
    background_image = tk.PhotoImage(file="imgs/background.png")
    root.background_image = background_image  
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#2E2E2E")
style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
style.configure("TButton", background="#4B4B4B", foreground="#FFFFFF")
theme_var = tk.StringVar(value="Dark")

# Interface Selection Windows loaded if on Windows
if platform.system() == "Windows":
    interface_dict = get_network_interfaces_unified()
    interfaces = list(interface_dict.keys())
    interface_text = tk.StringVar(root)
    interface_label = ttk.Label(root, text="Select Interface:")
    interface_label.pack()
    interface_dropdown = ttk.Combobox(root, values=interfaces, textvariable=interface_text, state="readonly", width=50)
    interface_dropdown.bind("<<ComboboxSelected>>", on_select)
    interface_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

elif platform.system() == "Linux": # Finally actually fixed
    interfaces = get_network_interfaces_unified()
    interface_dict = {iface: iface for iface in interfaces}  # Convert to dictionary
    interface_var = tk.StringVar()
    interface_label = ttk.Label(root, text="Select Interface:")
    interface_label.pack()
    interface_dropdown = ttk.Combobox(root, textvariable=interface_var, values=interfaces, state="readonly")
    interface_dropdown.bind("<<ComboboxSelected>>", update_dropdown)
    interface_dropdown.pack(pady=(0, 5))  # Added padding

elif platform.system() == "Darwin": # Finally actually fixed
    interface_dict = get_network_interfaces_unified()
    interface_var = tk.StringVar()
    interface_label = ttk.Label(root, text="Select Interface:")
    interface_label.pack()
    interfaces = get_network_interfaces_unified() 
    interface_dropdown = ttk.Combobox(root, textvariable=interface_var, values=interfaces, state="readonly")
    interface_dropdown.bind("<<ComboboxSelected>>", update_dropdown)
    interface_dropdown.pack(pady=(0, 5))  # Added padding for better spacing
       
# Firmware Selection
firmwaresList = ["1100", "1071", "1070", "1050", "1001", "1000", "960", "951", "950", "904", "903", "900", "852", "850", "803", "801", "800", "755", "751", "750", "702", "700"]
sel_fw_label = ttk.Label(root, text="Select Firmware:")
sel_fw_label.pack() 
fw_select_as_text = tk.StringVar(root)
fw_select_as_text.set(firmwaresList[0])  # Default selection
fw_dropdown = ttk.Combobox(root, textvariable=fw_select_as_text, values=firmwaresList, state="readonly", width=10)
fw_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

# Version Selection
versionsList = ["C++", "Rust", "Python"]
version_as_text = tk.StringVar(root)
version_as_text.set(versionsList[0])  # Default selection
version_label = ttk.Label(root, text="Select PPPwn Version")
version_label.pack() 
version_dropdown = ttk.Combobox(root, textvariable=version_as_text, values=versionsList, state="readonly", width=8)
version_dropdown.pack(pady=(0, 5))  # Added padding for better spacing

# Corrupt Num Setting
corruptLabel = ttk.Label(root, text="Corrupt Num (Default 0x1)(Default will be used if blank)")
corruptLabel.pack()  
corrupt_num = tk.Entry(root)
corrupt_num.pack(pady=(0, 5))  # Added padding for better spacing

# Pin Setting 
pinLabel = ttk.Label(root, text="Pin Num (Default 0x1000)(Default will be used if blank)")
pinLabel.pack()  
pin_num = tk.Entry(root)
pin_num.pack(pady=(0, 5))  # Added padding for better spacing

# Spray Setting 
sprayLabel = ttk.Label(root, text="Spray Num (Default 0x1000)(Default will be used if blank)")
sprayLabel.pack() 
spray_num = tk.Entry(root)
spray_num.pack(pady=(0, 5))  # Added padding for better spacing

# Custom IPV6
ipv6Label = ttk.Label(root, text="Custom ipv6 (Default 9f9f:41ff:9f9f:41ff)(Default will be used if blank)")
ipv6Label.pack() 
cipv6 = tk.Entry(root)
cipv6.pack(pady=(0, 5))  # Added padding for better spacing

# No wait for PADI
tick_padi = tk.IntVar()
tickbox = ttk.Checkbutton(root, text="Skip extra PADI", variable=tick_padi)
tickbox.pack(pady=(5, 0))  # Added padding for better spacing

# Run PPPwn and save user choices for next startup
run_button = ttk.Button(root, text="Run PPPwn", command=lambda: [run_command(), save_user_choices()])
run_button.pack(pady=(10, 10))  # Added padding for better spacing

# If Windows is the current OS allows for some additional options in the GUI
if platform.system() == "Windows":
    # Create a frame to hold the buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=(0, 10))  # Added padding for better spacing

    # Open Network Connections 
    net_button = ttk.Button(button_frame, text="Open Network Settings", command=net_command)
    net_button.pack(side=tk.LEFT, padx=(0, 10))  # Added padding for better spacing

    # Open ipconfig 
    ip_button = ttk.Button(button_frame, text="Show current IP info", command=ip_command)
    ip_button.pack(side=tk.LEFT)  # Added padding for better spacing

# Light and dark theme toggle
toggle_button = ttk.Button(root, text="Light/Dark Theme", command=toggle_theme)
toggle_button.pack(pady=(10, 10))  # Added padding for better spacing

# Frame for settings buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=(10, 10))

# Clear user settings
clear_button = ttk.Button(button_frame, text="Clear PPPwn Settings", command=clear_pppwn_settings)
clear_button.pack(side=tk.LEFT, padx=(0, 10))  # Added padding for better spacing

# Clear user settings
clear_button = ttk.Button(button_frame, text="Clear Size Settings", command=clear_size_settings)
clear_button.pack(side=tk.LEFT, padx=(10, 0))  # Added padding for better spacing

# Clear all settings
clear_button = ttk.Button(button_frame, text="Clear All Settings", command=clear_all_settings)
clear_button.pack(side=tk.LEFT, padx=(10, 0))  # Added padding for better spacing

# Load user choices on start
load_user_choices()

# Save user choices on exit
root.protocol("WM_DELETE_WINDOW", lambda: [save_user_choices(), root.destroy()])

root.mainloop()