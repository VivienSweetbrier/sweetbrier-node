import os
import sys
import PyInstaller.__main__

def build():
    # Make sure we are in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("[*] Initiating GUI-RELIQUARY-v2 PyInstaller Build Sequence...")
    
    PyInstaller.__main__.run([
        'main.py',
        '--name=GUI-RELIQUARY-v2',
        '--onefile',
        '--windowed',  # Hides the console window since it's a GUI (though it's a web app, we might want console for uvicorn output, so let's keep console for now if we want to see startup logs. I'll remove windowed)
        '--add-data=static;static',
        '--clean'
    ])
    
    print("[*] Build complete. Artifact 'GUI-RELIQUARY-v2.exe' is located in the 'dist' directory.")

if __name__ == "__main__":
    # Remove windowed argument to allow uvicorn console to appear.
    # We could also use --noconsole and open a browser window automatically, but a terminal + browser workflow works.
    # Actually, let's open the browser automatically in main.py if we want a true desktop app feel.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("[*] Initiating GUI-RELIQUARY-v2 PyInstaller Build Sequence...")
    
    PyInstaller.__main__.run([
        'main.py',
        '--name=GUI-RELIQUARY-v2',
        '--onefile',
        '--add-data=static;static',
        r'--add-data=C:\Users\Vivian\AppData\Roaming\Python\Python314\site-packages\llama_cpp\lib;llama_cpp\lib',
        '--collect-all=llama_cpp',
        '--clean'
    ])
    
    print("[*] Build complete. Artifact 'GUI-RELIQUARY-v2.exe' is located in the 'dist' directory.")
