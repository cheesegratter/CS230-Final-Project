"""Name: Mark Marget
CS230: Section 6
Data: NCAA Football Stadiums

Description:
This program uses the matplotlib, streamlit, and pandas imports to visualize many aspects of the provied csv file into a
comprehensive webiste. Pandas and matplotlib are used to analyse the csv file and display it as a graph (respectivley) while
streamlit is used to display it on a website. Shapely and geopandas are used to display the mapped stadiums. Beyond the textbook
and handouts, I referrenced StackOverflow, a towardsdatasciene article, W3Schools, and GeeksforGeeks.
"""

#imports the six modules
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

#returns the capacities of NCAA state stadiums given the two letter identifier and full name along with displaying a bar graph
#comparing the various stadiums in the state 

#univeral state abreviation to full name converter, this became neccesary due to its requirment in the main() and stateCapacity() functions
stateFull = {'AL': "Alabama", 'AR': "Arkansas", 'AZ' : "Arizona", 'CA' : "California", 'CO' : "Colorado", 'CT' : "Connecticut", 'DE' : "Delaware",
                 'FL' : "Florida", 'GA' : "Georgia",'HI' : "Hawaii", 'IA' : "Iowa", 'ID' : "Idaho", 'IL' : "Illinois", 'IN' : "Indiana", 'KS' : "Kansas", 'KY' : "Kentucky",
                 'LA' : "Louisiana", 'MA' : "Massachusetts", 'MD' : "Maryland", 'ME' : "Maine",'MI' : "Michigan", 'MN' : "Minnesota", 'MO' : "Missouri", 'MS' : "Mississippi",
                 'MT' : "Montana", 'NC' : "North Carolina", 'ND' : "North Dakota", 'NE' : "Nebraska", 'NH' : "New Hampshire", 'NJ' : "New Jersey", 'NM' : "New Mexico",'NV' : "Nevada",
                 'NY' : "New York", 'OH' : "Ohio", 'OK' : "Oklahoma", 'OR' : "Oregon", 'PA' : "Pennsylvania", 'RI' : "Rhode Island", 'SC' : "South Carolina", 'SD' : "South Dakota",
                 'TN' : "Tennessee", 'TX' : "Texas",'UT' : "Utah", 'VA' : "Virgina", 'WA' : "Washington", 'WI' : "Wisconsin", 'WV' : "West Virgina", 'WY' : "Wyoming"}

#returns the capacities of NCAA state stadiums given the two letter identifier and full name along with displaying a bar graph
#comparing the various stadiums in the state
def stateCapacity(state="PA", stateName = "Pennsylvania"):
    df = pd.read_csv("stadiums-geocoded.csv", index_col = "state")
    #sorts stadiums in state in decending order by capacity
    df.sort_index()
    capacityByState = df[("capacity")]
    #includes states with both the abreviation and name
    #for example: Pennsylvania takes values with both "PA" and "Pennsylvania" as its state name
    capacityOfState = capacityByState.get([state, stateFull[state]])
    #a neat system I made to detect only one stadium as the try: command had difficulties working with the combined modules which I found interesting
    #this qualifies as data filtering
    if capacityOfState is None:
        st.subheader("Only one stadium, no comparisons can be made.")
        return
    ser = df["stadium"]
    stadium = ser.get([state, stateFull[state]])
    plt.figure()
    plt.title("Stadium Capacity For " + stateName)
    plt.xlabel("Stadium")
    plt.rc('xtick', labelsize=5)
    plt.ylabel("Capacity")
    plt.legend()
    plt.bar(stadium, capacityOfState)
    st.pyplot(plt.show())
    return stadium, capacityOfState

#displays a bar graph of the average capacity for a stadium in each conference
def conferenceComparison():
    df = pd.read_csv("stadiums-geocoded.csv", index_col = "conference")
    #sorts all of the conferences in decending order by capacity
    df = df.sort_values(by='capacity',ascending=False)
    capacityByConference = df[("capacity")]
    plt.figure()
    plt.bar(capacityByConference.index, capacityByConference)
    plt.title("Capacity by Conference")
    plt.xlabel("Conference")
    plt.ylabel("Capacity")
    plt.legend()
    st.pyplot(plt.show())

#displays a map of the earth with all of the stadiums mapped out
def mapOfConferences(earth):
    df = pd.read_csv("stadiums-geocoded.csv", delimiter=',', skiprows=0, low_memory=False)
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = GeoDataFrame(df, geometry=geometry)   
    world = gpd.read_file(gpd.datasets.get_path(earth))
    gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15);
    st.pyplot(plt.show())

#the main function which calls all of the others and generally takes care of displaying to the streamlit site
def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Comparing NCAA Capacities")
    st.header("Stadium Capacities")
    stateAbr = "PA"
    stateAbr = st.selectbox('Pick a State', ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA','HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
                                              'ME','MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM','NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                                              'SD', 'TN', 'TX','UT', 'VA', 'WA', 'WI', 'WV', 'WY'])  
    stateCapacity(stateAbr, stateFull[stateAbr])
    st.header("Conference Capacities")
    conferenceComparison()
    st.header("NCAA Stadiums on a World Map")
    showMap = st.checkbox('Cities Only')
    if showMap:
        mapOfConferences('naturalearth_cities')
    else:
        mapOfConferences('naturalearth_lowres')
    f = open("likes.txt", "r")
    currentLikes = int(f.read())
    f.close()
    if st.button('Like'):
        f = open("likes.txt", "r")
        currentLikes = str(int(f.read())+1)
        f.close()
        f = open("likes.txt", "w")
        f.write(currentLikes)
        f.close()
    st.subheader("Total Likes: " + str(currentLikes))

#calls the main function
main()