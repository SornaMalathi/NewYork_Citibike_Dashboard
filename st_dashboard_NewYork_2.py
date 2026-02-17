######################################### City bike - New York Facitility  ####################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import folium
from datetime import datetime as dt
from PIL import Image
import numerize

########################### Initial settings for the dashboard ####################################################

st.set_page_config(page_title = 'City Bike - New york Facitlity - Strategy Dashboard', layout='wide')
st.title('City Bike - New york Facility - Strategy Dashboard')

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Top 20 most popular stations", 
   "Least 20 popular stations",
   "Table with Top & Least popular stations",
   "Weather component and bike usage", 
   "Trip Duration(mins) Vs User Type", 
   "Ride Frequency Vs Hour of the Day Vs Day of the week",
   "Bike Type usage by membership type",
   "Top 50 Routes Member Casual riders", 
   "Conclusions and recommendations"])

########################## Import data        ###################################################################

top_20 = pd.read_csv("New York_Weather_trip_data_Updated_top20.csv")
least_20 = pd.read_csv("New York_Weather_trip_data_Updated_least20.csv")
df_avgtemp = pd.read_csv("New York_Weather_trip_data_Updated_AvgTemp.csv")
df_ridetype = pd.read_csv("New York_ride_type_usage_by_membership_type.csv")
df_peakhour = pd.read_csv("New York_Weather_trip_data_membership_type_ride_count.csv")
df_boxplot = pd.read_csv("NewYork_Weather_trip_data_boxplot_stats.csv")
rides_per_hour_df = pd.read_csv("NewYork_Weather_trip_data_rides_per_hour.csv")
rides_per_day_df = pd.read_csv("NewYork_Weather_trip_data_rides_per_day.csv")

######################################### DEFINE THE PAGES #######################################################

######################### Intro page     #########################################################################

if page == "Intro page":
    
# Load the image
        bikes1 = Image.open('City Bike_New York.jpeg')   #source: https://citibikenyc.com/community-programs/reducedfare

# Create two columns: text on left, image on right
        col1, col2 = st.columns([2, 1])  # 2:1 ratio for more space for text

        with col1:
            st.markdown("#### This dashboard aims to help the business strategy department assess the current logistics model of bike distribution across the city and identify expansion opportunities.")
            st.markdown(" Since the Covid–19 pandemic, New York residents have found even more merit in bike sharing, creating higher demand. This has led to distribution problems—such as fewer bikes at popular bike stations or stations full of docked bikes, making it difficult to return a hired bike—and customer complaints.")
            st.markdown(" For this project, we have used the open source data from the Citi Bike database for the year 2022. To enrich this data set, we have gathered weather data using NOAA’s API service.")
            st.markdown("The objective of this analysis is to conduct a descriptive analysis of existing data and discover actionable insights for the business strategy team to help make informed decisions that will circumvent availability issues and ensure the company’s position as a leader in eco-friendly transportation solutions in the city.")
            st.markdown("The dashboard is separated into 6 sections:")
            st.markdown(" - Station Popularity Analysis")
            st.markdown(" - Weather impact on Bike usage")
            st.markdown(" - Time Based Usage patterns")
            st.markdown(" - Trip Duration Vs User Behaviour")
            st.markdown(" - Route Analysis")
            st.markdown(" - Bike Type Usage")
            st.markdown(" - Conclusions and Recommendations")
            st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")
    
        with col2:
             st.image(bikes1, width=400)  # Adjust width to fit the column

########################### Dual axis line chart page for Weather component & Bike usage #######################
    
elif page == 'Weather component and bike usage':


    season_transitions = df_avgtemp[df_avgtemp['season'] != df_avgtemp['season'].shift(1)]
    transition_dates = season_transitions[['date', 'season']]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df_avgtemp['date'],
            y=df_avgtemp['bike_rides_daily'],
            name='Daily bike rides',
            line=dict(color='steelblue')
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df_avgtemp['date'],
            y=df_avgtemp['avgTemp'],
            name='Daily temperature',
            line=dict(color='firebrick')
        ),
        secondary_y=True
    )

# Title
    fig.update_layout(
        title='Daily Rides and Temperature Over Time'
    )

    fig.update_xaxes(title_text='Date')

    fig.update_yaxes(
        title_text='Number of Bike Rides',
        secondary_y=False
    )

    fig.update_yaxes(
        title_text='Average Temperature (°C)',
        secondary_y=True
    )

    for _, row in transition_dates.iterrows():
        fig.add_shape(
            type="line",
            x0=row['date'],
            x1=row['date'],
            y0=0,
            y1=1,
            xref='x',
            yref='paper',  # 0 to 1 of y-axis (spans entire height)
            line=dict(color='gray', width=1, dash='dash')
        )
        fig.add_annotation(
            x=row['date'],
            y=1.03,  # slightly above the plot
            xref='x',
            yref='paper',
            text=row['season'].capitalize(),
            showarrow=False,
            align='center'
        )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

