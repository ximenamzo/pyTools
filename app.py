import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import os
import re

CONFIG_FILE = 'config.txt'

def cargar_ruta():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return file.read().strip()
    return ""

def guardar_ruta(ruta):
    with open(CONFIG_FILE, 'w') as file:
        file.write(ruta)

def descargar_audio(url, output_path, status_label):
    try:
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        # Obtener el título del video y limpiar caracteres no válidos para el nombre del archivo
        video_title = yt.title
        video_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

        # Descargar el archivo de audio
        output_file = video.download(output_path=output_path, filename=video_title + '.mp4')

        status_label.config(text="Descarga exitosa", fg="green")
    except Exception as e:
        if 'pytube' in str(e):
            status_label.config(text="No hay conexión a internet", fg="red")
        else:
            status_label.config(text="No se pudo descargar", fg="red")
        print(e)

def seleccionar_ruta(label):
    path = filedialog.askdirectory()
    if path:
        label.config(text=path)
        guardar_ruta(path)

# Configuración de la interfaz
root = tk.Tk()
root.title("Descargador de Audio de YouTube")

# Input para la URL del video de YouTube
tk.Label(root, text="URL del video de YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Ruta inicial
ruta_inicial = cargar_ruta()
ruta_label = tk.Label(root, text=ruta_inicial if ruta_inicial else "Selecciona la ruta para guardar el archivo")
ruta_label.pack(pady=5)

# Botón para elegir la ruta de guardado
tk.Button(root, text="Elegir ruta", command=lambda: seleccionar_ruta(ruta_label)).pack(pady=5)

# Botón para descargar el audio
status_label = tk.Label(root, text="", fg="red")
status_label.pack(pady=5)
tk.Button(root, text="Descargar", command=lambda: descargar_audio(url_entry.get(), ruta_label.cget("text"), status_label)).pack(pady=20)

# Mensajes de estado
status_label = tk.Label(root, text="", fg="red")
status_label.pack(pady=5)

root.mainloop()
