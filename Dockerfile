#Utilise une image de base Python
FROM python:3.9-slim

#Definition du répertoire de travail
WORKDIR /app

#Copie du fichier requierements.txt dans le répertoire de travail
COPY requierements.txt /app/requierements.txt

#Installation des dépendances
RUN pip install --no-cache-dir -r requierements.txt

#Copie du reste de l'application
COPY . /app

#Copie du fichier CSV
COPY Online/Sales/Data.csv /app/Online_Sales_Data.csv

#Exposition du port
EXPOSE 8501

#Commande pour lancer l'application
CMD [ "streamlit", "RUN", "app.py" ]