######################################## Most & Least popular stations ############################################

elif page == "Top 20 most popular stations":

    # Bar chart
    fig = go.Figure(
        go.Bar(
            x=top_20['value'],          
            y=top_20['station'],        
            orientation='h',            
            marker=dict(
                color=top_20['value'],
                colorscale='Blues'
            )
        )
    )

    fig.update_layout(
        title=dict(
            text="Top 20 Most Popular Bike Stations in New York",
            x=0.5,
            xanchor='center'
        ),
        width=1200,
        height=800,
        xaxis_title="Sum of Trips",
        yaxis_title="Station Names",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=250)   # important for long station names
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some stations that are more popular than others(high usage station) - in the top 3 we can see w 21 st & 6 ave, west st & chambers st, broadway & w 58 st. There is a big jump between the highest and lowest bars of the plot.")


elif page == "Least 20 popular stations":
    
    # Bar chart

    fig = go.Figure(
    go.Bar(
        x=least_20['value'],          
        y=least_20['station'],        
        orientation='h',              
        marker=dict(
            color=least_20['value'],
            colorscale='Blues'
        )
    )
)

    fig.update_layout(
        title=dict(
            text="Least 20 Popular Bike Stations in New York",
            x=0.5,
            xanchor='center'
        ),
        width=1200,
        height=800,
        xaxis_title="Sum of Trips",
        yaxis_title="Station Names",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=250)   # important for long station names
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("From the bar chart it is clear that there are some stations that are less popular than others - the last 3 we can see lafayette park, marin light rail, van vorst park. There is a big jump between the most and least popular stations ride frequency values, indicating some clear preferences for the leading stations. The stakeholders can think abt increasing the bike usage in these stations or based on the count just remove the stations to save some logistic cost")

########################   Table with top and least popular stations #############################################

elif page == 'Table with Top & Least popular stations':


# Top 3 high-demand stations
    top3 = top_20[top_20['usage_type'] == 'High Demand'].head(3)

# Least 3 low-demand stations
    least3 = least_20[least_20['usage_type'] == 'Low Demand'].head(3)  # or tail(3) if sorted differently

# Combine
    stations_summary = pd.concat([top3, least3], ignore_index=True)

# Optional: select relevant columns for dashboard
    stations_summary = stations_summary[['station', 'value', 'recommendation']]
    stations_summary.rename(columns={'value': 'total_trips'}, inplace=True)

# If using Streamlit
# import streamlit as st
    st.dataframe(stations_summary)


#####################  Trip Duration(mins) Vs User Type ################################################################

elif page == "Trip Duration(mins) Vs User Type":

# Separate stats
    member_stats = df_boxplot[df_boxplot['user_type'] == 'member'].iloc[0]
    casual_stats = df_boxplot[df_boxplot['user_type'] == 'casual'].iloc[0]

# Determine common y-axis range
    y_min = min(member_stats["lowerfence"], casual_stats["lowerfence"])
    y_max = max(member_stats["upperfence"], casual_stats["upperfence"])

# Create subplots: 1 row, 2 columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Member", "Casual"))

# Member box
    fig.add_trace(go.Box(
        q1=[member_stats["q1"]],
        median=[member_stats["median"]],
        q3=[member_stats["q3"]],
        lowerfence=[member_stats["lowerfence"]],
        upperfence=[member_stats["upperfence"]],
        name="Member",
        marker_color="royalblue",
        boxmean=False,  # hide mean
        showlegend=False
    ), row=1, col=1)

# Add median annotation for Member
    fig.add_annotation(
        x=0,  # first subplot
        y=member_stats["median"],
        text=f"Median: {member_stats['median']:.1f}",
        showarrow=True,
        arrowhead=2,
        row=1,
        col=1
    )

# Casual box
    fig.add_trace(go.Box(
        q1=[casual_stats["q1"]],
        median=[casual_stats["median"]],
        q3=[casual_stats["q3"]],
        lowerfence=[casual_stats["lowerfence"]],
        upperfence=[casual_stats["upperfence"]],
        name="Casual",
        marker_color="red",
        boxmean=False,
        showlegend=False
    ), row=1, col=2)

