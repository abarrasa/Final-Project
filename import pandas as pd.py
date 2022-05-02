import pandas as pd
from modules import m_acquisition as mac
from modules import m_analisys as man
from modules import m_reporting as mre
from modules import m_wrangling as mwr
import streamlit as st
import warnings


plot=['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']
select = ['Happy', 'Booster', 'Sad', 'Relax', 'Motivation', 'Energy','Dancing', 'Drive', 'Mix','Own']

st.set_page_config(
     page_title="Spotify recommender",
     page_icon=":musical_note:",
     layout="wide",
     initial_sidebar_state="expanded",
 )

#Definir el título

col1, col2, col3 = st.columns([2,4,1])
col1.write("")
col2.image("./Images/image/Logo.png",width=530) 
col3.write("")

col1, col2, col3 = st.columns(3)
col1.write("")
col2.title('Spotify recommender')
col3.write("")

col1, col2, col3 = st.columns(3)
col1.write("")
col2.caption('This is a project that I recommend songs based on moods or after songs.')
col3.write("")

for i in range(5):
    st.write("")
feel_1 = st.container()
for i in range(1):
    st.write("") 
feel_2 = st.container()


with feel_1:
    col1, col2, col3, col4, col5 = st.columns([2,2,3,2,2])
    col1.write("")
    col3.subheader("How do you feel today? ") 
    col3.write("")


with feel_2:
    col1, col2, col3, col4, col5 = st.columns([2,1,3,2,2])
    col1.image('./Images/image/12.jpg')
    col1.image('./Images/image/8.jpg')
    col1.image('./Images/image/4.jpg')
    col2.image('./Images/image/11.jpg')
    col2.image('./Images/image/7.jpg')
    col2.image('./Images/image/3.jpg')
    feeling = col3.selectbox(" ",('Happy', 'Booster', 'Sad', 'Relax', 'Drama', 'Motivation', 'Energy', 'Dancing', 'Mix', 'Own'))
    col4.image('./Images/image/10.jpg')
    col4.image('./Images/image/6.jpg')
    col4.image('./Images/image/2.jpg')
    col5.image('./Images/image/9.jpg')
    col5.image('./Images/image/5.jpg')
    col5.image('./Images/image/1.jpg')

    if feeling == 'Own':
        track=col3.text_input('Enter track', value="", key='text_value')
        artist=col3.text_input('Enter artist', value="", key='text_value')
    col3.write("")
    playlist_name=col3.text_input("Please choose the name of your new playlist:")
    if col3.button('Ready!'):
        run = 'yes'
    else:
        run = 'no'


    if run == 'no':
        st.write('')

    else:
        if __name__ == '__main__':
        
            data_songs = mac.import_data()
            if feeling == 'Own':
                track_id = mac.sp.search(q='artist:' + artist + ' track:' + track, type='track')
                ID = pd.DataFrame([track_id['tracks']['items'][0]['id']])
                ID=ID.iloc[0][0]
            elif feeling == 'Happy':
                songs = mac.get_id_songs('37i9dQZF1DXdPec7aLTmlC')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Booster':
                songs = mac.get_id_songs('37i9dQZF1DX3rxVfibe1L0')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Sad':
                songs = mac.get_id_songs('37i9dQZF1DWZqdNJSufucb')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Relax':
                songs = mac.get_id_songs('37i9dQZF1DWVIzZt2GAU4X')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Motivation':
                songs = mac.get_id_songs('37i9dQZF1DXdxcBWuJkbcy')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Energy':
                songs = mac.get_id_songs('37i9dQZF1DWYp5sAHdz27Y')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Mix':
                songs = mac.get_id_songs('37i9dQZEVXcOx8nqzmzXjg')
                ID = mwr.selectRandom(songs)
            elif feeling == 'Dancing':
                songs = mac.get_id_songs('37i9dQZF1DWSX4baQVDQut')
                ID = mwr.selectRandom(songs)

            df_features= mac.song_features(ID)
            df_features_clean = mwr.clean_df_features(df_features)
            data_songs = mwr.drop_duplicates(df_features_clean,data_songs)
            df_mix = mwr.concatenate(data_songs, df_features)
            df_mix_no_null=mwr.delete_nulls(df_mix)
            df_mix_scaled = man.scaler(df_mix_no_null)
            normalized_data_songs=man.normalization(df_mix_scaled)
            cos_sim = man.cosine_similarity(normalized_data_songs)
            cos_sim_df = man.df(cos_sim)
            songs_ponderate = man.concat(df_mix,cos_sim_df)
            similar_song = man.prepare_dataframe(songs_ponderate)
            best_tracks=mre.select_songs(similar_song)
            tracks=mre.prepare_tracks(best_tracks)
            playlist_id=mre.create_playlist(playlist_name)
            mre.cover_playlist(playlist_id)
            mre.add_tracks(playlist_id, tracks)
            col3.write(f"Your new playlist called '{playlist_name}' is ready. Enjoy it!")
            col3.write(f"[Click here to go](https://open.spotify.com/playlist/{playlist_id})")