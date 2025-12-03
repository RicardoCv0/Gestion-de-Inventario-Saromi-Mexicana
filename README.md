#  Gestion de Inventario Saromi Mexicana

## Instrucciones

### Para ejecutar el servidor:

1. Crear un entorno virtual 

```shell
py -m venv venv
```

2. Activa el entorno virtual

- En windows:
```powershell
.\venv\Scripts\activate
```

- En Linux:
```shell
source venv/bin/activate
```

3. Instala django
```shell
py -m pip install django
```

4. Inicia el servidor
```shell
py manage.py runserver 
```

### Para ejecutar las pruebas
Ejecuta el siguiente comando en la terminal:

```shell
py manage.py test
```

Si deseas generar un reporte de las pruebas, ejecuta el script:

```shell
.\generate_test_report.bat
```
El reporte se generará en el archivo `salida.txt`