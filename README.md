# PPPwn-Tinker-GUI
PPPwn-Tkinter-GUI was crafted with the goal of extending the functionality of the current PPPwn solutions. By altering the way in which the exploit is deployed and run, one can increase reliability to nearly 100%. This is often console-dependent, but it's better to experiment than not.

At present, PPPwn-Tkinter-GUI was made with Windows in mind. Hopefully this will be built upon soon. As it stands, there aren't any options to "save" a configuration, but this will also hopefully be added soon.

This tool is open-source and provided as-is. Under the hood it utilizes new functionality added to PPPwn_cpp by nn9dev with the help of Borris_ta (and is also open source!) 

Please be sure to read the instructions carefully, and happy tinkering!

# Installing Dependencies for C++ version
1. Download and install [Npcap1.79](https://npcap.com/#download)    
# Installing Dependencies For Python version
1. Download and install [Python](https://www.python.org/downloads/)
Make sure to add it to path and install as admin           
![-](python.PNG)         
2. Then run the following commands in a CMD window        
```   
python -m ensurepip --default-pip
```    
```
pip install scapy
```    


# How to use the new options Corrupt Num, Pin Num and Spray Num
# Corrupt Num
1. Corrupt Num increases the is the amount of overflow packets sent to the PS4. Enter in hex OR decimal. (Default: 0x1 or 1)
The reccomended DECIMAL values are 
# Pin Num 
1. No information about it untested if it helps but is available if you'd like to try. Enter in hex OR decimal. (Default: 0x1000 or 4096)
# Spray num
When spray is higher the scan range is larger. (Default: 0x1000 or 4096)(pending better description)

# PPPwn-Tinker C++ Instructions          
1. Choose your ethernet interface      
To find it you can look in        
Settings>Network & Internet>**Ethernet** on the left menu>Then Click on the connection name scroll down and fine the Description      
2. Select the firmware version your PS4 is on        
3. PPPwn version C++ is the default option       
4. Usually not using the old IPV6 version is reccomended but if your console experienses crashes with no progress past Stage 2 tick it to use the old IPV6       
5.    
6.    
7.    
8.   
9.    
      
   
# PPPwn-Tinker Python Instructions         
1. Choose your ethernet interface          
To find it you can look in         
Settings>Network & Internet>**Ethernet** on the left menu>Then Click on the connection name scroll down and fine the Description      
2. Select the firmware version your PS4 is on     
3. To select the Python version click on the dropdown menu and choose **Python**    
4. Python does not have the option to use the old IPV6.      
5. Python does not have support for tweaking the Num values left blank or with writing in it will not result in errors or additions to the command.       


# Troubleshooting 
1. If the script gets stuck at [*] Waiting for interface to be ready... restart the exploit process
2. If the script gets stuck at [+] Pinning to CPU XX...done restart the exploit process
3. If the script is stuck on 
[+] Scanning for corrupted object...found fe80::0fdf:4141:4141:4141
[+] STAGE 2: KASLR defeat
[*] Defeating KASLR...
and your console crashes try changing to the old IPV6
4. If the script is stuck on [*] Waiting for IPCP configure ACK... and your console crashes try changing to the old IPV6
5. If the script gets stuck on any of the following 
[*] Sending LCP configure ACK...
[*] Sending LCP configure request...
[*] Waiting for LCP configure ACK...
[*] Waiting for IPCP configure request...
[*] Sending IPCP configure NAK...
[*] Waiting for IPCP configure request...
[*] Sending IPCP configure ACK...
[*] Sending IPCP configure request...
[*] Waiting for IPCP configure ACK...
[*] Waiting for interface to be ready...
 Restart the exploit process

# Credits 
[TheOfficialFloW for PPPwn](https://github.com/TheOfficialFloW/PPPwn)
[xfangfang for C++ rewrite](https://github.com/xfangfang/PPPwn_cpp?tab=readme-ov-file)
[nn9dev for the C++ changes](https://github.com/nn9dev/PPPwn_cpp/releases/tag/1.1-b1)
[Borris-ta for his help](https://github.com/Borris-ta)
Thank you to Beta testers of the GUI Sausig, Rust, and nn9dev. 