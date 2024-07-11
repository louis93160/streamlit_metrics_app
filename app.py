import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Titre de l'application
st.title("Insights sur les Ventes en Ligne")

# Lecture du fichier CSV
df = pd.read_csv("Online_Sales_Data.csv")

# Convertir la colonne 'Date' en datetime sans afficher les minutes
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Ajouter des filtres par région et date
st.sidebar.header("Filtres")
region_options = df['Region'].unique()
selected_regions = st.sidebar.multiselect('Sélectionner les Régions', region_options, region_options)

min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = st.sidebar.date_input('Sélectionner la plage de dates', [min_date, max_date])

# Filtrer les données
df_filtered = df[(df['Region'].isin(selected_regions)) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Calculs
def calculate_sales_by_region(data):
    return data.groupby('Region')['Total Revenue'].sum().reset_index()

def calculate_sales_over_time(data):
    return data.groupby('Date')['Total Revenue'].sum().reset_index()

def calculate_top_selling_products(data, metric='Units Sold'):
    top_products = data.groupby('Product Name')[metric].sum().reset_index()
    top_products = top_products.sort_values(by=metric, ascending=False).head(10)
    return top_products

def calculate_revenue_by_payment_method(data):
    return data.groupby('Payment Method')['Total Revenue'].sum().reset_index()

def calculate_heatmap_data(data):
    heatmap_data = data.pivot_table(values='Total Revenue', index='Product Name', columns='Region', aggfunc='sum')
    heatmap_data = heatmap_data.fillna(0)
    return heatmap_data

# Agrégation des données par mois, catégorie de produit et région
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
agg_data = df_filtered.groupby(['Month', 'Product Category', 'Region']).agg({
    'Units Sold': 'sum',
    'Total Revenue': 'sum'
}).reset_index()

# Visualisations
st.header("Ventes Totales par Région")
sales_by_region = calculate_sales_by_region(df_filtered)
fig_region = px.bar(sales_by_region, x='Region', y='Total Revenue', title="Ventes Totales par Région")
st.plotly_chart(fig_region)

st.header("Ventes Journalières")
sales_over_time = calculate_sales_over_time(df_filtered)
fig_time = px.line(sales_over_time, x='Date', y='Total Revenue', title="Ventes Journalières")
st.plotly_chart(fig_time)

st.header("Top 10 des Produits les Plus Vendus")
top_products = calculate_top_selling_products(df_filtered)
fig_products = px.bar(top_products, x='Product Name', y='Units Sold', title="Top 10 des Produits les Plus Vendus")
st.plotly_chart(fig_products)

st.header("Revenus par Méthode de Paiement")
revenue_by_payment = calculate_revenue_by_payment_method(df_filtered)
fig_payment = px.pie(revenue_by_payment, names='Payment Method', values='Total Revenue', title="Revenus par Méthode de Paiement")
st.plotly_chart(fig_payment)

st.header("Heatmap des Ventes par Produit et Région")
heatmap_data = calculate_heatmap_data(df_filtered)
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='OrRd'
))
fig_heatmap.update_layout(title="Heatmap des Ventes par Produit et Région", xaxis_title="Région", yaxis_title="Produit")
st.plotly_chart(fig_heatmap)

# Visualisation des tendances
st.header("Tendances des Ventes par Catégorie de Produit")

# Plot Units Sold by Product Category
fig_category_units = px.line(agg_data, x='Month', y='Units Sold', color='Product Category', title='Unités Vendues par Catégorie de Produit au fil du Temps')
st.plotly_chart(fig_category_units)

# Plot Total Revenue by Product Category
fig_category_revenue = px.line(agg_data, x='Month', y='Total Revenue', color='Product Category', title='Revenu Total par Catégorie de Produit au fil du Temps')
st.plotly_chart(fig_category_revenue)

st.header("Tendances des Ventes par Région")

# Plot Units Sold by Region
fig_region_units = px.line(agg_data, x='Month', y='Units Sold', color='Region', title='Unités Vendues par Région au fil du Temps')
st.plotly_chart(fig_region_units)

# Plot Total Revenue by Region
fig_region_revenue = px.line(agg_data, x='Month', y='Total Revenue', color='Region', title='Revenu Total par Région au fil du Temps')
st.plotly_chart(fig_region_revenue)

# Ajout de KPIs
st.sidebar.header("KPIs")
total_revenue = df_filtered['Total Revenue'].sum()
total_units_sold = df_filtered['Units Sold'].sum()
st.sidebar.metric("Revenus Totaux", f"${total_revenue:,.2f}")
st.sidebar.metric("Total des Unités Vendues", f"{total_units_sold:,}")