# Add median annotation for Casual
    fig.add_annotation(
        x=1,  # second subplot
        y=casual_stats["median"],
        text=f"Median: {casual_stats['median']:.1f}",
        showarrow=True,
        arrowhead=2,
        row=1,
        col=2
    )

# Update layout
    fig.update_layout(
        title_text="Trip Duration (Minutes) by User Type",
        template="plotly_white",
        width=1000,
        height=500
    )

# Add axis labels and enforce same y-axis
    fig.update_xaxes(title_text="User Type", row=1, col=1)
    fig.update_xaxes(title_text="User Type", row=1, col=2)
    fig.update_yaxes(title_text="Trip Duration (Minutes)", row=1, col=1, range=[y_min, y_max])
    fig.update_yaxes(title_text="Trip Duration (Minutes)", row=1, col=2, range=[y_min, y_max])


    st.plotly_chart(fig, use_container_width=True)

    st.markdown("The boxplot compares trip duration (in minutes) between member and casual riders. Casual riders tend to take longer trips compared to members.Casual trips vary more (short leisure rides + long sightseeing trips) Members are more consistent. The analysis reveals clear behavioral differences between members and casual riders. Casual users generally take longer and more variable trips, suggesting recreational or leisure usage. In contrast, members exhibit shorter and more consistent trip durations, consistent with commuting behavior. The presence of extreme long-duration outliers, particularly among casual users, further supports the interpretation of leisure-driven usage patterns.")

##################################  Bike Type usage by membership type ############################################

elif page == "Bike Type usage by membership type":

# Reset index so 'member_casual' becomes a column
    df_plotly = df_ridetype.reset_index(drop=True)

# Convert wide to long format for Plotly
    df_long = df_plotly.melt(
        id_vars='member_casual',
        var_name='rideable_type',
        value_name='number_of_rides'
    )

# Define custom colors for each rideable type
    rideable_colors = {
        'classic_bike': 'royalblue',
        'electric_bike': 'orange'
}

