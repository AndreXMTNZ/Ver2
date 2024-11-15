import time
from gpiozero import MotionSensor
import os

# Configuración del sensor PIR en el pin GPIO 4
pir = MotionSensor(4)
video_path = "/home/pi/videos/video.mp4"  # Cambia esta ruta si tu video está en otro lugar

def play_video():
    # Activa la pantalla y reproduce el video en bucle
    os.system("vcgencmd display_power 1")  # Activa la pantalla
    os.system(f"cvlc --fullscreen --loop {video_path} &")  # Reproduce el video en VLC

def stop_video():
    # Detiene el video y apaga la pantalla
    os.system("pkill vlc")  # Detiene VLC
    os.system("vcgencmd display_power 0")  # Apaga la pantalla

while True:
    if pir.motion_detected:
        print("Movimiento detectado: reproduciendo video")
        play_video()

        # Espera hasta que no haya movimiento durante 30 segundos
        pir.wait_for_no_motion(timeout=30)
        print("No se detecta movimiento durante 30 segundos: apagando pantalla")
        stop_video()

    time.sleep(1)
