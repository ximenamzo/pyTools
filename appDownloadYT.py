import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import os
import re
import threading

CONFIG_FILE = 'config.txt'


def cargar_ruta():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return file.read().strip()
    return ""


def guardar_ruta(ruta):
    with open(CONFIG_FILE, 'w') as file:
        file.write(ruta)


def descargar_audio(url, output_path, status_label, descargar_audio_btn, descargar_video_btn):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
        audio_file_temp = video.download(output_path=output_path, filename=video_title + '_audio.mp4')
        new_file = os.path.splitext(audio_file_temp)[0] + '.mp3'
        os.system(f'ffmpeg -i "{audio_file_temp}" "{new_file}"')
        os.remove(audio_file_temp)
        status_label.config(text="Audio descargado con éxito", fg="green")
    except Exception as e:
        if 'pytube' in str(e):
            status_label.config(text="No hay conexión a internet", fg="red")
        else:
            status_label.config(text="No se pudo descargar el audio", fg="red")
        print(e)
    finally:
        descargar_audio_btn.config(state=tk.NORMAL)
        descargar_video_btn.config(state=tk.NORMAL)


def descargar_video(url, output_path, status_label, descargar_audio_btn, descargar_video_btn):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
        output_file = stream.download(output_path=output_path, filename=video_title + '_video.mp4')
        status_label.config(text="Video descargado con éxito", fg="green")
    except Exception as e:
        if 'pytube' in str(e):
            status_label.config(text="No hay conexión a internet", fg="red")
        else:
            status_label.config(text="No se pudo descargar el video", fg="red")
        print(e)
    finally:
        descargar_audio_btn.config(state=tk.NORMAL)
        descargar_video_btn.config(state=tk.NORMAL)


def seleccionar_ruta(label):
    path = filedialog.askdirectory()
    if path:
        label.config(text=path)
        guardar_ruta(path)


def on_enter(e, widget, bg_color):
    widget['background'] = bg_color


def on_leave(e, widget, bg_color):
    widget['background'] = bg_color


def iniciar_descarga_video(url, output_path, status_label, descargar_audio_btn, descargar_video_btn):
    threading.Thread(target=descargar_video, args=(url, output_path, status_label, descargar_audio_btn, descargar_video_btn)).start()
    status_label.config(text="Cargando...", fg="blue")
    descargar_audio_btn.config(state=tk.DISABLED)
    descargar_video_btn.config(state=tk.DISABLED)


def iniciar_descarga_audio(url, output_path, status_label, descargar_audio_btn, descargar_video_btn):
    threading.Thread(target=descargar_audio, args=(url, output_path, status_label, descargar_audio_btn, descargar_video_btn)).start()
    status_label.config(text="Cargando...", fg="blue")
    descargar_audio_btn.config(state=tk.DISABLED)
    descargar_video_btn.config(state=tk.DISABLED)


# Configuración de la interfaz
root = tk.Tk()
root.title("Descargador de YouTube")

# Obtener dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dimensiones de la ventana
window_width = screen_width // 2
window_height = screen_height // 2

# Posicionar la ventana en el centro de la pantalla
position_right = screen_width // 2 - window_width // 2
position_down = screen_height // 2 - window_height // 2
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_down}')

# Configurar fondo blanco y padding
root.config(bg='white')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
container = tk.Frame(root, bg='white', padx=window_width * 0.2, pady=window_height * 0.1)
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
ruta_label = tk.Label(container, text=ruta_inicial if ruta_inicial else "Selecciona la ruta para guardar el archivo",
                      bg='white', font=('Arial', 10))
ruta_label.pack(pady=5)

# Botón para elegir la ruta de guardado
elegir_ruta_btn = tk.Button(container, text="Elegir ruta", command=lambda: seleccionar_ruta(ruta_label), **button_style,
                            bg='lightblue', fg='black')
elegir_ruta_btn.pack(pady=5)
elegir_ruta_btn.bind("<Enter>", lambda e: on_enter(e, elegir_ruta_btn, 'lightcyan'))
elegir_ruta_btn.bind("<Leave>", lambda e: on_leave(e, elegir_ruta_btn, 'lightblue'))

# Frame para los botones de descarga
buttons_frame = tk.Frame(container, bg='white')
buttons_frame.pack(pady=20)

# Botón para descargar el video
descargar_video_btn = tk.Button(buttons_frame, text="Descargar video",
                                command=lambda: iniciar_descarga_video(url_entry.get(), ruta_label.cget("text"),
                                                                       status_label, descargar_audio_btn, descargar_video_btn), **button_style, bg='purple',
                                fg='white')
descargar_video_btn.pack(side='left', padx=10)
descargar_video_btn.bind("<Enter>", lambda e: on_enter(e, descargar_video_btn, 'violet'))
descargar_video_btn.bind("<Leave>", lambda e: on_leave(e, descargar_video_btn, 'purple'))

# Botón para descargar el audio
descargar_audio_btn = tk.Button(buttons_frame, text="Descargar audio",
                                command=lambda: iniciar_descarga_audio(url_entry.get(), ruta_label.cget("text"),
                                                                       status_label, descargar_audio_btn, descargar_video_btn), **button_style, bg='green',
                                fg='white')
descargar_audio_btn.pack(side='right', padx=10)
descargar_audio_btn.bind("<Enter>", lambda e: on_enter(e, descargar_audio_btn, 'lightgreen'))
descargar_audio_btn.bind("<Leave>", lambda e: on_leave(e, descargar_audio_btn, 'green'))

# Mensajes de estado
status_label = tk.Label(container, text="", fg="red", bg='white', font=('Arial', 12))
status_label.pack()

# Aplicar estilos adicionales
for widget in [url_entry, elegir_ruta_btn, descargar_video_btn, descargar_audio_btn]:
    widget.config(borderwidth=1, relief="solid")

url_entry.config(highlightbackground='gray', highlightcolor='gray', highlightthickness=1, bd=1, relief='solid')
url_entry.bind('<FocusIn>', lambda e: url_entry.config(highlightthickness=2))

elegir_ruta_btn.config(relief='solid', bd=0, highlightthickness=0)
elegir_ruta_btn.bind("<Enter>", lambda e: on_enter(e, elegir_ruta_btn, 'lightcyan'))
elegir_ruta_btn.bind("<Leave>", lambda e: on_leave(e, elegir_ruta_btn, 'lightblue'))

descargar_video_btn.config(relief='solid', bd=0, highlightthickness=0)
descargar_video_btn.bind("<Enter>", lambda e: on_enter(e, descargar_video_btn, 'violet'))
descargar_video_btn.bind("<Leave>", lambda e: on_leave(e, descargar_video_btn, 'purple'))

descargar_audio_btn.config(relief='solid', bd=0, highlightthickness=0)
descargar_audio_btn.bind("<Enter>", lambda e: on_enter(e, descargar_audio_btn, 'lightgreen'))
descargar_audio_btn.bind("<Leave>", lambda e: on_leave(e, descargar_audio_btn, 'green'))

# Bordes redondeados y sombra
url_entry.config(relief='solid', bd=2, highlightthickness=2)
url_entry.pack_configure(ipady=5)

for btn in [elegir_ruta_btn, descargar_video_btn, descargar_audio_btn]:
    btn.config(borderwidth=1, relief="solid", bd=2, highlightthickness=2)

root.mainloop()
