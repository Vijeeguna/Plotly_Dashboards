# Reference: https://www.statworx.com/de/blog/plotly-an-interactive-charting-library/?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com
# Data Source: https://bikeshare.metro.net/about/data/

import pandas as pd
import plotly.graph_objs as go
import chart_studio.plotly as py
import plotly.figure_factory as ff

#read file
rental = pd.read_csv('metro-bike-share-trip-data.csv')
rental['Start Time'] = pd.to_datetime(rental['Start Time'])
rental['Start_Date'] = rental['Start Time'].dt.date
# Size includes NaN values
# count does not include NaN values
# choose appropriately
py.sign_in(username='VijeeGuna', api_key='phJU9PB8c41agc5Xoxsm')
rental_count = rental.groupby(["Start_Date", "Passholder_Type"]).size().reset_index(name ="Total_Count")
trace1 = go.Scatter(
    x = rental_count.query('Passholder_Type == "Flex Pass"').Start_Date,
    y = rental_count.query('Passholder_Type == "Flex Pass"').Total_Count,
    name = 'Flex Pass',
    mode = 'lines',
    line = dict(color='red')
)
trace2 = go.Scatter(
    x = rental_count.query('Passholder_Type == "Monthly Pass"').Start_Date,
    y = rental_count.query('Passholder_Type == "Monthly Pass"').Total_Count,
    name = 'Monthly Pass',
    mode = 'lines',
    line = dict(color='blue')
)
trace3 = go.Scatter(
    x = rental_count.query('Passholder_Type == "Walk-up"').Start_Date,
    y =rental_count.query('Passholder_Type == "Walk-up"').Total_Count,
    mode = 'lines',
    name = 'Walk-up',
    line = dict(color = 'green')
)
data = [trace1, trace2, trace3]
layout = go.Layout(title="Number of rented bikes over time",
                   yaxis=dict(title="Number of rented bikes",
                              zeroline=False),
                   xaxis=dict(title="Date",
                              zeroline = False)
)
py.plot(data, auto_open=True, filename='LA Bike Share')

# Pie chart
share = rental.groupby("Passholder_Type").sum().reset_index()
print(share.columns)
trace4 = go.Pie(labels=share.Passholder_Type,
       values=share.Duration,
       hoverinfo = 'label+percent',
       marker = dict(colors = ['grey','blue','green', 'orange'],
                     line = dict(color='white', width=2)))

go.Figure(data = [trace4])
py.plot([trace4], auto_open=True, filename='Bike Rental Pie Chart')

# Distribution plot

mean =rental.groupby(["Start_Date", "Passholder_Type"])['Duration'].mean().reset_index()
hist = [mean.query('Passholder_Type == "Flex Pass"').Duration,
             mean.query('Passholder_Type == "Monthly Pass"').Duration,
             mean.query('Passholder_Type == "Walk-up"').Duration]
labels = ['Flex Pass', 'Monthly Pass', 'Walk-up']
text = [mean.query('Passholder_Type == "Flex Pass"').Start_Date,
             mean.query('Passholder_Type == "Monthly Pass"').Start_Date,
             mean.query('Passholder_Type == "Walk-up"').Start_Date]
fig = ff.create_distplot(hist,
                   group_labels= labels,
                   rug_text= text,
                    show_hist= False,
                   colors = ['red', 'blue', 'green'])
py.plot(fig, auto_open=True, filename='Bike Rental Duration Distribution Plot')

# Bar Chart
trip_route = rental.groupby(['Trip_Route_Category', 'Passholder_Type']).size().reset_index(name='Total')
bar1 = go.Bar(
    x = trip_route.query('Passholder_Type == "Flex Pass"').Trip_Route_Category,
    y = trip_route.query('Passholder_Type == "Flex Pass"').Total,
    name = 'Flex Pass',
    marker = dict(color='red')
)
bar2 = go.Bar(
    x = trip_route.query('Passholder_Type == "Monthly Pass"').Trip_Route_Category,
    y = trip_route.query('Passholder_Type == "Monthly Pass"').Total,
    name = 'Monthly Pass',
    marker = dict(color='blue')
)
bar3 = go.Bar(
    x = trip_route.query('Passholder_Type == "Walk-up"').Trip_Route_Category,
    y = trip_route.query('Passholder_Type == "Walk-up"').Total,
    name = 'Walk-up',
    marker = dict(color='green')
)
fig_bar = go.Figure(data = [bar1, bar2, bar3], layout = dict(barmode = 'stack'))
py.plot(fig_bar, auto_open=True, filename='Bike Rental - Stacked Bar Chart')
