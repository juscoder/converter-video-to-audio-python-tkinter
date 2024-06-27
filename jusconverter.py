import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os
import sys
import threading

def convert_video_to_audio(video_path, output_audio_path, format, update_status):
    try:
        update_status("Iniciando la conversión...")
        with VideoFileClip(video_path) as video_clip:
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(output_audio_path, codec='mp3' if format == 'MP3' else 'pcm_s16le', logger=None)
        update_status("Conversión completada con éxito.")
    except Exception as e:
        update_status(f"Error al convertir el video: {str(e)}")

def browse_video():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        video_path.set(file_path)

def browse_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_directory.set(directory)

def start_conversion():
    video = video_path.get()
    directory = output_directory.get()
    filename = output_filename.get()
    format = format_var.get()

    if not video or not directory or not filename:
        messagebox.showerror("Error", "Por favor completa todos los campos.")
        return

    output = os.path.join(directory, f"{filename}.{format.lower()}")

    status_label.config(text="Iniciando la conversión...")
    conversion_thread = threading.Thread(target=run_conversion, args=(video, output, format))
    conversion_thread.start()
    monitor_conversion(conversion_thread)

def run_conversion(video, output, format):
    try:
        convert_video_to_audio(video, output, format, update_status)
    except Exception as e:
        update_status(f"Hubo un error durante la conversión: {str(e)}")
    finally:
        reset_inputs()
        root.update_idletasks()

def reset_inputs():
    video_path.set("")
    output_directory.set("")
    output_filename.set("")

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()

def monitor_conversion(thread):
    if thread.is_alive():
        root.after(100, monitor_conversion, thread)
    else:
        update_status("Conversión finalizada.")               

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para desarrollo y para PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Configuración de la interfaz
root = tk.Tk()
root.title("JusConversor de Video a Audio")
root.iconbitmap(resource_path("img/jusconverter.ico"))

video_path = tk.StringVar()
output_directory = tk.StringVar()
output_filename = tk.StringVar()
format_var = tk.StringVar(value='MP3')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Selecciona el archivo de video MP4:").grid(row=0, column=0, sticky=tk.W)
tk.Entry(frame, textvariable=video_path, width=50).grid(row=0, column=1)
tk.Button(frame, text="Buscar", command=browse_video).grid(row=0, column=2)

tk.Label(frame, text="Selecciona el formato de audio:").grid(row=1, column=0, sticky=tk.W)
tk.Radiobutton(frame, text="MP3", variable=format_var, value='MP3').grid(row=1, column=1, sticky=tk.W)
tk.Radiobutton(frame, text="WAV", variable=format_var, value='WAV').grid(row=1, column=1)

tk.Label(frame, text="Selecciona la ubicación para guardar el archivo de audio:").grid(row=2, column=0, sticky=tk.W)
tk.Entry(frame, textvariable=output_directory, width=50).grid(row=2, column=1)
tk.Button(frame, text="Buscar", command=browse_output_directory).grid(row=2, column=2)

tk.Label(frame, text="Nombre del archivo de audio:").grid(row=3, column=0, sticky=tk.W)
tk.Entry(frame, textvariable=output_filename, width=50).grid(row=3, column=1)

tk.Button(frame, text="Iniciar la conversión", command=start_conversion).grid(row=4, column=0, columnspan=3, pady=10)

status_label = tk.Label(frame, text="")
status_label.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
