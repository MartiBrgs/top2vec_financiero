@echo off
title Top2Vec - Instalacion

REM Limpiar pantalla
cls

echo.
echo ================================================================
echo.
echo              TOP2VEC - INSTALACION
echo              Preparando el entorno
echo.
echo ================================================================
echo.
echo.
echo   Este proceso instalara todos los componentes necesarios
echo   para ejecutar Top2Vec.
echo.
echo   Tiempo estimado: 5-10 minutos
echo.
echo ----------------------------------------------------------------
echo.
echo   Presiona cualquier tecla para comenzar la instalacion
pause >nul
echo.

echo [1/3] Verificando Python
echo.
python --version
if errorlevel 1 goto error_python
echo.
echo   Python encontrado correctamente
echo.

echo [2/3] Creando entorno virtual
if exist .venv goto venv_exists
echo   Creando nuevo entorno virtual
python -m venv .venv
if errorlevel 1 goto error_venv_create
echo.
echo   Entorno virtual creado correctamente
goto activate_venv

:venv_exists
echo.
echo   Entorno virtual ya existe (omitiendo creacion)

:activate_venv
:activate_venv
echo.
echo   Activando entorno virtual
call .venv\Scripts\activate.bat
if errorlevel 1 goto error_venv_activate
echo.
echo   Entorno virtual activado correctamente
echo.

echo [3/3] Instalando dependencias
echo   (Esto puede tomar varios minutos, por favor espera)
echo.
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 goto error_pip_install
echo.
echo   Dependencias instaladas correctamente
echo.

echo.
echo ================================================================
echo.
echo              INSTALACION COMPLETADA
echo.
echo ================================================================
echo.
echo   Ahora puedes iniciar la aplicacion haciendo doble click en:
echo.
echo      INICIAR_APP.bat
echo.
echo   O leyendo el manual de usuario:
echo.
echo      LEEME.txt
echo.
echo.
echo   Presiona cualquier tecla para cerrar
pause >nul
exit /b 0

:error_python
echo.
echo ================================================================
echo   ERROR: Python no esta instalado
echo ================================================================
echo.
echo   Por favor instala Python 3.8 o superior desde:
echo   https://www.python.org/downloads/
echo.
echo   Durante la instalacion, marca la opcion:
echo   "Add Python to PATH"
echo.
echo   Presiona cualquier tecla para cerrar esta ventana
pause >nul
exit /b 1

:error_venv_create
echo.
echo ================================================================
echo   ERROR: No se pudo crear el entorno virtual
echo ================================================================
echo.
echo   Verifica que Python este instalado correctamente.
echo.
echo   Presiona cualquier tecla para cerrar
pause >nul
exit /b 1

:error_venv_activate
echo.
echo ================================================================
echo   ERROR: No se pudo activar el entorno virtual
echo ================================================================
echo.
echo   Intenta eliminar la carpeta .venv y ejecutar este script nuevamente.
echo.
echo   Presiona cualquier tecla para cerrar
pause >nul
exit /b 1

:error_pip_install
echo.
echo ================================================================
echo   ERROR: Fallo la instalacion de dependencias
echo ================================================================
echo.
echo   Intenta ejecutar este script nuevamente.
echo   Si el error persiste, verifica tu conexion a internet.
echo.
echo   Presiona cualquier tecla para cerrar
pause >nul
exit /b 1