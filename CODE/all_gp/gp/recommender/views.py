from django.shortcuts import render
from io import BytesIO
from keras.models import model_from_json
from keras.preprocessing import image
import cv2
import base64
from PIL import Image
import re
import numpy as np
import pandas as pd
import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#from .models import Analysis
from songs.models import Song
from .models import Analysis

## LOADING THE MODEL

emotion_classifier = model_from_json(open("C:\\Users\\dialajubeh\\Documents\\all_gp\\gp\\models\\model.json", "r").read())

## LOAD THE MODEL'S WEIGHTS
emotion_classifier.load_weights("C:\\Users\\dialajubeh\\Documents\\all_gp\\gp\\models\\model.h5")

facehaarcascade = cv2.CascadeClassifier("C:\\Users\\dialajubeh\\Documents\\all_gp\\gp\\models\\haarcascade_frontalface_default.xml")
emotion_val = None
def index(request):
    context={'a':1}
    return render(request, 'recommender/in.html', context)

def predictImage(request):
    if request.POST.get('captured_image'):
        captured_image = request.POST.get('captured_image')
        datauri = captured_image
        image_data = re.sub("^data:image/png;base64,", "", datauri)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        im = Image.open(image_data)
        path = "media\\temporary_file.png"
        l = im.save(path)
        gray_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        faces_detected = facehaarcascade.detectMultiScale(gray_img, 1.32, 5)
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(gray_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
            roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            predictions = emotion_classifier.predict(img_pixels)
            # find max indexed array
            max_index = np.argmax(predictions[0])
            emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]
            global emotion_val
            analysis_obj = Analysis(user=request.user,emotion= predicted_emotion)
            analysis_obj.save()
            def emotion_val():
                return predicted_emotion
            if os.path.exists("media\\temporary_file.png"):
                os.remove("media\\temporary_file.png")
            context = {'predicted_emotion': predicted_emotion}
            return render(request, 'recommender/in.html', context)


