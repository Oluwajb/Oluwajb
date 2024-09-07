import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Sales Dashboard', page_icon=':bar_chart:', layout='wide')

# Center the title with reduced margin using Markdown with HTML and CSS
st.markdown("""
    <style>
        .title {
            text-align: center;
            margin-top: -50px; /* Adjust the margin-top as needed to move the title upwards */
            margin-bottom: 10px; /* Optional: Adjust the margin-bottom if needed */
        }
    </style>
    <h1 class="title">Estate Sales Analysis</h1>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def get_data():
    data = pd.read_csv('DA/Data/DA_Sales.csv')
    return data

df = get_data()

# Sidebar for filters
st.sidebar.header('Select Filter')
selected_estates = st.sidebar.multiselect(
    'Estate:',
    options=df['Estate'].unique(),
    default=df['Estate'].unique()
)
selected_payment_types = st.sidebar.multiselect(
    'Payment Type:',
    options=df['PAYMENT TYPE'].unique(),
    default=df['PAYMENT TYPE'].unique()
)

# Apply filters to the DataFrame based on selected values
df_select = df[
    df['Estate'].isin(selected_estates) &
    df['PAYMENT TYPE'].isin(selected_payment_types)
]

if df_select.empty:
    st.warning('No data available with the current filter settings.')

# Display the filtered DataFrame
with st.expander('Display Data'):
    st.dataframe(df_select)

# Create columns for metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Display the number of unique estates
estate_count = df_select['Estate'].nunique()
with col1:
    st.metric(
        value=f'{estate_count} estates',
        label='Distinct Estate'
    )

# Transaction count
number_of_transaction = df_select.shape[0]
with col2:
    st.metric(
        value=f'{number_of_transaction} transactions',
        label='Total Transactions'
    )

# Total cost of land
cost_of_land = df_select['cost_of_land'].sum()
with col3:
    st.metric(
        value=f'₦{cost_of_land:,.0f}',
        label='Total Cost of Land'
    )

# Amount paid
amount_paid = df_select['amount_paid'].sum()
with col4:
    st.metric(
        value=f'₦{amount_paid:,}',
        label='Total Amount Paid'
    )

# Outstanding payment
balance = df_select['Balance'].sum()
with col5:
    st.metric(
        value=f'₦{balance:,}',
        label='Total Outstanding Payment'
    )

# Excess payment
refund = df_select['Refund'].sum()
with col6:
    st.metric(
        value=f'₦{refund:,}',
        label='Excess Payment'
    )

# Define a common blue color scale and sequence
color_continuous_scale = 'Blues'
color_discrete_sequence = px.colors.sequential.Greys

# Bar chart for cost of land per estate
cost_per_estate = df_select.groupby('Estate')['cost_of_land'].sum().sort_values(ascending=False)
fig1 = px.bar(
    cost_per_estate,
    x=cost_per_estate.index,
    y='cost_of_land',
    title='Cost of Land per Estate',
    labels={'Estate': 'Estate', 'cost_of_land': 'Cost of Land'},
    color='cost_of_land',
    color_continuous_scale=color_continuous_scale,
    text='cost_of_land',  # Display the value on the bars
)

# Update layout for better appearance
fig1.update_layout(
    xaxis_title='Estate',
    yaxis_title='Cost of Land (₦)',
    title_font_size=20,
    title_x=0.5,
    xaxis_tickangle=-45,
    margin=dict(l=0, r=0, t=40, b=0),
    template='plotly_white'
)

# Customize text labels to include commas
fig1.update_traces(
    texttemplate='%{text:,.0f}',  # Format text with commas
    textposition='outside',  # Position text outside the bars
)

st.plotly_chart(fig1)

with st.expander('Total Cost by Estate'):
    st.write(cost_per_estate)
    # Convert DataFrame to CSV format
    csv = df_select.to_csv(index=False).encode('utf-8')
    # Add a download button
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='Estate_sales.csv'
    )

# Pie chart for cost of land by payment type
transact_by_payment_cost = df_select.groupby('PAYMENT TYPE')['cost_of_land'].sum().reset_index()
fig2 = px.pie(
    transact_by_payment_cost,
    names='PAYMENT TYPE',
    values='cost_of_land',
    title='Total Cost of Land by Payment Type',
    labels={'PAYMENT TYPE': 'Payment Type', 'cost_of_land': 'Total Cost of Land'},
    color='PAYMENT TYPE',
    color_discrete_sequence=px.colors.sequential.Cividis
)

# Update layout for better appearance
fig2.update_layout(
    title={'text': 'Total Cost of Land by Payment Type', 'x': 0.5},
    margin=dict(l=0, r=0, t=40, b=0),
    legend_title='Payment Type',
    legend=dict(x=1.05, y=0.5, traceorder='normal'),
    template='plotly_white'
)

# Pie chart for number of transactions by payment type
transact_by_payment_count = df_select.groupby('PAYMENT TYPE').size().reset_index(name='Number of Transactions')
fig3 = px.pie(
    transact_by_payment_count,
    names='PAYMENT TYPE',
    values='Number of Transactions',
    title='Number of Transactions by Payment Type',
    labels={'PAYMENT TYPE': 'Payment Type', 'Number of Transactions': 'Number of Transactions'},
    color='PAYMENT TYPE',
    color_discrete_sequence=px.colors.sequential.speed # Blue color sequence
)

# Update layout for better appearance
fig3.update_layout(
    title={'text': 'Number of Transactions by Payment Type', 'x': 0.5},
    margin=dict(l=0, r=0, t=40, b=0),
    legend_title='Payment Type',
    legend=dict(x=1.05, y=0.5, traceorder='normal'),
    template='plotly_white'
)

# Display the plots in columns
left_col, right_col = st.columns(2)
with left_col:
    st.plotly_chart(fig2)

with right_col:
    st.plotly_chart(fig3)

st.divider()

# Total plots by estate
plots_per_estate = df_select.groupby('Estate')['plot'].sum().sort_values(ascending=False)
fig4 = px.bar(
    plots_per_estate,
    x=plots_per_estate.index,
    y='plot',
    title='Plot of Land per Estate',
    labels={'Estate': 'Estate', 'plot': 'Plot'},
    color='plot',
    color_continuous_scale=color_continuous_scale,  # Blue color scale
    text='plot',  # Display the value on the bars
)

# Update layout for better appearance
fig4.update_layout(
    xaxis_title='Estate',
    yaxis_title='Plot',
    title_font_size=20,
    title_x=0.5,
    xaxis_tickangle=-45,
    margin=dict(l=0, r=0, t=40, b=0),
    template='plotly_white'
)

st.plotly_chart(fig4)

st.divider()

# Group by 'PAYMENT STATUS' and aggregate data
transact_by_payment_status = df_select.groupby('PAYMENT STATUS').agg(
    Number_of_Transactions=('PAYMENT STATUS', 'size'),
    Total_Cost_of_Land=('cost_of_land', 'sum')
).reset_index()

# Create a bar chart
fig5 = px.bar(
    transact_by_payment_status,
    x='PAYMENT STATUS',
    y='Number_of_Transactions',
    title='Payment Status by Total Transactions',
    color='Number_of_Transactions',
    color_discrete_sequence=px.colors.sequential.Electric, # Blue color sequence

    text='Number_of_Transactions',  # Display the value on the bars
    hover_data={'PAYMENT STATUS': True, 'Number_of_Transactions': True, 'Total_Cost_of_Land': True}  # Show additional data on hover
)

# Update layout for better appearance
fig5.update_layout(
    xaxis_title='Payment Status',
    yaxis_title='Total Transactions',
    title_font_size=20,
    title_x=0.5,
    xaxis_tickangle=-45,
    margin=dict(l=0, r=0, t=40, b=0),
    template='plotly_white'
)

# Customize text labels to include commas
fig5.update_traces(
    texttemplate='%{text:,.0f}'  # Format text with commas
)

st.plotly_chart(fig5)
