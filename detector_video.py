from gpiozero import MotionSensor
import subprocess
import time
import os

# Configuración del sensor PIR
pir = MotionSensor(17)  # GPIO 17
video_path = "/ruta/a/tu/video.mp4"  # Cambia esta ruta al archivo de video
vlc_process = None  # Variable para controlar el proceso de VLC

try:
    print("Esperando detección de movimiento...")
    while True:
        # Esperar movimiento
        pir.wait_for_motion()
        print("¡Movimiento detectado! Reproduciendo video...")
        
        # Iniciar VLC si no está ejecutándose
        if vlc_process is None:
            vlc_process = subprocess.Popen(["vlc", "--fullscreen", "--no-video-title-show", video_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Esperar 30 segundos de inactividad
        last_motion_time = time.time()
        while time.time() - last_motion_time < 30:
            if pir.motion_detected:
                print("Movimiento detectado, reiniciando temporizador...")
                last_motion_time = time.time()
            time.sleep(1)
        
        # No se detectó movimiento en 30 segundos
        print("No se detectó movimiento por 30 segundos. Cerrando VLC...")
        if vlc_process is not None:
            vlc_process.terminate()  # Terminar el proceso de VLC
            vlc_process = None  # Reiniciar el control del proceso

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")

finally:
    # Asegurar que VLC se cierre si está abierto
    if vlc_process is not None:
        vlc_process.terminate()
    print("Limpiando recursos...")
