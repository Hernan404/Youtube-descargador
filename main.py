import tkinter
import customtkinter
import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from moviepy.editor import AudioFileClip
from tkinter import filedialog

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        
        download_folder = folder_path_var.get()  # Get the selected download folder

        progressBar.set(0)

        if download_folder:
            if download_choice.get() == "Video MP4":
                video = ytObject.streams.get_highest_resolution()
                file_extension = video.mime_type.split("/")[-1]
                filename = os.path.join(download_folder, video.default_filename)
            else:
                video = ytObject.streams.filter(only_audio=True).first()
                file_extension = "mp3"
                filename = os.path.join(download_folder, ytObject.title + ".mp3")
                temp_filename = os.path.join(download_folder, "temp." + file_extension)
                filename = os.path.join(download_folder, ytObject.title + "mp3.")
           
            if video:
                title_label.configure(text=ytObject.title, text_color="white")
                finishLabel.configure(text="")
                
                video.download(output_path=download_folder, filename=(video.default_filename.replace(".mp4", "") + "." + file_extension))

                if download_choice.get() == "Audio MP3":
                    if os.path.exists(temp_filename):
                        if convert_to_mp3(temp_filename, filename):
                            os.remove(temp_filename)
                            finishLabel.configure(text="Descargado!")
                            download.configure(text="Descargar")
                else:
                    video.download(output_path=download_folder, filename=video.default_filename)
                    finishLabel.configure(text="Descargado!")
                    download.configure(text="Descargar")
                    
                pPercentaje.configure(text="0%")
                progressBar.set(0)

            else:
                print("no tiene resolucion adecuada")
                finishLabel.configure(text="No tiene resolucion adecuada", text_color="red")  
        else:
            print("Seleccione una carpeta de descarga")
            finishLabel.configure(text="Seleccione una carpeta de descarga", text_color="red")

    except RegexMatchError:
        print("enlace no es valido")
        finishLabel.configure(text="Error al descargar, Link invalido", text_color="red")
    except VideoUnavailable:
        print("video no disponible o enlace incorrecto")
        finishLabel.configure(text="video no disponible o enlace incorrecto", text_color="red")

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)
        

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize 
    bytes_download = total_size - bytes_remaining
    percentage_of_compeletion = int(bytes_download/total_size * 100)

    per = str(int(percentage_of_compeletion))
    pPercentaje.configure(text=per + '%')
    pPercentaje.update()

    progressBar.set(float(percentage_of_compeletion)/100)

def convert_to_mp3(input_file, output_file):
    audio = AudioFileClip(input_file)
    audio.write_audiofile(output_file, codec='libmp3lame')
    audio.close()

def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)



# configuracion 
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")



# frame de la aplicacion
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Descargador de Youtube")

link_frame = customtkinter.CTkFrame(app)
link_frame.pack(padx=10, pady=10)


# añado la interfaz 
title_label = customtkinter.CTkLabel(link_frame, text="INSERT YOUTUBE LINK")
title_label.pack(side="left") # tamaño

#barra de progresso
pPercentaje = customtkinter.CTkLabel(app, text="0%")
pPercentaje.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)


# input para el link 
url_var = tkinter.StringVar() # hago una variable url var para tener la ultima info de que es lo que hay en el link y usarlo en cualquier lado
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# botton de descarga 
download = customtkinter.CTkButton(app, text="DOWNLOAD", command=startDownload) 
download.pack(padx=15, pady=15)
link.pack(padx=5, pady=5)

context_menu = tkinter.Menu(app, tearoff=0)
context_menu.add_command(label="Paste", command=lambda: link.event_generate("<<Paste>>"))

link.bind("<Button-3>", show_context_menu)

# menu desplegable
download_choice = customtkinter.StringVar(app)
download_choice.set("Video MP4")

download_menu = customtkinter.CTkOptionMenu(app, values=["Video MP4" , "Audio MP3"], command=lambda value: download_choice.set(value)) 
download_menu.pack(padx=0, pady=0)

frame = customtkinter.CTkFrame(app)
frame.pack(pady=30, padx=30)

# ruta de carpeta
default_download_folder = os.path.expanduser("~/Downloads")
folder_path_var = tkinter.StringVar(value= default_download_folder) # defino una variable para guardar la ruta elejida
folder_label = customtkinter.CTkLabel(frame, text="FILE ROOT") #creo que prompt para que el usuario elija la ruta
folder_label.pack(pady=1, padx=1)

folder_path_entry = customtkinter.CTkEntry(app, textvariable=folder_path_var, state="readonly", width=150) 
folder_path_entry.pack(pady=1, padx=1)

#creo el boton 
browse_button = customtkinter.CTkButton(app, text="SEARCH", command=choose_folder)
browse_button.pack(padx=10, pady=10)

# termino la descarga 
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

resolution_frame = customtkinter.CTkFrame(app)
resolution_frame.pack(padx=5, pady=5)


# corro la app
app.mainloop()
