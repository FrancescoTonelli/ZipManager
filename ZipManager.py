import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import subprocess

def select():
    root = tk.Tk()
    root.withdraw() 

    file_path = filedialog.askopenfilename(
        title="ZipManager",
        filetypes=[("File ZIP", "*.zip")]
    )

    return file_path

def open_up(file_path, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        zipfile.ZipFile(file_path, 'r').extractall(temp_dir)
    except:
        raise Exception("Not a .zip file")

if __name__ == "__main__":
    temp_dir = ".\\ZipManagerTemp\\"
    file_path = select()
    
    try:
        if file_path:
            open_up(file_path, temp_dir)
            os.startfile(temp_dir)  
            
        else:
            raise Exception("No file selected")
    except Exception as ex:
        messagebox.showerror("Error", ex)