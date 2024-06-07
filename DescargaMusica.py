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


def on_enter(e, widget, bg_color):
    widget['background'] = bg_color


def on_leave(e, widget, bg_color):
    widget['background'] = bg_color


# Configuración de la interfaz
root = tk.Tk()
root.title("Descargador de Audio de YouTube")

# Obtener dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dimensiones de la ventana
window_width = screen_width // 3
window_height = screen_height // 3

# Posicionar la ventana en el centro de la pantalla
position_right = screen_width // 2 - window_width // 2
position_down = screen_height // 2 - window_height // 2
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_down}')

# Configurar fondo blanco y padding
root.config(bg='white')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
container = tk.Frame(root, bg='white', padx=window_width*0.2, pady=window_height*0.1)
container.grid(sticky='nsew')

# Estilos comunes
entry_style = {'font': ('Arial', 12), 'bg': 'white', 'bd': 2, 'relief': 'solid'}
button_style = {'font': ('Arial', 12), 'bd': 0, 'highlightthickness': 0}

# Input para la URL del video de YouTube
tk.Label(container, text="LINK del video de YouTube:", bg='white', font=('Arial', 12)).pack(pady=5)
url_entry = tk.Entry(container, width=50, **entry_style)
url_entry.pack(pady=5)
url_entry.config(highlightbackground='gray', highlightcolor='gray', highlightthickness=1, bd=1, relief='solid')
url_entry.bind('<FocusIn>', lambda e: url_entry.config(highlightthickness=2))

# Espacio entre el input de la URL y el label de la ruta
tk.Label(container, text="", bg='white').pack(pady=2)

# Ruta inicial
ruta_inicial = cargar_ruta()
ruta_label = tk.Label(container, text=ruta_inicial if ruta_inicial else "Selecciona la ruta para guardar el archivo", bg='white', font=('Arial', 10))
ruta_label.pack(pady=5)

# Botón para elegir la ruta de guardado
elegir_ruta_btn = tk.Button(container, text="Elegir ruta", command=lambda: seleccionar_ruta(ruta_label), **button_style, bg='lightblue', fg='black')
elegir_ruta_btn.pack(pady=5)
elegir_ruta_btn.bind("<Enter>", lambda e: on_enter(e, elegir_ruta_btn, 'lightcyan'))
elegir_ruta_btn.bind("<Leave>", lambda e: on_leave(e, elegir_ruta_btn, 'lightblue'))

# Botón para descargar el audio
descargar_btn = tk.Button(container, text="Descargar", command=lambda: descargar_audio(url_entry.get(), ruta_label.cget("text"), status_label), **button_style, bg='lightgreen', fg='black')
descargar_btn.pack(pady=20)
descargar_btn.bind("<Enter>", lambda e: on_enter(e, descargar_btn, 'palegreen'))
descargar_btn.bind("<Leave>", lambda e: on_leave(e, descargar_btn, 'lightgreen'))

# Mensajes de estado
status_label = tk.Label(container, text="", fg="red", bg='white', font=('Arial', 12))
status_label.pack(pady=5)

# Aplicar estilos adicionales
for widget in [url_entry, elegir_ruta_btn, descargar_btn]:
    widget.config(borderwidth=1, relief="solid")

url_entry.config(highlightbackground='gray', highlightcolor='gray', highlightthickness=1, bd=1, relief='solid')
url_entry.bind('<FocusIn>', lambda e: url_entry.config(highlightthickness=2))

elegir_ruta_btn.config(relief='solid', bd=0, highlightthickness=0)
elegir_ruta_btn.bind("<Enter>", lambda e: on_enter(e, elegir_ruta_btn, 'lightcyan'))
elegir_ruta_btn.bind("<Leave>", lambda e: on_leave(e, elegir_ruta_btn, 'lightblue'))

descargar_btn.config(relief='solid', bd=0, highlightthickness=0)
descargar_btn.bind("<Enter>", lambda e: on_enter(e, descargar_btn, 'palegreen'))
descargar_btn.bind("<Leave>", lambda e: on_leave(e, descargar_btn, 'lightgreen'))

# Bordes redondeados y sombra
url_entry.config(relief='solid', bd=2, highlightthickness=2)
url_entry.pack_configure(ipady=5)

for btn in [elegir_ruta_btn, descargar_btn]:
    btn.config(borderwidth=1, relief="solid", bd=2, highlightthickness=2)

root.mainloop()
