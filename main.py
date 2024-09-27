# Video Downloader App
# Copyright (C) 2024 Diego Parra
#
# Este programa es software libre: puede redistribuirlo y/o modificarlo bajo
# los términos de la Licencia Pública General de GNU publicada por la Free Software
# Foundation, ya sea la versión 3 de la Licencia, o (a su elección) cualquier versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de
# COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.
# Consulte la Licencia Pública General de GNU para más detalles.
#
# Debería haber recibido una copia de la Licencia Pública General de GNU
# junto con este programa. Si no, consulte <https://www.gnu.org/licenses/>.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window  # Importar para cambiar el tamaño de la ventana
from threading import Thread
import yt_dlp
import os
import re

# Ajustar el tamaño de la ventana de la aplicación
Window.size = (400, 500)

class DownloadScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)  # Definir padding alrededor de los widgets
        self.spacing = dp(10)  # Espacio entre los widgets

        # Header con el nombre de la aplicación
        self.header = Label(
            text="[b]Video Downloader[/b]",  # Texto con formato negrita
            size_hint=(1, 0.2),  # Tamaño proporcional en la interfaz
            font_size='24sp',  # Tamaño de la fuente
            markup=True,
            color=(0, 0.5, 0.8, 1)  # Color del texto
        )
        self.add_widget(self.header)

        # Campo de entrada para el enlace del video
        self.link_input = TextInput(
            hint_text="Ingresa el enlace del video",  # Texto que aparece en el input
            size_hint=(1, 0.15),
            font_size='16sp'  # Tamaño de la fuente del input
        )
        self.add_widget(self.link_input)

        # Botón para seleccionar la ruta de descarga
        self.path_button = Button(
            text="Elegir ruta de descarga", 
            size_hint=(1, 0.15),
            background_color=(0.1, 0.6, 0.3, 1),  # Color de fondo del botón
            font_size='16sp'
        )
        self.path_button.bind(on_press=self.select_path)  # Vincular acción al presionar el botón
        self.add_widget(self.path_button)

        # Etiqueta para mostrar la ruta seleccionada
        self.selected_path_label = Label(
            text="Ruta: No seleccionada",  # Texto inicial
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0.8, 0, 0, 1),  # Color de la etiqueta
            text_size=(Window.width - dp(40), None),  # Ajustar el ancho del texto
            halign='left',  # Alinear texto a la izquierda
            valign='middle'  # Centrar verticalmente el texto
        )
        self.selected_path_label.bind(size=self.update_text_wrap)  # Actualizar ajuste de texto según tamaño
        self.add_widget(self.selected_path_label)

        # Barra de progreso
        self.progress_bar = ProgressBar(value=0, max=100, size_hint=(1, 0.1))
        self.add_widget(self.progress_bar)

        # Etiqueta para mostrar el progreso en porcentaje
        self.progress_label = Label(
            text="Progreso: 0%", 
            size_hint=(1, 0.1),
            font_size='14sp'
        )
        self.add_widget(self.progress_label)

        # Botón para iniciar la descarga
        self.download_button = Button(
            text="Descargar MP3", 
            size_hint=(1, 0.15),
            background_color=(0.2, 0.5, 0.8, 1),  # Color de fondo del botón
            font_size='16sp'
        )
        self.download_button.bind(on_press=self.start_download)  # Iniciar la descarga al presionar el botón
        self.add_widget(self.download_button)

        # Etiqueta para mostrar el estado de la descarga
        self.status_label = Label(
            text="Estado: Esperando...",  # Texto inicial
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)  # Color gris para el estado
        )
        self.add_widget(self.status_label)

        # Footer con el nombre y correo del desarrollador
        self.footer = Label(
            text="[i]Desarrollado por Diego Parra - profediegoparra01@gmail.com[/i]",  # Texto en cursiva
            size_hint=(1, 0.1),
            font_size='12sp', 
            markup=True, 
            color=(0.3, 0.3, 0.3, 1)  # Color del texto del footer
        )
        self.add_widget(self.footer)

    def select_path(self, instance):
        # Crear un popup para seleccionar la carpeta de descarga
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path=os.path.expanduser('~'), dirselect=True)  # Selección de directorios
        content.add_widget(filechooser)

        # Botón para confirmar la selección de la carpeta
        select_button = Button(
            text="Seleccionar", 
            size_hint=(1, 0.2),
            background_color=(0.1, 0.6, 0.3, 1)  # Color del botón de selección
        )
        select_button.bind(on_press=lambda x: self.confirm_path(filechooser.path))  # Vincular acción
        content.add_widget(select_button)

        # Crear y abrir el popup para seleccionar la carpeta de destino
        popup = Popup(title="Selecciona la carpeta de destino", content=content, size_hint=(0.9, 0.9))
        popup.open()

        # Guardar referencia del popup para cerrarlo más tarde
        self.path_popup = popup

    def confirm_path(self, path):
        # Cerrar el popup y guardar la ruta seleccionada
        self.download_path = path
        self.selected_path_label.text = f"Ruta: {self.download_path}"  # Actualizar la etiqueta con la ruta seleccionada
        self.path_popup.dismiss()

    def start_download(self, instance):
        # Validar que se haya seleccionado una ruta de descarga
        if not self.download_path:
            self.status_label.text = "Error: Selecciona una ruta"
            return
        link = self.link_input.text  # Obtener el enlace del video
        if not link:
            self.status_label.text = "Error: Ingresa un enlace"
            return

        # Actualizar el estado e iniciar la descarga en un hilo separado
        self.status_label.text = "Estado: Descargando..."
        self.download_button.disabled = True  # Desactivar el botón mientras se descarga
        Thread(target=self.download_video, args=(link,)).start()  # Ejecutar la descarga en un hilo

    def download_video(self, link):
        # Configuración para descargar el video como MP3 usando yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',  # Mejor calidad de audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convertir a formato MP3
                'preferredquality': '192',  # Calidad de 192 kbps
            }],
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),  # Ruta de salida
            'progress_hooks': [self.progress_hook],  # Vincular la barra de progreso
        }
        try:
            # Descargar el video usando la configuración especificada
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except yt_dlp.utils.DownloadError as e:
            self.status_label.text = f"Error: {str(e)}"  # Mostrar mensaje de error si falla
        except Exception as e:
            self.status_label.text = f"Error inesperado: {str(e)}"  # Mostrar otros errores inesperados

    def progress_hook(self, d):
        # Actualizar la barra de progreso y el estado durante la descarga
        if d['status'] == 'downloading':
            progress = d['_percent_str']  # Obtener porcentaje de descarga
            progress = re.sub(r'\x1b\[[0-9;]*m', '', progress).replace('%', '').strip()  # Limpiar caracteres especiales
            self.progress_bar.value = float(progress)  # Actualizar valor de la barra de progreso
            Clock.schedule_once(lambda dt: self.update_progress(progress))

        # Cuando la descarga se complete, actualizar el estado
        if d['status'] == 'finished':
            self.status_label.text = "Estado: Descarga completa"
            Clock.schedule_once(lambda dt: self.reset_interface())  # Reiniciar la interfaz después de completar

    def update_progress(self, progress):
        # Actualizar la etiqueta con el progreso de descarga
        self.progress_label.text = f"Progreso: {progress}%"
        self.status_label.text = f"Estado: {progress}% completado"

    def reset_interface(self):
        # Reiniciar la interfaz para permitir nuevas descargas
        self.download_button.text = "Descargar otro video"
        self.download_button.disabled = False
        self.progress_bar.value = 0
        self.progress_label.text = "Progreso: 0%"
        self.status_label.text = "Estado: Esperando..."
        self.link_input.text = ""  # Limpiar el campo de enlace
        self.selected_path_label.text = "Ruta: No seleccionada"  # Restablecer la ruta

    # Función para actualizar el ajuste de texto en el label cuando cambia el tamaño
    def update_text_wrap(self, instance, value):
        instance.text_size = (instance.width - dp(20), None)  # Ajusta el tamaño del texto según el ancho disponible

class VideoDownloaderApp(App):
    def build(self):
        # Crear y mostrar la pantalla principal de descarga
        return DownloadScreen()

if __name__ == '__main__':
    VideoDownloaderApp().run()  # Ejecutar la aplicación
