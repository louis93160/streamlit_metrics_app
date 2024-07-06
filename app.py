import streamlit as st
import pandas as pd

# Titre de l'application

st.title("Insights sur les Ventes en Ligne")

# Lecture du fichier CSV

df = pd.read_csv("Online_Sales_Data.csv")
