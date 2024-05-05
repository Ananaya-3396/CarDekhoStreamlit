import streamlit as st
import pandas as pd
import altair as alt

# st.title('Car Dekho Data Analysis')


data = pd.read_csv("cardekho_dataset.csv")
del data["Unnamed: 0"]
del data["model"]
data = data.loc[:, ["fuel_type", "transmission_type", "seller_type", "brand", "car_name",
                    "vehicle_age", "km_driven", "seats", "mileage", "engine", "max_power", "selling_price"]]

data = data.rename(columns={"engine": "engine_capacity"})

if st.sidebar.button('View Data'):
    st.title('Car Dekho Data')
    st.write(data, )

st.sidebar.header("Filters")

fuel_type = st.sidebar.multiselect("Select the fuel type you want to look",
                                   options=data["fuel_type"].unique(),

                                   )
data = data[data["fuel_type"].isin(fuel_type)]

seller_type = st.sidebar.multiselect("Select the seller type you want to look",
                                     options=data["seller_type"].unique(),

                                     )
data = data[data["seller_type"].isin(seller_type)]

brand = st.sidebar.multiselect("Select the brand you want to look",
                               options=data["brand"].unique(),

                               )
data = data[data['brand'].isin(brand)]

car_name = st.sidebar.multiselect("Select the car name you want to look",
                                  options=data["car_name"].unique(),

                                  )
filtered_data = data[data['car_name'].isin(car_name)]

metric_options = ['engine_capacity', 'mileage']
selected_metric = st.sidebar.selectbox("Select the metric", metric_options)

if st.sidebar.button('View Filtered Data'):
    st.title('Car Dekho Filtered Data')
    st.write(filtered_data, height=800)

# Plot vehicle age vs km driven using bar chart
if not filtered_data.empty:
    chart_data = filtered_data.groupby('vehicle_age')['km_driven'].sum().reset_index()
    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x='vehicle_age:O',
        y='km_driven:Q'
    ).properties(
        width=600,
        height=400)

if not filtered_data.empty:
    seat_counts = filtered_data['seats'].value_counts().reset_index()
    seat_counts.columns = ['Seats', 'Count']

    pie_chart = alt.Chart(seat_counts).mark_arc().encode(
        theta="Count",
        color="Seats"
    ).properties(
        width=600,
        height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Vehicle Age vs Kilometers Driven")
        st.altair_chart(bar_chart, use_container_width=True)

    with col2:
        st.write("Seats Count")
        st.altair_chart(pie_chart, use_container_width=True)

if selected_metric == 'engine_capacity':
    filtered_data1 = filtered_data.groupby('engine_capacity')[['selling_price']].mean().reset_index()
elif selected_metric == 'mileage':
    filtered_data1 = filtered_data.groupby('mileage')[['selling_price']].mean().reset_index()

if not filtered_data1.empty:
    line_chart = alt.Chart(filtered_data1).mark_line().encode(
        x=alt.X(selected_metric + ':N', title=selected_metric.capitalize()),
        y=alt.Y('selling_price:Q', title='Selling Price')
    ).properties(
        width=600,
        height=400,
        title='Selling Price vs ' + selected_metric.capitalize()
    )
    st.altair_chart(line_chart, use_container_width=True)

