import os
from pytube import YouTube

def download_video(youtube_url, output_path):
    yt = YouTube(youtube_url)
    stream = yt.streams.get_highest_resolution()
    video_file = stream.download(output_path=output_path)
    print(f'Video descargado: {video_file}')
    return video_file

def download_audio(youtube_url, output_path):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_file = stream.download(output_path=output_path, filename='audio.mp4')

    # Convertir el archivo de audio al formato deseado
    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'
    os.system(f'ffmpeg -i "{audio_file}" "{new_file}"')
    os.remove(audio_file)
    print(f'Audio descargado: {new_file}')
    return new_file

# Ejemplo de uso
youtube_url = 'https://www.youtube.com/watch?v=q9zbBmmO7JM'  # Reemplaza con la URL del video de YouTube
output_path = r'C:\Users\ximen\Music\descargasPython'  # Reemplaza con la ruta donde quieres guardar los archivos

# Descargar video
download_video(youtube_url, output_path)

# Descargar audio
download_audio(youtube_url, output_path)
