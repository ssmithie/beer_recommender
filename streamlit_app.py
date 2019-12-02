import streamlit as st
import pandas as pd
import pickle
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import math


def main():
    st.title("Hello Beer World")
    st.markdown("Welcome to my beer recommender - simply choose a beer you know you like, and it will give you 3 others that you will enjoy!")
    
    st.sidebar.title("What do you want to do?")
    app_mode = st.sidebar.selectbox("Choose the mode", ["Look at the data!", "Run the app"])

    if app_mode == "Look at the data!":
        with st.spinner('Gathering the data...'):
            run_the_data()

    elif app_mode == "Run the app":
        with st.spinner("Fermenting the beers..."):
            run_the_app()


def run_the_data():
    st.subheader('The data at a glance')

    @st.cache
    def load_full_data():
        data = pd.read_csv('data_files/top_beers.csv', index_col=0)
        return data

    sm_df_full = load_full_data()

    st.write(sm_df_full.sample(10))



def run_the_app():
    st.subheader("Let's get started!")

    @st.cache
    def load_sm_df():
        data = pd.read_csv('data_files/sm_top_beers.csv', index_col=0)
        return data
    
    @st.cache
    def load_full_df():
        data = pd.read_csv('data_files/top_beers.csv', index_col=0)
        return data

    with st.spinner("Canning the beer..."):
        sm_df = load_sm_df()

    with st.spinner("Chilling the beer..."):
        sm_df_full = load_full_df()

    #working code
    #flavors = st.radio('Do you want to choose some key words?', ['No', 'Yes'])
    #if filter_by == 'Yes':
    #    beer_location = st.selectbox('Choose a location:', sm_df_full['location'].unique()) 

    desired_beer = st.selectbox('Choose a beer:', sm_df_full['name'].unique().tolist())
    st.write(sm_df_full[sm_df_full.name == desired_beer])

    filter_by = st.radio('Do you want to filter by location?', ['No', 'Yes'])
    if filter_by == 'Yes':
        beer_location = st.selectbox('Choose a location:', sm_df_full['location'].unique())

#st.subheader("This is a different option")

#chosen_beer = st.text_input("Tell me a beer:", 'your beer here')

    @st.cache
    def load_matrix():
        cosine_sim = np.load('cosine_sim.npy')
        return cosine_sim

    cosine_sim = load_matrix()


    indices = pd.Series(sm_df.index)

    def load_image(url):
        if type(url) == str:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                st.image(img)
            except:
               None 

    
    def full_recommendations(cosine_sim = cosine_sim):
        title = desired_beer
        if filter_by == 'Yes':
            location = beer_location
        # initializing the empty list of recommended beers
        recommended_beers = []
    
        # gettin the index of the beer that matches the name
        idx = indices[indices == title].index[0]

        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        # getting the indexes of the 100 most similar beers
        top_20_indexes = list(score_series.iloc[1:100].index)
    
        # populating the list with the titles of the best 10 matching beers
    
    
        if filter_by == 'No':
        
            for i in top_20_indexes:
                rec_beer_dict = {}
                full_ind = sm_df_full.index[sm_df_full['name'] == list(sm_df.index)[i]].tolist()[0]
                rec_beer_dict['Beer'] = list(sm_df.index)[i]
                rec_beer_dict['Brewery'] = sm_df_full.loc[full_ind]['brewery']
                rec_beer_dict['Location'] = sm_df_full.loc[full_ind]['location']
                rec_beer_dict['Rating'] = sm_df_full.loc[full_ind]['avg_score']
                rec_beer_dict['url'] = sm_df_full.loc[full_ind]['url']
                #if not sm_df_full.loc[full_ind]['img'] == None:
                rec_beer_dict['Image'] = sm_df_full.loc[full_ind]['img']
                #else:
                    #rec_beer_dict['Image'] = 'no'

                recommended_beers.append(rec_beer_dict)
            st.write("These are the beers you should check out:")
            for i in range(0,3):
                st.write(i+1)
                img_url = recommended_beers[i]['Image']
                load_image(img_url)
                st.write(f"{recommended_beers[i]['Beer']} from {recommended_beers[i]['Brewery']} in {recommended_beers[i]['Location']}")
                st.write(f"It has a rating of {recommended_beers[i]['Rating']}")
                st.markdown(f"[Click here]({recommended_beers[i]['url']}) to check out the reviews!")
            
            #return recommended_beers[:3]
    
        elif filter_by == 'Yes':
            for i in top_20_indexes:
                rec_beer_dict = {}
                full_ind = sm_df_full.index[sm_df_full['name'] == list(sm_df.index)[i]].tolist()[0]
                rec_beer_dict['Beer'] = list(sm_df.index)[i]
                rec_beer_dict['Brewery'] = sm_df_full.loc[full_ind]['brewery']
                rec_beer_dict['Location'] = sm_df_full.loc[full_ind]['location']
                rec_beer_dict['Rating'] = sm_df_full.loc[full_ind]['avg_score']
                rec_beer_dict['url'] = sm_df_full.loc[full_ind]['url']
                rec_beer_dict['Image'] = sm_df_full.loc[full_ind]['img']
                if sm_df_full.loc[full_ind]['location'] == location:
                    recommended_beers.append(rec_beer_dict)
    
            if len(recommended_beers) >= 1:
                for i in range(len(recommended_beers)):
                    st.write(i+1)
                    img_url = recommended_beers[i]['Image']
                    load_image(img_url)
                    st.write(f"{recommended_beers[i]['Beer']} from {recommended_beers[i]['Brewery']} in {recommended_beers[i]['Location']}")
                    st.write(f"It has a rating of {recommended_beers[i]['Rating']}")
                    st.markdown(f"[Click here]({recommended_beers[i]['url']}) to check out the reviews!")
            else:
                st.write("Sorry, there are no similar high rated beers in that country")

    st.write(full_recommendations())

if __name__ == "__main__":
    main()


