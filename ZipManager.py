import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class FolderMonitorHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        self.update_callback = update_callback

    def on_any_event(self, event):
        self.update_callback()

class FolderViewerApp:
    def __init__(self, root, folder_path, file_path):
        self.root = root
        self.folder_path = folder_path
        self.file_path = file_path

        self.root.title("Changes Panel")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text=file_path)
        self.label.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill=tk.BOTH, expand=1)

        self.button = tk.Button(root, text="Save All", command=self.button_clicked)
        self.button.pack()

        self.update_folder_contents()

        event_handler = FolderMonitorHandler(self.update_folder_contents)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.folder_path, recursive=False)
        self.observer_thread = threading.Thread(target=self.observer.start)
        self.observer_thread.start()

    def update_folder_contents(self):
        self.listbox.delete(0, tk.END)
        try:
            for item in os.listdir(self.folder_path):
                self.listbox.insert(tk.END, item)
        except FileNotFoundError:
            self.listbox.insert(tk.END, "Directory doesn't exist")

    def button_clicked(self):
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("ZipManager")
        self.dialog.geometry("300x100")
        self.dialog_label = tk.Label(self.dialog, text="Wait for compression")
        self.dialog_label.pack(expand=True)

        threading.Thread(target=self.compress_and_close).start()

    def compress_and_close(self):
        try:
            rezip(self.folder_path, self.file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Compression error: {e}")
        finally:
            self.observer.stop()
            self.observer.join()
            self.dialog.destroy()
            self.root.quit()

    def on_closing(self):
        self.observer.stop()
        self.observer.join()
        self.root.quit()

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
    temp_dir = ".\\ZipManagerTemp"
    file_path = select()
    
    try:
        if file_path:
            unzip(file_path, temp_dir)
            os.startfile(temp_dir)
            
            root = tk.Tk()
            app = FolderViewerApp(root, temp_dir, file_path)
            root.protocol("WM_DELETE_WINDOW", app.on_closing)
            root.mainloop()
            
        else:
            exit()
    except Exception as ex:
        messagebox.showerror("Error", ex)