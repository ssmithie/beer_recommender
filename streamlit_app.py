import streamlit as st
import pandas as pd
import pickle
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pyLDAvis.gensim

def main():
    #st.title("Hello Beer World")
    #st.markdown("Welcome to my beer recommender - simply choose a beer you know you like, and it will give you 3 others that you will enjoy!")
    
    st.sidebar.title("What do you want to do?")
    app_mode = st.sidebar.selectbox("Choose the mode", ["Look at the data", "Find Your Beer's Peer"])

    if app_mode == "Look at the data":
        st.title("Get a feel for the data")
        st.markdown("Choose below to see some insights into the data.")
        with st.spinner('Gathering the data...'):
            run_the_data()

    elif app_mode == "Find Your Beer's Peer":
        st.title("Find your beer's peer")
        st.markdown("Below you can choose from over 40,000 of the top rated beers, and it will return the beers that are the most similar based on the description of the beers.")
        with st.spinner("Fermenting the beers..."):
            run_the_app()


def run_the_data():
    st.subheader('The data at a glance:')

    @st.cache
    def load_full_data(desti):
        data = pd.read_csv(desti, index_col=0)
        return data

    sm_df_full = load_full_data('data_files/top_top_beers.csv')
    stats_df = load_full_data('data_files/stats_df.csv')
    
    st.write("209,508 Unique beers.")
    st.write("7,019,687 Reviews.")
    st.write("118,190 Breweries.")
    st.write("111 Beer Styles.")
    st.write("---")
    st.subheader("Here is a sample of the data:")
    st.dataframe(sm_df_full.sample(10))
    stats_vis = st.checkbox("Look at the descriptive statistics")
    if stats_vis:
        st.dataframe(stats_df.describe())

    
    plt.style.use('seaborn')

    st.subheader("Here are some visualisations of the data:")
    display = st.checkbox("Show the rating distributions")
    if display:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=stats_df['avg_score'], name='Overall Distribution'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'New England IPA']['avg_score'], name='New England IPA'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'American Light Lager']['avg_score'],name='American Light Lager'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'American Stout']['avg_score'], name='American Stout'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'Bohemian Pilsener']['avg_score'], name='Bohemian Pilsener'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'Russian Imperial Stout']['avg_score'],name='Russian Imperial Stout'))
        fig.add_trace(go.Histogram(x=stats_df.loc[stats_df['style'] == 'Belgian Saison']['avg_score'], name='Belgian Saison'))

        # Overlay both histograms
        fig.update_layout(title='Distribution of User Ratings', barmode='overlay')
        # Reduce opacity to see both histograms
        fig.update_traces(opacity=0.7)
        st.plotly_chart(fig)


        #plt.figure()
        #plt.hist(stats_df['avg_score'], bins=18, color='indigo')
        #plt.title("Distribution of User Ratings")
        #st.pyplot()

    pl_display = st.checkbox("Show where the breweries are")
    if pl_display:
        labels = ['US', 'Canada', 'England', 'Germany', 'Belgium', 'Australia', 'Spain', 'RestOfWorld']
        values = [77616, (2235+1734+1578), 4458, 2652, 1881, 1141, 1015, (109508 - (77616+2235+1734+1578+4458+2652+1881+1141+1015))]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig)

    lda_display = st.checkbox("Look at the topic modelling.")
    if lda_display:
        st.markdown("Click [here](file:///Users/sarah/Documents/DataScience/final_project/beer_recommender/lda_vis.html) to check out the interactive graph!", unsafe_allow_html=True)
        
    #hist_data = [stats_df['avg_score'], stats_df['taste_avg'].dropna() , stats_df['look_avg'].dropna(), stats_df['smell_avg'].dropna(), stats_df['feel_avg'].dropna()]
    #groups = ['Overall', 'Taste', 'Look', 'Smell', 'Feel']

    #fig = ff.create_distplot(hist_data, groups, bin_size=[20, 15, 15, 15, 15])
    
    #st.plotly_chart(fig)
    viz_disp = st.checkbox("Look at the topics in the beer reviews")
    if viz_disp:
        st.write("These are the words most commonly used in each of the 12 topics:")
        st.image(['images/topic_0.png','images/topic_1.png','images/topic_2.png','images/topic_3.png','images/topic_4.png','images/topic_5.png','images/topic_6.png','images/topic_7.png','images/topic_8.png','images/topic_9.png','images/topic_10.png','images/topic_11.png'])