# Create Plotly bar chart with custom colors
    fig = px.bar(
        df_long,
        x='member_casual',
        y='number_of_rides',
        color='rideable_type',
        barmode='group',  # side-by-side bars
        labels={
            'member_casual': 'Membership Type',
            'number_of_rides': 'Number of Rides',
            'rideable_type': 'Ride Type'
        },
        title='Ride Type Usage by Membership Type',
        color_discrete_map=rideable_colors  # Apply custom colors
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("The chart shows the distribution of ride types across membership types. The x-axis represents the membership type (Member vs Casual), while the grouped bars show the number of rides for each rideable type (classic_bike, electric_bike). Classic bikes are the most popular across all users, with members taking significantly more rides than casuals. Fleet management should prioritize classic bikes for members while promoting electric bikes to casual riders to balance usage and improve overall service efficiency.")


##############################   Top 50 Routes Member/Casual riders ###################################################

elif page == "Top 50 Routes Member Casual riders": 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York - Member/Casual riders")

    path_to_html = "member_casual_top_50_routes.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Top 50 popular Bike Trip routes in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("The name of the stations can be seen by hovering over the map. The Map shows the top 50 frequent routes in New York, identified by the membership type. Most of the popular routes are done by members. The top 5 routes are bewteen 'W 21 St & 6 Ave-9 Ave & W 22 St, 1 Ave & E 62 St-1 Ave & E 68 St, Norfolk St & Broome St-Henry St & Grand St, North Moore St & Greenwich St-Vesey St & Church St, Henry St & Grand St-Norfolk St & Broome St. Operations should focus on ensuring availability, maintaining bikes, and considering promotions to encourage casual rider adoption on these popular routes")

##########################  Ride Frequency Vs Hour of the Day Vs Day of the week ###############################

elif page == "Ride Frequency Vs Hour of the Day Vs Day of the week":
    # Ensure correct day order
    day_order = ["Monday", "Tuesday", "Wednesday", 
                 "Thursday", "Friday", "Saturday", "Sunday"]

    rides_per_day_df['day_of_week'] = pd.Categorical(
        rides_per_day_df['day_of_week'],
        categories=day_order,
        ordered=True
    )
    
    rides_per_day_df = rides_per_day_df.sort_values('day_of_week')

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Ride Frequency by Hour (with Membership)",
                        "Ride Frequency by Day"),
        specs=[[{"secondary_y": True}, {}]]
    )

    fig.add_trace(
        go.Bar(
            x=rides_per_hour_df['ride_hour'],
            y=rides_per_hour_df['total_rides'],
            name="Total Rides",
            marker_color="steelblue"   # BLUE bars
        ),
        row=1, col=1,
        secondary_y=False
    )
    
    for member_type in df_peakhour['member_casual'].unique():
        subset = df_peakhour[df_peakhour['member_casual'] == member_type]
        
        fig.add_trace(
            go.Scatter(
                x=subset['ride_hour'],
                y=subset['total_rides'],
                mode='lines+markers',
                name=member_type
            ),
            row=1, col=1,
            secondary_y=True
        )
    
    fig.update_xaxes(title_text="Hour of Day", row=1, col=1)
    fig.update_yaxes(title_text="Total Rides (All Users)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Rides by Membership Type", row=1, col=1, secondary_y=True)

    fig.add_trace(
        go.Bar(
            x=rides_per_day_df['day_of_week'],
            y=rides_per_day_df['total_rides'],
            name="Daily Total",
            marker_color="steelblue"
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Day of Week", row=1, col=2)
    fig.update_yaxes(title_text="Total Rides", row=1, col=2)
    
    fig.update_layout(
        height=500,
        width=1100,
        template="plotly_white",
        title_text="Ride Frequency Analysis Dashboard"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The left plot shows how the rides are distributed across the day, along with the ride behaviour of members and casual riders and the right plot shows how its distributed across a week. The dashboard shows that bike rides are concentrated during certain hours and days, likely corresponding to commuting patterns. The line chart illustrates the distribution of bike rides across different hours of the day for members and casual users. Clear morning peak from 7-9AM and evening peak 4-6PM and lower activity overnight.Members show strong commuting patterns, with pronounced peaks during typical work commute hours.Casual riders tend to ride more during leisure hours rather than commuting hours. Operations can be optimized by reallocating bikes during peak times, expanding capacity at busy stations, and promoting off-peak usage to balance demand")

###################################################################################################################

else:

# Load the image
    bikes = Image.open("New York_bike_image.jpeg")  

# Create two columns: text on left, image on right
    col1, col2 = st.columns([2, 1])  # 2:1 ratio for more space for text

    with col1:
        st.header("Conclusions")
    
        st.markdown("""
#### Ride Patterns by Hour and Day
- Peak usage occurs during **weekday commute hours**, while weekends have lower ridership.
- **Members dominate weekday usage**; casual riders are more active on weekends.

#### Weather Impact
- Bike ridership demonstrates clear seasonal patterns and appears positively correlated with temperature. 
- Demand peaks during warmer seasons and declines in colder months, indicating strong weather sensitivity.

#### Ride Duration (Boxplots)
- Members tend to take **short, consistent trips**, while casual users show **more variability and longer trips**.
- **Median trip duration** for members is lower than casual riders.

#### Ride Type Usage
- **Classic bikes** are the most used ride type for both members and casuals.
- Members take **more rides overall** than casual users.

#### Popular Routes
- The **top 50 most frequent routes** are mostly used by members, suggesting heavy commuter usage.
- Casual riders use these routes less frequently, indicating **recreational or occasional usage**.
""")

    st.header("Recommendations")
    st.markdown("""
#### Operation Planning 
- Increase availability of the bikes in warm months. 
- Consider offering discounted winter membership, reducing cold-weather incentives, offering seasonal passes etc.
- High-demand stations may run out of bikes quickly. Plan frequent rebalancing from lower-demand stations.
- For top stations, consider adding more docks or bikes to meet demand.
- Work with local communities to understand why usage is low and promote cycling in those neighborhoods. If stations consistently underperform, consider merging them with nearby stations to optimize coverage.
- Members mostly take short, regular trips, typical for commuting, while casual users take longer, more variable trips, likely for leisure. Operations, promotions, and bike allocation should reflect these usage patterns.

#### Fleet & Station Management
- Ensure **sufficient classic bikes** at high-demand stations.
- Maintain **electric bikes** for casual users, particularly in tourist or recreational areas.
- **Expand dock capacity** along high-traffic routes.
- Encourage casual riders to try electric bikes through promotions or discounts, helping balance bike usage.

#### Maintenance
- Prioritize **maintenance on high-use bikes and routes**.
- Schedule maintenance during **low-demand hours** to minimize disruptions.

#### Marketing & Promotions
- Promote **electric bikes** to casual riders to balance usage.
- Encourage **off-peak usage** with discounts or incentives.
- Highlight **popular routes** to boost membership adoption among commuters.

""")

    with col2:
#    st.image(bikes, use_column_width=True)
         st.image(bikes, width=400)  # Adjust width to fit the column

##############################################################################################################
