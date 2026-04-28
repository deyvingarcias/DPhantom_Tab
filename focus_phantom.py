# Importo de X libreria (selenium) Y herramoenta (webdriver) por ejemplo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pygame

#--------------------------
# Inicializamos el modulo de sonido de pygame antes de usarlo
pygame.mixer.init()
#--------------------------

# Parte del usuario, introduce URL que quiere y driver abre la pagina, luego inyectamos el JS 
# para engañar a la pagina y evitar que detecte que no estamos en la pestaña activa
url = input("Introduce la URL del sitio web: ")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

#--------------------------
# Inyectamos JS para engañar a la pagina:
# - visibilityState siempre devuelve "visible"
# - hidden siempre devuelve false
# - interceptamos y cancelamos los eventos visibilitychange y blur
# - stopImmediatePropagation corta la cadena antes de que llegue al reproductor

js = """
Object.defineProperty(document, 'visibilityState', {value: 'visible', writable: false});
Object.defineProperty(document, 'hidden', {value: false, writable: false});
window.addEventListener('visibilitychange', function(e) {e.stopImmediatePropagation(); }, true);
window.addEventListener('blur', function(e) {e.stopImmediatePropagation(); }, true);
"""

#---------------------------
# Bucle infinito que reinyecta el JS cada 3 segundos.
# Tambien comprueba si el video esta pausado cada ciclo.
# - execute_script con return devuelve el valor JS a Python
# - si pausado es True significa que algo interrumpio el video
# Ctrl+C para cerrar limpiamente

# ya_avisado evita que la alarma suene en bucle mientras el video siga pausado
# se inicializa fuera del bucle para que no se resetee cada 3 segundos
ya_avisado = False

try:
    while True:
        driver.execute_script(js)
        try:
            pausado = driver.execute_script("return document.querySelector('video').paused")
            if pausado and not ya_avisado:
                # Solo suena una vez — cuando ya_avisado es False y el video esta pausado
                print("⚠️ El video está pausado!")
                pygame.mixer.Sound('alert.wav').play()
                ya_avisado = True  # Marcamos que ya avisamos para no repetir
            elif not pausado:
                # El video se reanudo — reseteamos ya_avisado y paramos el sonido
                ya_avisado = False  
                pygame.mixer.stop()  # Detenemos la alarma si el video se reanuda
        except:
            pass  # No hay video en la pagina todavia, ignoramos
        time.sleep(3)
except KeyboardInterrupt:
    print("Terminando el programa...")
    driver.quit()