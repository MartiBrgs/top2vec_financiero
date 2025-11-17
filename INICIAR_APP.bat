@echo off
title Top2Vec - Aplicacion Web para Economistas

REM Limpiar pantalla
cls

echo.
echo ================================================================
echo.
echo              TOP2VEC - APLICACION WEB
echo              Analisis de Topicos en Noticias
echo.
echo ================================================================
echo.
echo.
echo   Iniciando aplicacion web...
echo   Por favor espera unos segundos...
echo.
echo   La aplicacion se abrira automaticamente en tu navegador
echo   en la direccion: http://localhost:8501
echo.
echo ----------------------------------------------------------------
echo   Para DETENER la aplicacion: Cierra esta ventana
echo   o presiona Ctrl+C
echo ----------------------------------------------------------------
echo.
echo.

REM Activar entorno virtual local
call .venv\Scripts\activate.bat

REM Ejecutar aplicación Streamlit
python -m streamlit run src\app.py

REM Si hay error, pausar para ver el mensaje
if errorlevel 1 (
    echo.
    echo ================================================================
    echo   ERROR: No se pudo iniciar la aplicacion
    echo ================================================================
    echo.
    echo   Posibles soluciones:
    echo   1. Ejecuta primero: INSTALAR.bat
    echo   2. Verifica que Python este instalado
    echo   3. Lee el archivo: LEEME.txt
    echo.
    echo   Presiona cualquier tecla para cerrar...
    pause >nul
)
