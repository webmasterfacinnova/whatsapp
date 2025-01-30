# Utilizamos la imagen oficial de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo
# WORKDIR /app

# Copiamos el archivo requirements.txt al directorio de trabajo
# COPY requirements.txt .

# Instalamos las dependencias
# RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código al directorio de trabajo
# COPY . .

# Ejecutamos las pruebas unitarias
# CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
