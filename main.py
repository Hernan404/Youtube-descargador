import tkinter
import customtkinter

from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        if video:
            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="")
            video.download()
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
    #print(percentage_of_compeletion)
    #progressBar.set(percentage_of_compeletion)
    #finishLabel.configure(percentage_of_compeletion)
    per = str(int(percentage_of_compeletion))
    pPercentaje.configure(text=per + '%')
    pPercentaje.update()

    progressBar.set(float(percentage_of_compeletion)/100)

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
download = customtkinter.CTkButton(app, text="Descargar", command=startDownload) 
download.pack(padx=10, pady=10)


# corro la app
app.mainloop()
