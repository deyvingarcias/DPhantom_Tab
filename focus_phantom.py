# Importo de X libreria (selenium) Y herramoenta (webdriver) por ejemplo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
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

try:
    while True:
        driver.execute_script(js)
        # Preguntamos a la pagina si el video esta pausado, guardamos True o False en pausado
        pausado = driver.execute_script("return document.querySelector('video').paused")
        # Si pausado es True, avisamos en la terminal
        if pausado:
            print("⚠️ El video está pausado!")
        time.sleep(3)  # Ejecuta el script cada 3 segundos para mantener la ilusión
except KeyboardInterrupt:
    print("Terminando el programa...")
    driver.quit()