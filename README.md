# Keen2Mi-Routes 🚀

A utility for automatically importing IP route lists from Keenetic/Windows (`.bat`) format into Xiaomi routers (MiWiFi/LuCI firmware).

## 📖 Project Description
Keenetic routers feature a convenient built-in tool for importing routing tables from files. In the Xiaomi (MiWiFi) interface, this feature is missing—each address must be entered manually.

Since there are already numerous ready-made route databases in `.bat` format (prepared for Keenetic) available online, this script allows you to reuse them. The program parses the files, converts the data, and "injects" them into your Xiaomi router via API.

### How it works:
1. **Parsing**: The script searches for `route add <IP> mask <MASK>` strings in text files.
2. **Conversion**: It converts subnet masks into CIDR format (e.g., from `255.255.255.255` to `/32`), which Xiaomi understands.
3. **Automation**: The script sends POST requests to the router's `smartvpn_url` endpoint, mimicking manual entry via the web interface.
4. **Security**: No tokens are stored in the code—everything is entered dynamically at runtime.

---

## 💾 Downloads (Releases)
If you do not want to install Python, pre-compiled executables are available in the **[Releases](https://github.com/MarkinF1/Keen2Mi-Routes/releases)** section for:
* 🪟 **Windows** (`.exe`)
* 🐧 **Linux** (binary file)

---

## 🛠 Requirements for Running from Source
To run the script, you need **Python 3.x** and the `requests` library.

### Installing dependencies:
```bash
pip install -r requirements.txt
```

---

### 🚀 Usage Instructions

1. Get the STOK:
   * Log in to your router's admin panel in a browser.
   * Copy the value following ;stok= from the address bar. (Example: 945654750a6503c0c3a1n499b7200j14)

2. Run the program:
```bash
python main.py
```

Or run the release version specific to your OS.

3. Enter the data:

    Router IP: Usually 192.168.1.1.

    STOK: Paste the copied key.

    Path: You can specify the path to a specific file or an entire folder (the script will automatically find all files inside, including nested subfolders).

⚠️ Important Note
The stok token is tied to your current session. If you log out of the admin panel in your browser or if too much time passes, the token will become invalid. If this happens, simply refresh the page in your browser and get a new token.
