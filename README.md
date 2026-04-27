# DPhantom Tab

Script en Python que evita que plataformas de cursos pausan el video al cambiar de pestaña.

## ¿Qué hace?
Abre Chrome con Selenium e inyecta JavaScript cada 3 segundos que sobreescribe la Page Visibility API del navegador, cancelando los eventos `visibilitychange` y `blur` antes de que lleguen al reproductor. También avisa en terminal si el video se pausa.

## Instalación
\```bash
pip install selenium webdriver-manager
\```

## Uso
\```bash
python focus_phantom.py
\```
Introduce la URL cuando te la pida. `Ctrl+C` para cerrar.

## Requisitos
- Python 3.x
- Google Chrome instalado

## TODO
- Detección de popups "¿Sigues aquí?"
- Soporte múltiples pestañas