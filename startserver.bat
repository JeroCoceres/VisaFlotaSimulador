@echo off
REM Buscar la dirección IPv4
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do set IP=%%i

REM Quitar espacios iniciales en la variable IP
set IP=%IP:~1%

REM Mostrar la dirección IP con el puerto
echo La URL para acceder al simulador es: http://%IP%:8000
echo .
echo Recuerde que para salir del mismo debe apretar 'ctrl + c' (y enter) y a continuacion: 's' (y enter)
echo .
echo .
echo .
REM Cambiar al directorio del proyecto
cd /d C:\Users\jeron\OneDrive\Documentos\Proyectos\VisaFlotaSimulador

REM Activar el entorno virtual
call venv\Scripts\activate

REM Iniciar el servidor Django
python manage.py runserver 0.0.0.0:8000 --insecure

pause