def song_playing(request):
    if request.method=='POST':
        spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id='ad0693d36aca48fb969dbc408be48279',
                                                                client_secret='15b4999d9a30416bb48795614171172f', ))
        calm_dataframe = pd.read_csv("calm0.csv")
        positive_dataframe = pd.read_csv("positive0.csv")
        low_mood_dataframe = pd.read_csv("low-mood0.csv")
        tough_dataframe = pd.read_csv("tough0.csv")
        calm_df = pd.read_csv("calm0.csv")
        calm_df["id"]=calm_df["id"].astype('|S')
        positive_df = pd.read_csv("positive0.csv")
        positive_df["id"]=positive_df["id"].astype('|S')
        tough_df = pd.read_csv("tough0.csv")
        tough_df["id"]=tough_df["id"].astype('|S')
        low_mood_df = pd.read_csv("low-mood0.csv")
        low_mood_df["id"] =low_mood_df["id"].astype('|S')

        emotion = emotion_val()

        if emotion=="neutral":
            calm_s = calm_df['id'].sample(1)
            id_pre = calm_s.to_string()
            id= id_pre[-23:-1]

            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name= song_detail["name"]
            song_instance = Song(song_name= song_name,songid = id,song_cat= "calm")
            song_instance.save()
            song_instance_id=song_instance.id



            popularity = calm_dataframe.loc[calm_dataframe['id'] == id].popularity
            popularity= popularity.to_string()[8:]

            danceability = calm_dataframe.loc[calm_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = calm_dataframe.loc[calm_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = calm_dataframe.loc[calm_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]

            calm_s_1 = calm_df['id'].sample(1)
            id_pre_1 = calm_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/"+id1)


            calm_s_2 = calm_df['id'].sample(1)
            id_pre_2 = calm_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/"+id2)


            calm_s_3 = calm_df['id'].sample(1)
            id_pre_3 = calm_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/"+id3)

            print(song_instance_id)
            return render(request, 'recommender/song_playing.html', {"result":result, "song_name":song_name, "danceability":danceability,
                                                                   "acousticness":acousticness,
                                                                   "release_date":release_date,"popularity":popularity,"extra_song_1":extra_song_1,
                                                                   "extra_song_2": extra_song_2,"extra_song_3":extra_song_3,
                                                                     "extra_song_1_result":extra_song_1_result, "extra_song_2_result":extra_song_2_result,
                                                                     "extra_song_3_result":extra_song_3_result, "song_instance_id":int(song_instance_id)})

        if emotion == "happy":
            positive_s = positive_df['id'].sample(1)
            id_pre = positive_s.to_string()
            id = id_pre[-23:-1]
            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]
            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = positive_dataframe.loc[positive_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = positive_dataframe.loc[positive_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = positive_dataframe.loc[positive_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = positive_dataframe.loc[positive_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]

            positive_s_1 = positive_df['id'].sample(1)
            id_pre_1 = positive_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/" + id1)

            positive_s_2 = calm_df['id'].sample(1)
            id_pre_2 = positive_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/" + id2)

            positive_s_3 = calm_df['id'].sample(1)
            id_pre_3 = positive_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/" + id3)

            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness, "release_date": release_date,
                           "popularity": popularity,"extra_song_1":extra_song_1,
                                                                   "extra_song_2": extra_song_2,"extra_song_3":extra_song_3,
                                                                   "extra_song_1_result":extra_song_1_result,"extra_song_2_result":extra_song_2_result,
                                                                   "extra_song_3_result":extra_song_3_result, "song_instance_id":int(song_instance_id)})

        if emotion == "sad":
            low_mood_s = low_mood_df['id'].sample(1)
            id_pre = low_mood_s.to_string()
            id = id_pre[-23:-1]
            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]
            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = low_mood_dataframe.loc[low_mood_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = low_mood_dataframe.loc[low_mood_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = low_mood_dataframe.loc[low_mood_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = low_mood_dataframe.loc[low_mood_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]


            low_mood_s_1 = calm_df['id'].sample(1)
            id_pre_1 = low_mood_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/"+id1)

            low_mood_s_2 = calm_df['id'].sample(1)
            id_pre_2 = low_mood_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/"+id2)

            low_mood_s_3 = calm_df['id'].sample(1)
            id_pre_3 = low_mood_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/"+id3)



            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness,"release_date": release_date,
                           "popularity": popularity
                              , "extra_song_1": extra_song_1,
                           "extra_song_2": extra_song_2, "extra_song_3": extra_song_3,
                           "extra_song_1_result": extra_song_1_result, "extra_song_2_result": extra_song_2_result,
                           "extra_song_3_result": extra_song_3_result, "song_instance_id":int(song_instance_id)})

        if emotion == "disgust":
            positive_s = positive_df['id'].sample(1)
            id_pre = positive_s.to_string()
            id = id_pre[-23:-1]

            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]
            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = positive_dataframe.loc[positive_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = positive_dataframe.loc[positive_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = positive_dataframe.loc[positive_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = positive_dataframe.loc[positive_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]

            positive_s_1 = positive_df['id'].sample(1)
            id_pre_1 = positive_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/" + id1)

            positive_s_2 = calm_df['id'].sample(1)
            id_pre_2 = positive_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/" + id2)

            positive_s_3 = calm_df['id'].sample(1)
            id_pre_3 = positive_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/" + id3)


            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness, "release_date": release_date,
                           "popularity": popularity
                              , "extra_song_1": extra_song_1,
                           "extra_song_2": extra_song_2, "extra_song_3": extra_song_3,
                           "extra_song_1_result": extra_song_1_result, "extra_song_2_result": extra_song_2_result,
                           "extra_song_3_result": extra_song_3_result, "song_instance_id":int(song_instance_id)})
        if emotion == "fear":
            calm_s = calm_df['id'].sample(1)
            id_pre = calm_s.to_string()
            id = id_pre[-23:-1]
            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]

            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = calm_dataframe.loc[calm_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = calm_dataframe.loc[calm_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = calm_dataframe.loc[calm_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = calm_dataframe.loc[calm_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]


            calm_s_1 = calm_df['id'].sample(1)
            id_pre_1 = calm_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/"+id1)



            calm_s_2 = calm_df['id'].sample(1)
            id_pre_2 = calm_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/"+id2)



            calm_s_3 = calm_df['id'].sample(1)
            id_pre_3 = calm_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/"+id3)


            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness, "release_date": release_date,
                           "popularity": popularity
                              , "extra_song_1": extra_song_1,
                           "extra_song_2": extra_song_2, "extra_song_3": extra_song_3,
                           "extra_song_1_result": extra_song_1_result, "extra_song_2_result": extra_song_2_result,
                           "extra_song_3_result": extra_song_3_result, "song_instance_id":int(song_instance_id)})
        if emotion == "angry":
            tough_s = tough_df['id'].sample(1)
            id_pre = tough_s.to_string()
            id = id_pre[-23:-1]
            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]

            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = tough_dataframe.loc[tough_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = tough_dataframe.loc[tough_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = tough_dataframe.loc[tough_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]



            release_date = tough_dataframe.loc[tough_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]


            tough_s_1 = calm_df['id'].sample(1)
            id_pre_1 = tough_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/"+id1)

            tough_s_2 = calm_df['id'].sample(1)
            id_pre_2 = tough_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/"+id2)

            tough_s_3 = calm_df['id'].sample(1)
            id_pre_3 = tough_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/"+id3)


            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness,  "release_date": release_date,
                           "popularity": popularity
                              , "extra_song_1": extra_song_1,
                           "extra_song_2": extra_song_2, "extra_song_3": extra_song_3,
                           "extra_song_1_result": extra_song_1_result, "extra_song_2_result": extra_song_2_result,
                           "extra_song_3_result": extra_song_3_result, "song_instance_id":int(song_instance_id)})
        if emotion == "surprise":
            calm_s = calm_df['id'].sample(1)
            id_pre = calm_s.to_string()
            id = id_pre[-23:-1]
            result = ("https://open.spotify.com/embed/track/"+id)
            song_detail = spotify.track(track_id=id)
            song_name = song_detail["name"]

            song_instance = Song(song_name=song_name, songid=id, song_cat="calm")
            song_instance.save()
            song_instance_id = song_instance.id

            popularity = calm_dataframe.loc[calm_dataframe['id'] == id].popularity
            popularity = popularity.to_string()[8:]

            danceability = calm_dataframe.loc[calm_dataframe['id'] == id].danceability
            danceability = danceability.to_string()[8:]

            acousticness = calm_dataframe.loc[calm_dataframe['id'] == id].acousticness
            acousticness = acousticness.to_string()[8:]


            release_date = calm_dataframe.loc[calm_dataframe['id'] == id].release_date
            release_date = release_date.to_string()[8:]

            calm_s_1 = calm_df['id'].sample(1)
            id_pre_1 = calm_s_1.to_string()
            id1 = id_pre_1[-23:-1]
            extra_song_1 = spotify.track(track_id=id1)
            extra_song_1_result = ("https://open.spotify.com/embed/track/" + id1)

            calm_s_2 = calm_df['id'].sample(1)
            id_pre_2 = calm_s_2.to_string()
            id2 = id_pre_2[-23:-1]
            extra_song_2 = spotify.track(track_id=id2)
            extra_song_2_result = ("https://open.spotify.com/embed/track/" + id2)

            calm_s_3 = calm_df['id'].sample(1)
            id_pre_3 = calm_s_3.to_string()
            id3 = id_pre_3[-23:-1]
            extra_song_3 = spotify.track(track_id=id3)
            extra_song_3_result = ("https://open.spotify.com/embed/track/" + id3)

            return render(request, 'recommender/song_playing.html',
                          {"result": result, "song_name": song_name, "danceability": danceability,
                           "acousticness": acousticness, "release_date": release_date,
                           "popularity": popularity
                              , "extra_song_1": extra_song_1,
                           "extra_song_2": extra_song_2, "extra_song_3": extra_song_3,
                           "extra_song_1_result": extra_song_1_result, "extra_song_2_result": extra_song_2_result,
                           "extra_song_3_result": extra_song_3_result, "song_instance_id":int(song_instance_id)})
    else:
        return render(request, 'recommender/song_playing.html')

def analysis(request):
    analysis_objs = Analysis.objects.filter(user = request.user)
    labels = []
    data = []
    dict_d = {}
    analysis_objs = list(analysis_objs)
    num_notifications = len(analysis_objs)
    for obj in analysis_objs:
        if obj.emotion not in dict_d.keys():
            dict_d[obj.emotion] = 1
        else:
            dict_d[obj.emotion]+= 1

    for i in dict_d:
        labels.append(i)
        data.append(dict_d[i])

    max_key = max(dict_d, key=dict_d.get)
    status = ""
    if max_key == 'neutral':
        status = "Feeling neutral most times is the best alignment you can be because it means doing what is good without bias for or against order. But be awarn that it can be a dangerous alignment when it advances mediocrity by limiting the actions of the truly capable."
    if max_key == 'sad':
        status = "It looks like you are sad in the past few days...                           Try to think about whether your sleep and eating patterns are good for you.Help someone else. Find a creative way to express your sadness, like listening more to our calm and positive music!"
    if max_key == 'happy':
        status = "You are doing so good!, Keep up the good mood!!!"
    if max_key == 'surprise':
        status = "Accept that unexpected things can happen. ...   Do you have control over any of the unexpected events that regularly occur? ... Prepare yourself for the unexpected. ... don't over react immediately. ...cknowledge your emotions. ...Stay Positive."
    if max_key == 'disgust':
        status = "Don't over react, Respond with Flexibility. ..."
    if max_key == 'fear':
        status = "Don't figure things out by yourself."+ "Be real with how you feel. Be OK with some things being out of your control. Practice self-care.Be conscious of your intentions. Focus on positive thoughts.Practice mindfulness.Train your brain to stop the fear response."
    if max_key == 'angry':
        status = "1. Think before you speak  2. Once you're calm, express your anger  3. Get some exercise. 4. listen to music that eases your anger 5. Take a timeout."
    return render(request, 'recommender/analysis.html', {"analysis_objs":analysis_objs,
        'labels': labels,
        'data': data,"status":status
    })