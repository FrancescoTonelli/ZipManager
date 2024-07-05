import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil

def select():
    root = tk.Tk()
    root.withdraw() 

    file_path = filedialog.askopenfilename(
        title="ZipManager",
        filetypes=[("File ZIP", "*.zip")]
    )

    return file_path

def unzip(file_path, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        zipfile.ZipFile(file_path, 'r').extractall(temp_dir)
    except:
        raise Exception("Not a .zip file")

def rezip(folder_path, replace_path):
    zip_path=r'.'
    if not os.path.isdir(folder_path):
        raise ValueError("La cartella specificata non esiste o non è valida.")
    
    # Determina il nome del file zip basato sulla cartella di origine
    zip_filename = os.path.basename(folder_path) + '.zip'
    zip_path = os.path.join(zip_path, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    if os.path.exists(replace_path):
        os.remove(replace_path)
    os.rename(zip_path, replace_path)
    shutil.rmtree(folder_path)

if __name__ == "__main__":
    temp_dir = ".\\ZipManagerTemp\\"
    file_path = select()
    
    try:
        if file_path:
            unzip(file_path, temp_dir)
            input("Invio per procedere")
            rezip(temp_dir, file_path)
            
        else:
            raise Exception("No file selected")
    except Exception as ex:
        messagebox.showerror("Error", ex)