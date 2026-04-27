# ServiGuia Backend By EDC
Backend para la aplicación de ServiGuia. Desarrollado por Equipo de Cuatro.

## ¿Cómo comenzar a trabajar?
### Clonar repositorio
```
git clone https://github.com/santiagopoblete/serviGuiaBack
cd serviGuiaBack
```

### Crear y activar virtual environment
- Windows
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

- iOS
```
python -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias y paquetes
`pip install -r requirements.txt`

### Crear .env
En el folder raíz de tu proyecto, crear un archivo .env. Dentro de este archivo incluir lo siguiente:
`OPENAI_API_KEY=stringDeAPIkey`

### Adjuntar master_prompt.txt
En el folder raíz de tu proyecto, subir el archivo master_prompt.txt compartido contigo. Este archivo incluye el comportamiento deseado del modelo de IA.

## Al trabajar
### Correr el servidor
Correr el siguiente comando en la terminal:
`fastapi dev`

### Instalar nuevas dependencias y paquetes
Si se instalarán nuevos paquetes, es importante actualizar el archivo de requirements.txt.
Para hacer esto, correr el siguiente comando en la terminal una vez instaladas todas las dependencias nuevas:
```
pip install -r requirements.txt
pip freeze > requirements.txt
```

## Al terminar de trabajar
### Detener el servidor
En terminal realizar el comando Ctrl + C.

### Detener virtual environment
Escribir en la terminal el siguiente comando:
`deactivate`
