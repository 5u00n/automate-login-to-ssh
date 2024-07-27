Steps to Install nmap on Windows
1. Download nmap:
    - Go to the [nmap download page](https://nmap.org/download.html).
    - Download the installer.

2. Install nmap:
   - Run the downloaded installer and follow the installation instructions.
3. Add nmap to System PATH:
   - Open the Start Menu, search for "Environment Variables," and select "Edit the system environment variables."
   - In the System Properties window, click on the "Environment Variables" button.
   - In the Environment Variables window, find the "Path" variable in the "System variables" section and select it. Click "Edit."
   - Click "New" and add the path to the nmap installation directory (e.g., C:\Program Files (x86)\Nmap).
   - Click "OK" to close all windows.
4. Verify Installation:
   - Open a new Command Prompt window and type nmap. You should see the nmap help output, indicating that nmap is installed and accessible.


Example Command to Verify nmap Installation
```
    nmap --version
```