def run_the_app():
    st.subheader("Let's get started!")

    @st.cache
    def load_sm_df():
        data = pd.read_csv('data_files/sm_top_beers.csv', index_col=0)
        return data
    
    @st.cache
    def load_full_df():
        data = pd.read_csv('data_files/top_top_beers.csv', index_col=0)
        return data

    with st.spinner("Canning the beer..."):
        sm_df = load_sm_df()

    with st.spinner("Chilling the beer..."):
        sm_df_full = load_full_df()

    #working code
    #flavors = st.radio('Do you want to choose some key words?', ['No', 'Yes'])
    #if filter_by == 'Yes':
    #    beer_location = st.selectbox('Choose a location:', sm_df_full['location'].unique()) 

  
    chosen_brewery = st.selectbox('Choose a brewery:', sm_df_full['brewery'].unique().tolist())
    
    #dropdown:
    desired_beer = st.selectbox('Choose a beer:', sm_df_full.loc[sm_df_full['brewery'] == chosen_brewery]['name'].unique().tolist())
    
    beer_df = sm_df_full[sm_df_full.name == desired_beer]

    topic = int(beer_df[beer_df.brewery == chosen_brewery]['Dominant_Topic'].values[0])
    st.write("Here is a look at the dominant words used to describe your choosen beer:")
    st.image(f'images/topic_{topic}.png')
    st.write(f'Style: {sm_df_full[sm_df_full.name == desired_beer]["style"].values[0]}')
    #if I want to show the df for the beer, uncomment this:
    #st.write(beer_df[beer_df.brewery == chosen_brewery])

    filter_by = st.radio('Do you want to filter by location?', ['No', 'Yes'])
    if filter_by == 'Yes':
        beer_location = st.selectbox('Choose a location:', sm_df_full['location'].unique())

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
                rec_beer_dict['abv'] = sm_df_full.loc[full_ind]['abv']
                rec_beer_dict['avail'] = sm_df_full.loc[full_ind]['avail']
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
                st.write("The stats:")
                st.write(f"Rating: {recommended_beers[i]['Rating']}")
                st.write(f"ABV: {recommended_beers[i]['abv']}")
                st.write(f"Availability: {recommended_beers[i]['avail']}")
                st.write(f"[Click here]({recommended_beers[i]['url']}) to check out the reviews!")
            
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
                rec_beer_dict['abv'] = sm_df_full.loc[full_ind]['abv']
                rec_beer_dict['avail'] = sm_df_full.loc[full_ind]['avail']
                rec_beer_dict['Image'] = sm_df_full.loc[full_ind]['img']
                if sm_df_full.loc[full_ind]['location'] == location:
                    recommended_beers.append(rec_beer_dict)
    
            if len(recommended_beers) > 3:
                for i in range(0,3):
                    st.write(i+1)
                    img_url = recommended_beers[i]['Image']
                    load_image(img_url)
                    st.write(f"{recommended_beers[i]['Beer']} from {recommended_beers[i]['Brewery']} in {recommended_beers[i]['Location']}")
                    st.write("The stats:")
                    st.write(f"Rating: {recommended_beers[i]['Rating']}")
                    st.write(f"ABV: {recommended_beers[i]['abv']}")
                    st.write(f"Availability: {recommended_beers[i]['avail']}")
                    st.write(f"[Click here]({recommended_beers[i]['url']}) to check out the reviews!")
            
            elif len(recommended_beers) >= 1:
                for i in range(len(recommended_beers)):
                    st.write(i+1)
                    img_url = recommended_beers[i]['Image']
                    load_image(img_url)
                    st.write(f"{recommended_beers[i]['Beer']} from {recommended_beers[i]['Brewery']} in {recommended_beers[i]['Location']}")
                    st.write("The stats:")
                    st.write(f"Rating: {recommended_beers[i]['Rating']}")
                    st.write(f"ABV: {recommended_beers[i]['abv']}")
                    st.write(f"Availability: {recommended_beers[i]['avail']}")
                    st.write(f"[Click here]({recommended_beers[i]['url']}) to check out the reviews!")

            
            else:
                st.write("Sorry, there are no similar high rated beers in that location.")

    if st.button("Beer Me!"):
        st.write(full_recommendations())
    else:
        st.image("images/beer_meme.jpeg")
    

if __name__ == "__main__":
    main()


