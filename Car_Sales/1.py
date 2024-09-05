import pandas as pd
import streamlit as st
import plotly.express as px
import  toml



#set page config
st.set_page_config(page_title='Car Stock Dashboard', page_icon=':car:', layout='wide')
# Load the data
@st.cache_data
def get_data():
    data = pd.read_csv("cars.csv",index_col=0)
    return data

df = get_data()

#rename the Foreign/Local Used column
df=df.rename(columns={'Foreign/Local Used':'Foreign_Local_Used'})



# import sidebar
st.sidebar.header('Please filter here')


# manufacturer sidebar
manufacturer = st.sidebar.multiselect(
    'Select the Manufacturer:',
    options= df['manufacturer'].unique(),
    default= df['manufacturer'].unique()
)

# automation sidebar
automation = st.sidebar.radio(
    'Select the Automation:',
    options= df['Automation'].unique(),
)

# use category sidebar
use_category =st.sidebar.radio(
    "Select the use_category:",
    options= df['Foreign_Local_Used'].unique()
)

# linking filters with main_page
df_select=df.query(
    "manufacturer == @manufacturer & Automation == @automation & Foreign_Local_Used==@use_category"
)

# if selection is not available
if df_select.empty:
    st.warning('No data available on the current filter setting')
# set title
st.title(' :car: Car Stock Dashboard')
st.markdown('##')

#calculate KPI's
average_price = int(df_select['price'].mean())
car_count = df_select.shape[0] #counts the number of rows
earliest_make_year = df_select['make-year'].min()

first_column, second_column, third_column = st.columns(3)

with first_column:
    st.subheader('Average Price')
    st.subheader(f"NGN ₦ {average_price:,}")

with second_column:
    st.subheader('Car Count')
    st.subheader(f"{car_count:,} Cars")

with third_column:
    st.subheader('Earliest Make Year')
    st.subheader(f"{earliest_make_year}")

# adding divider
st.divider()



# Group by color and sum prices, then sort by total price
Price_per_color = df_select.groupby('color')['price'].sum().sort_values()

# Create bar chart for price per color
fig_color_price = px.bar(
    Price_per_color,
    x='price',
    y=Price_per_color.index,
    orientation='h',  # Horizontal bar chart
    title='<b>Price per Color</b>',
    color_discrete_sequence=['#0083b8'] * len(Price_per_color),
    template='plotly_white'
)
fig_color_price.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)



# Group by manufacturer and sum prices, then sort by total price
Price_per_make = df_select.groupby('manufacturer')['price'].sum().sort_values()

# Create bar chart for price per manufacturer
fig_make_price = px.bar(
    Price_per_make,
    x=Price_per_make.index,
    y=Price_per_make.values,
    orientation='v',  # Vertical bar chart
    title='<b>Price per Manufacturer</b>',
    color_discrete_sequence=['#0083b8'] * len(Price_per_make),
    template='plotly_white'
)
fig_make_price.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)

# Display charts in Streamlit columns
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_color_price, use_container_width=True)
right_column.plotly_chart(fig_make_price, use_container_width=True)


st.divider()

#add more kpi's
import streamlit as st

# Calculate min and max prices
max_price = df_select['price'].max()
min_price = df_select['price'].min()


# Sample data
min_price = df_select['price'].min()
max_price = df_select['price'].max()

# add KPI's
left_column,middle_column,right_column= st.columns(3)


with left_column:
    st.metric(
    label='Minimum price of cars selected (₦)',
    value=f"NGN ₦ {min_price:,}"
)
with left_column:
    st.metric(
    label='Maximum price of cars selected (₦)',
    value=f"NGN ₦ {max_price:,}"
)
#plot pie chart to show seat-make distribution
seat_make_dist = df.groupby('seat-make')['price'].agg('count').sort_values()

fig_seat_dist = px.pie(
    seat_make_dist,
   values='price',
    title= 'seat Make Distribution',
    names=seat_make_dist.index,
    color_discrete_sequence=px.colors.sequential.RdBu,
    hole = 0.4
)
fig_make_price.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)




#seat make pie chart plot
middle_column.plotly_chart(fig_seat_dist,use_container_width=True)

# right column

#make year plot
make_year_fig = px.histogram(df_select,x='make-year',title='Make Year Distribution')
make_year_fig.update_layout(
    plot_bgcolor = 'rgba(0,0,0,0)',
    bargap=0.1,
    xaxis=(dict(showgrid=False))
)
right_column.plotly_chart(make_year_fig,use_container_width=True)



