
# Video Downloader App

¡Bienvenido a Video Downloader App! Esta aplicación te permite descargar videos de YouTube como archivos MP3 fácilmente, con una interfaz gráfica amigable desarrollada en Kivy. Solo necesitas ingresar el enlace del video, seleccionar la carpeta de destino y comenzar la descarga. La app también incluye una barra de progreso para mostrar el avance de la descarga y notificaciones sobre el estado de la misma.

![Icon App](/img/iconApp.jpg)
## Características

- **Descargas rápidas**: Convierte videos de YouTube a MP3 con solo un clic.
- **Interfaz gráfica**: Fácil de usar, desarrollada con Kivy.
- **Barra de progreso**: Visualiza el avance de la descarga en tiempo real.
- **Selección de carpeta**: Elige dónde guardar tus archivos MP3.
- **Conversión a MP3**: La app utiliza `yt-dlp` y `FFmpeg` para convertir videos a audio de alta calidad.
- **Compatibilidad multiplataforma**: Funciona en Windows, Linux y macOS.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.6+** 
- **FFmpeg** (necesario para la conversión a MP3)
- Las dependencias listadas en el archivo `requirements.txt`:

```txt
yt-dlp==2023.9.24
kivy[full]
plyer
easygui
pyinstaller
```

## Instalación

### Paso 1: Clonar el repositorio

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/Diego-debian/musica.git
cd videodownloaderapp
```

### Paso 2: Instalar las dependencias

Instala las dependencias necesarias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

### Paso 3: Crear el ejecutable

Para convertir la aplicación en un ejecutable independiente, utilizamos PyInstaller. Puedes hacerlo con el siguiente comando:

```bash
pyinstaller --onefile --log-level=DEBUG main.py
```

Este comando generará un archivo ejecutable en la carpeta `dist/`. Ahora tendrás un archivo binario que podrás ejecutar directamente en tu sistema.

### Paso 4: Crear el instalador (opcional)

Si deseas crear un instalador para facilitar la distribución de la aplicación, ejecuta el siguiente comando:

```bash
python3 build_installer.py
```

Este script generará un instalador que te permitirá distribuir la aplicación fácilmente a otros usuarios.

### Paso 5: Ejecutar la aplicación

Una vez creado el ejecutable, puedes ejecutarlo directamente:

- **Windows**: Navega a la carpeta `dist` y haz doble clic en `main.exe`.
- **Linux/macOS**: Navega a la carpeta `dist` y ejecuta el archivo desde la terminal:

```bash
./main
```

## Uso

1. Abre la aplicación.
2. Ingresa el enlace del video de YouTube que deseas descargar.
3. Selecciona la carpeta de destino.
4. Haz clic en "Descargar MP3".
5. Observa la barra de progreso y el estado de la descarga en tiempo real.
6. Una vez finalizada la descarga, el archivo MP3 estará disponible en la carpeta seleccionada.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un issue o un pull request en el repositorio. ¡Apreciamos tus ideas y mejoras!

## Contacto

Desarrollado por Diego Debian  
Correo: [profediegoparra01@gmail.com](mailto:profediegoparra01@gmail.com)

¡Gracias por usar Video Downloader App! 🎧🚀
