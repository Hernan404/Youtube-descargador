import tkinter
import customtkinter

from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from moviepy.editor import VideoFileClip




def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        

        if download_choice.get() == "Video":
            video = ytObject.streams.get_highest_resolution()
            file_extension = video.mine_type.split("/")[-1]
            filename = video.default_filename
        else:
            video = ytObject.streams.filter(only_audio=True).first()
            file_extension = "mp3"
            filename = ytObject.title + ".mp3"

        if video:
            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="")
            video.download(filename="temp." + file_extension)
            if download_choice.get() == "MP3":
                convert_to_mp3("temp." + file_extension, filename)
            else: 
                #renombro archivo temporal
                import os 
                os.rename("temp." + file_extension, filename)
            print("Descarga Completada")
            finishLabel.configure(text="Descargado!")
            #progressBar.set(100)
        else:
            print("no tiene resolucion adecuada")
            finishLabel.configure(text="No tiene resolucion adecuada", text_color="red")  

                                
    except RegexMatchError:
            print("enlace no es valido")
            finishLabel.configure(text="Error al descargar, Link invalido", text_color="red")
    except VideoUnavailable:
            print("video no disponible o enlace incorrecto")
            finishLabel.configure(text="video no disponible o enlace incorrecto", text_color="red")
        
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize 
    bytes_download = total_size - bytes_remaining
    percentage_of_compeletion = int(bytes_download/total_size * 100)

    per = str(int(percentage_of_compeletion))
    pPercentaje.configure(text=per + '%')
    pPercentaje.update()

    progressBar.set(float(percentage_of_compeletion)/100)

def convert_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)
    video.close()


# configuracion 
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# frame de la aplicacion
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Descargador de Youtube")


# añado la interfaz 
title = customtkinter.CTkLabel(app, text="Inserte link de YouTube")
title.pack(padx=10, pady=10) # tamaño

# input para el link 
url_var = tkinter.StringVar() # hago una variable url var para tener la ultima info de que es lo que hay en el link y usarlo en cualquier lado
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# termino la descarga 
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()


#barra de progresso
pPercentaje = customtkinter.CTkLabel(app, text="0%")
pPercentaje.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# botton de descarga
download_choice = tkinter.StringVar(app)
download_choice.set("Video MP4")

download_menu = tkinter.OptionMenu(app, download_choice, "Video MP4" , "Audio MP3" )
download_menu.pack(padx=10, pady=10)

download = customtkinter.CTkButton(app, text="Descargar", command=startDownload) 
download.pack(padx=10, pady=10)


# corro la app
app.mainloop()
