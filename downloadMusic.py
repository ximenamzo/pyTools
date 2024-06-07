from pytube import YouTube
from pydub import AudioSegment
import os
import re


def descargar_audio_mp3(url, output_path):
    # Descargar el video de YouTube
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

    # Obtener el título del video y limpiar caracteres no válidos para el nombre del archivo
    video_title = yt.title
    video_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

    # Descargar el archivo de audio
    output_file = video.download(output_path=output_path, filename=video_title + '.mp4')

    # Convertir el audio a MP3
    base, ext = os.path.splitext(output_file)
    mp3_file = base + '.mp3'
    audio = AudioSegment.from_file(output_file)
    audio.export(mp3_file, format='mp3')

    # Eliminar el archivo original
    os.remove(output_file)

    print(f'Audio descargado y convertido a MP3: {mp3_file}')


# Ejemplo de uso
url = 'https://www.youtube.com/watch?v=649zhcMQajo'
output_path = r"C:\Users\ximen\Music\descargasPython"  # Usa el prefijo 'r' para cadenas sin procesar
# Descargar audio en MP3
descargar_audio_mp3(url, output_path)
