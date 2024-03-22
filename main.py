import tkinter
import customtkinter

from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        video = ytObject.streams.get_highest_resolution()
        if video:
            video.download()
            print("Descarga Completada")
        else:
            print("no tiene resolucion adecuada")
    except RegexMatchError:
            print("enlace no es valido")
    except VideoUnavailable:
            print("video no disponible o enlace incorrecto")

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

# botton de descarga
download = customtkinter.CTkButton(app, text="Descargar", command=startDownload) 
download.pack(padx=10, pady=10)


# corro la app
app.mainloop()