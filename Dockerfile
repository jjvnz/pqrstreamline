# Utiliza una imagen base de Python
FROM python:3.12-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación a la imagen
COPY . .

# Expone el puerto en el que tu aplicación escuchará
EXPOSE 80

# Define el comando por defecto para ejecutar tu aplicación usando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
