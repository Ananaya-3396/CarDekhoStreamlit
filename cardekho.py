import streamlit as st
import pandas as pd
import altair as alt


# st.title('Car Dekho Data Analysis')


data = pd.read_csv("cardekho_dataset.csv")
del data["Unnamed: 0"]
del data["model"]
data = data.loc[:, ["fuel_type", "transmission_type", "seller_type", "brand", "car_name",
                    "vehicle_age", "km_driven", "seats", "mileage", "engine", "max_power", "selling_price"]]

# columns_to_plot = st.sidebar.multiselect("Select column(s) for frequency distribution plot", options=data.columns))


data = data.rename(columns={"engine": "engine_capacity"})

def main():

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to",
                                ["Whole Data", "Filtered Data", "Analysis Report", "Frequency Distribution Plot"])

    if page == "Whole Data":
        whole_data(data)
    elif page == "Filtered Data":
        filtered_data_function(filtered_data)
    elif page == "Analysis Report":
        analysis_function(filtered_data)
    elif page == "Frequency Distribution Plot":
        dist_plot(filtered_data, columns_to_plot)
    # elif page == "Education/Certification":
    #     display_education()

def whole_data(data):
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

def filtered_data_function(filtered_data):
    if st.sidebar.button('View Filtered Data'):
        st.title('Car Dekho Filtered Data')
        st.write(filtered_data, height=800)

# metric_options = ['engine_capacity', 'mileage']
# selected_metric = st.sidebar.selectbox("Select the metric", metric_options)


def analysis_function(filtered_data):
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

    # if selected_metric == 'engine_capacity':
    #     filtered_data1 = filtered_data.groupby('engine_capacity')[['selling_price']].mean().reset_index()
    # elif selected_metric == 'mileage':
    #     filtered_data1 = filtered_data.groupby('mileage')[['selling_price']].mean().reset_index()

    # if not filtered_data1.empty:
    #     line_chart = alt.Chart(filtered_data1).mark_line().encode(
    #         x=alt.X(selected_metric + ':N', title=selected_metric.capitalize()),
    #         y=alt.Y('selling_price:Q', title='Selling Price')
    #     ).properties(
    #         width=600,
    #         height=400,
    #         title='Selling Price vs ' + selected_metric.capitalize()
    #     )
    #     st.altair_chart(line_chart, use_container_width=True)


    if not filtered_data.empty:
        # Create the first line chart for engine_capacity
        filtered_data1 = filtered_data.groupby('engine_capacity')[['selling_price']].mean().reset_index()
        line_chart_engine_capacity = alt.Chart(filtered_data1).mark_line().encode(
            x=alt.X('engine_capacity:N', title='Engine Capacity'),
            y=alt.Y('selling_price:Q', title='Selling Price')
        ).properties(
            width=600,
            height=400,
            title='Selling Price vs Engine Capacity'
        )

        # Create the second line chart for mileage
        filtered_data1 = filtered_data.groupby('mileage')[['selling_price']].mean().reset_index()
        line_chart_mileage = alt.Chart(filtered_data1).mark_line().encode(
            x=alt.X('mileage:N', title='Mileage'),
            y=alt.Y('selling_price:Q', title='Selling Price')
        ).properties(
            width=600,
            height=400,
            title='Selling Price vs Mileage'
        )

        # Display both charts
        st.altair_chart(line_chart_engine_capacity, use_container_width=True)
        st.altair_chart(line_chart_mileage, use_container_width=True)

options = ["vehicle_age", "km_driven", "seats", "mileage", "engine_capacity", "max_power", "selling_price"]

columns_to_plot = st.sidebar.multiselect("Select column(s) for frequency distribution plot",
                                                 options=options)



def dist_plot(filtered_data, columns_to_plot):
    for column in columns_to_plot:
        df = pd.DataFrame(filtered_data, columns=[column])
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(column, bin=True),
            y='count()',
        ).properties(
            width=600,
            height=400,
            title=f'{column} Distribution'
        )
        st.write(f"### {column} Distribution")
        st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    # st.set_page_config(page_title="Car Dekho Analysis Report", page_icon=":clipboard:", layout="wide")
    main()


