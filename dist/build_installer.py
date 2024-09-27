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

import os
import subprocess

def create_directory_structure(app_name, app_version):
    # Definir la estructura de los directorios necesarios para el paquete
    base_dir = f"{app_name}_package"  # Directorio base del paquete
    bin_dir = f"{base_dir}/usr/local/bin"  # Directorio donde irá el ejecutable
    debian_dir = f"{base_dir}/DEBIAN"  # Directorio para los archivos de control del paquete DEB
    
    # Crear los directorios necesarios
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(debian_dir, exist_ok=True)

    # Crear el archivo de control (control) que define los detalles del paquete
    control_content = f"""Package: {app_name}
        Version: {app_version}
        Section: utils
        Priority: optional
        Architecture: amd64
        Maintainer: Diego Parra <profediegoparra01@gmail.com>
        Description: {app_name} - Aplicación para descargar videos de YouTube como MP3 usando Kivy.
    """
    control_file_path = os.path.join(debian_dir, "control")  # Ruta del archivo de control
    with open(control_file_path, "w") as control_file:
        control_file.write(control_content)  # Escribir el contenido del archivo de control

    # Crear el script postinst para gestionar el enlace simbólico del ejecutable en el terminal
    postinst_content = f"""#!/bin/bash
        # Verificar si el enlace simbólico ya existe
        if [ -L /usr/local/bin/videodownloader ]; then
            # Si existe, eliminar el enlace simbólico
            rm /usr/local/bin/videodownloader
        fi

        # Crear un nuevo enlace simbólico al ejecutable
        ln -s /usr/local/bin/{app_name} /usr/local/bin/videodownloader
    """
    postinst_file_path = os.path.join(debian_dir, "postinst")  # Ruta del script postinst
    with open(postinst_file_path, "w") as postinst_file:
        postinst_file.write(postinst_content)  # Escribir el contenido del script postinst

    # Hacer el script postinst ejecutable
    os.system(f"chmod +x {postinst_file_path}")

    print(f"Estructura del paquete creada: {base_dir}")

def copy_executable(app_name, executable_path):
    # Copiar el ejecutable compilado al directorio bin del paquete
    bin_dir = f"{app_name}_package/usr/local/bin"  # Directorio de destino del ejecutable
    if os.path.isfile(executable_path):
        dest_path = os.path.join(bin_dir, app_name)  # Ruta completa donde se copiará el ejecutable
        os.system(f"cp {executable_path} {dest_path}")  # Copiar el archivo ejecutable
        # Asegurarse de que el archivo tenga permisos de ejecución
        os.system(f"chmod +x {dest_path}")
        print(f"Ejecutable copiado a: {dest_path}")
    else:
        print("¡Ejecutable no encontrado!")

def create_desktop_entry(app_name):
    # Crear la entrada del escritorio para la aplicación (archivo .desktop)
    desktop_entry_content = f"""[Desktop Entry]
        Name={app_name}
        Exec=/usr/local/bin/{app_name}
        Icon=utilities-terminal  # Icono genérico del sistema
        Type=Application
        Categories=Utility;
    """
    desktop_file_path = f"/usr/share/applications/{app_name}.desktop"  # Ruta del archivo .desktop
    with open(desktop_file_path, "w") as desktop_file:
        desktop_file.write(desktop_entry_content)  # Escribir el contenido de la entrada de escritorio
    
    # Establecer permisos de ejecución para el archivo .desktop
    os.system(f"chmod +x {desktop_file_path}")
    print(f"Entrada de escritorio creada en: {desktop_file_path}")

def build_deb_package(app_name):
    # Construir el paquete DEB usando dpkg-deb
    package_dir = f"{app_name}_package"  # Directorio base del paquete
    package_name = f"{app_name}.deb"  # Nombre del archivo DEB
    output_path = os.path.join(os.getcwd(), package_name)  # Obtener la ruta completa del archivo .deb
    subprocess.run(["dpkg-deb", "--build", package_dir, output_path], check=True)  # Crear el paquete DEB
    print(f"Paquete creado: {output_path}")

def install_package(app_name):
    # Instalar el paquete DEB
    package_name = f"{app_name}.deb"  # Nombre del archivo DEB
    package_path = os.path.join(os.getcwd(), package_name)  # Obtener la ruta completa del archivo .deb
    subprocess.run(["sudo", "dpkg", "-i", package_path], check=True)  # Instalar el paquete
    print(f"Paquete instalado: {package_path}")

if __name__ == "__main__":
    # Definir los detalles de la aplicación
    app_name = "VideoDownloader"
    app_version = "1.0"
    executable_path = "./main"  # Ruta del ejecutable compilado

    # Paso 1: Crear la estructura de directorios y el archivo de control
    create_directory_structure(app_name, app_version)

    # Paso 2: Copiar el ejecutable compilado al directorio del paquete
    copy_executable(app_name, executable_path)

    # Paso 3: Crear la entrada de escritorio para la aplicación
    create_desktop_entry(app_name)

    # Paso 4: Construir el paquete DEB
    build_deb_package(app_name)

    # Paso 5: Instalar el paquete
    install_package(app_name)

    print("Instalación completada con éxito.")
