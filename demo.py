from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
from pymongo import MongoClient
import pymysql
import streamlit as st

st.title("youtube data harvesting")

api_key='AIzaSyAK4UiDcELmzjka5YNM7kyGP6DRyPrtls8'
#api_service_name = "youtube'
#api_version = 'v3'
channel_id='UCUBNKEKMaWE-gkUZ2ptvyuQ'
#'UCUBNKEKMaWE-gkUZ2ptvyuQ' #biriyani man reacts
#'UCueYcgdqos0_PzNOq81zAFg' parthapagal
#'UCUnYvQVCrJoFWZhKK3O2xLg' Javatpoint
#'UCv9bWHC0DIn-Xb7ALNoOGWQ' w3schools
#'UCnz-ZXXER4jOvuED5trXfEA' techTFQ           

youtube=build('youtube', 'v3', developerKey=api_key)

#get channel details
def get_channel_stats(youtube,channel_id):
    all_data=[]
    request=youtube.channels().list(
              part='snippet,contentDetails,statistics',
              id=channel_id)
    response=request.execute()

    for i in range(len(response['items'])):
        data=dict(channel_name=response['items'][i]['snippet']['title'],
            subscriber=int(response['items'][i]['statistics']['subscriberCount']),
            viewcount=int(response['items'][i]['statistics']['viewCount']),
            total_videos=int(response['items'][i]['statistics']['videoCount']),
             publishedAt=str(datetime.strptime((response['items'][i]['snippet']['publishedAt']), '%Y-%m-%dT%H:%M:%S.%fz')),
            #publishedAt=(response['items'][i]['snippet']['publishedAt']),
            channel_id=channel_id,
            description=response['items'][i]['snippet']['description'],
           playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
            )
        all_data.append(data)
   
    return all_data

get_channel_stats(youtube,channel_id)
channel_detail=get_channel_stats(youtube,channel_id)

if st.text_input("channelId", ""):
    st.write(channel_detail) 


#st.write(channel_detail)

def playlist(channel_id):
    all_playlist=[]
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        #id=channel_id,
        channelId=channel_id,
        maxResults=50)
    response = request.execute()
    
    for i in range(len(response['items'])):
        data=dict(playlist_id=response['items'][i]['id'],
                  channel_id=channel_id,
             publishedAt=str(datetime.strptime((response['items'][i]['snippet']['publishedAt']),'%Y-%m-%dT%H:%M:%Sz')),
             playlist_name=response['items'][i]['snippet']['title'],
             #description=response['items'][i]['snippet']['description'],
             etag=response['items'][i]['etag'],
            itemcount=int(response['items'][i]['contentDetails']['itemCount']))
        
        next_page_token = response.get('nextPageToken')
        
    
        all_playlist.append(data)
        
    return all_playlist
playlist_details=playlist(channel_id)
#st.write(playlist_details)

#get video ids
#nextpagetoken-return the next page result
def get_video_ids(playlist_id):
    video_ids=[]
    playlist_id=playlist_id
    request=youtube.playlistItems().list(part='snippet,contentDetails', 
        playlistId=playlist_id,maxResults=50)
    response=request.execute()    
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token=response.get('nextPageToken')
    #more_pages=True
    
    while next_page_token is not None:
        request=youtube.playlistItems().list(
                     part='snippet,contentDetails', 
                     playlistId=playlist_id, maxResults=50,
                     pageToken=next_page_token)         
        response=request.execute()
            
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        
        next_page_token=response.get('nextPageToken')

    return video_ids

playlist_id="UUnz-ZXXER4jOvuED5trXfEA"

video_id=get_video_ids(playlist_id)

#get video details
def get_video_details(video_id,playlist_id):
    all_video_stats=[]
    
    for i in range(0,len(video_id), 50):
        request=youtube.videos().list(
                 part='snippet,statistics,contentDetails', id=','.join(video_id[i:i+50]))
        response=request.execute()
        
        for video in response['items']:
            video_stats=dict(video_name=video['snippet']['title'],
                             video_id=video['id'],
                             #playlist_id=playlist_details[0]['playlist_id'],
                             playlist_id=playlist_id,
                            published_date=str(datetime.strptime((video['snippet']['publishedAt']),'%Y-%m-%dT%H:%M:%Sz')),
                            description=video['snippet']['description'],
                            views=int(video['statistics']['viewCount']),
                            Likes = int(video['statistics']['likeCount']),
                            Dislikes = video['statistics'].get('dislikeCount'),
                             caption=video['contentDetails']['caption'],
                            #Duration=str(datetime.strptime((video['contentDetails']['duration']),'T%M:%S')),
                            Comments = int(video['statistics'].get('commentCount'))
                            )
            all_video_stats.append(video_stats)
    return all_video_stats

video_details=get_video_details(video_id,playlist_id)
#st.write(video_details)

#comment_details
def get_comments(video_id):
    list_of_comments=[]
    try:
        for i in video_id:
            request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=i, maxResults=100)
            response = request.execute()
        
            for item in response['items']:
                comment_info={
                    "video_id":i,
                    "comment_id":item['snippet']['topLevelComment']['id'],
                    "comment_text":item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "comment_author":item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "comment_publishedAt":str(datetime.strptime((item['snippet']['topLevelComment']['snippet']['publishedAt']),'%Y-%m-%dT%H:%M:%Sz'))
                    }
                list_of_comments.append(comment_info)
    except:
        pass
            
    return list_of_comments
comment_details=get_comments(video_id)

#all_function
def all_function(channel_id):
    channel_stats=get_channel_stats(youtube,channel_id)
    playlist_id=playlist(channel_id)
    #video_id=get_video_ids(playlist_id)
    video_details=get_video_details(video_id, playlist_id)
    comment_details=get_comments(video_id)
    
    data={
        'channel_details':channel_stats,
        'playlist_details':playlist_id,
        'comment_details':comment_details,
        'video_details':video_details
    }
    return data
data1=all_function(channel_id)

#stored in mongo
local_client=MongoClient("mongodb+srv://revathi4179:CsRvNLvxB8oE7BHP@cluster0.efiyjqv.mongodb.net/")

#create new db in cloud(Atlas)
db=local_client["youtube_data"]

#create collection for database in cloud
mycollection=db["alldata"]

mycollection.insert_one(data1)

mycollection.find()

if st.button("store mongodb"):
    #st.text_input("stored")
    #st.text("stored in mongodb")
    list1=[]
    for i in mycollection.find({},{"_id":0}):
        list1.append(i)
    
st.text("stored in mongodb")
 

#sql
myconnection=pymysql.connect(host='127.0.0.1', user='root',password='1234')

#accessing python by using cursor
cur=myconnection.cursor()

#create database
cur.execute("create database youtube_data")

myconnection=pymysql.connect(host='127.0.01', user='root', password='1234', database='youtube_analysis')
cur=myconnection.cursor()

#channel_details
cur.execute("create table channel(channel_name varchar(255),subscriber int,viewcount int, totalvideo int,publishedAt datetime,channel_id varchar(255) primary key,description text,playlist_id varchar(255))")
sql="insert into channel(channel_name, subscriber, viewcount, totalvideo, publishedAt, channel_id, description, playlist_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
for j in i['channel_details']:
    cur.execute(sql,tuple(j.values()))
myconnection.commit()

#playlist_details
cur.execute("create table playlist(playlist_id varchar(255) primary key, channel_id varchar(255), publishedAt datetime, playlist_name varchar(255), etag varchar(255), itemcount int)")
sql1="insert into playlist(playlist_id,channel_id, publishedAt, playlist_name, etag, itemcount) values(%s,%s,%s,%s,%s,%s)"
for j in i['playlist_details']:
    cur.execute(sql1,tuple(j.values()))
myconnection.commit()

#video_details
cur.execute("create table video(video_name varchar(255), video_id varchar(255) primary key, playlist_id varchar(255), published_date datetime, description text, views int, likes int, dislikes int, caption varchar(255), comments int)")
sql2="insert into video(video_name, video_id, playlist_id, published_date, description, views, likes, dislikes, caption, comments) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for j in i['video_details']:
    cur.execute(sql2,tuple(j.values()))
myconnection.commit()

#video_details
cur.execute("create table comment(video_id varchar(255), comment_id varchar(255) primary key, comment_text text, comment_author varchar(255), comment_publishedAt datetime)")
sql3="insert into comment(video_id, comment_id, comment_text, comment_author, comment_publishedAt) values(%s,%s,%s,%s,%s)"
for j in i['comment_details']:
    cur.execute(sql3,tuple(j.values()))
myconnection.commit()

question_tosql = st.selectbox('**Select your Question**',
('1. What are the names of all the videos and their corresponding channels?',
'2. Which channels have the most number of videos, and how many videos do they have?',
'3. What are the top 10 most viewed videos and their respective channels?',
'4. How many comments were made on each video, and what are their corresponding video names?',
'5. Which videos have the highest number of likes, and what are their corresponding channel names?',
'6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
'7. What is the total number of views for each channel, and what are their corresponding channel names?',
'8. What are the names of all the channels that have published videos in the year 2022?',
'9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
'10. Which videos have the highest number of comments, and what are their corresponding channel names?'), key = 'collection_question')

if question_tosql == '1. What are the names of all the videos and their corresponding channels?':
    cur.execute("SELECT channel.Channel_Name, video.Video_Name FROM channel JOIN playlist JOIN video ON channel.Channel_Id = playlist.Channel_Id AND playlist.Playlist_Id = video.Playlist_Id;")
    result1 = cur.fetchall()
    df1 = pd.DataFrame(result1)
    #df1.index += 1
    st.dataframe(df1)
elif question_tosql == '2. Which channels have the most number of videos, and how many videos do they have?':
    cur.execte("select max(`video`.`views`), count(*), `channel`.`channel_name` from video inner join channel on `video`.`playlist_id`=`channel`.`playlist_id` group by `channel`.`channel_name`;")
    result2=cur.fetchall()
    df2=pd.DataFrame(result2)
    st.dataframe(df2)
elif question_tosql == '4.How many comments were made on each video, and what are their corresponding video names?':
    cur.execute("select video_name, comments from video;")
    result4=cur.fetchall()
    df4=pd.DataFrame(result4)
    st.dataframe(df4)
elif question_tosql == '5.Which videos have the highest number of likes, and what are their corresponding channel names?':
    cur.execute("select `channel`.`channel_name`, `video`.`likes` from video inner join channel on `video`.`playlist_id`=`channel`.`playlist_id` order by `video`.`likes` desc limit 0,1;")
    result5=cur.fetchall()
    df4=pd.DataFrame(result5)
    st.dataframw(df4)
elif question_tosql == '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
    cur.execute("select video_name, sum(likes), sum(dislikes) from video group by video_name;")
    result6=cur.fetchall()
    df5=pd.DataFrame(result6)
    st.dataframe(df5)
elif question_tosql == '7.What is the total number of views for each channel, and what are their corresponding channel names?':
    cur.execute("select sum(`video`.`views`) tot_views, `channel`.`channel_name` from video inner join channel on `video`.`playlist_id`=`channel`.`playlist_id` group by `channel`.`channel_name`;")
    result7=cur.fetchall()
    df6=pd.DataFrame(result7)
    st.dataframe(df6)
elif question_tosql == '8.What are the names of all the channels that have published videos in the year 2022?':
    cur.execute("select `channel`.`channel_name` from channel inner join video on `channel`.`playlist_id`=`video`.`playlist_id`where `video`.`published_date` like '%2022%' group by `channel`.`channel_name`;")
    result8=cur.fetchall()
    df7=pd.DataFrame(result8)
    st.dataframe(df7)
elif question_tosql == '9.what are the comments published on october 2014 with corresponding video name?':
    cur.execute("select `comment`.`comment_text`,`video`.`video_name` from comment inner join video on `comment`.`video_id`=`video`.`video_id` where `comment`.`comment_publishedAt` like '2014-10%';")
    result9=cur.fetchall()
    df8=pd.DataFrame(result9)
    st.dataframe(df8)
elif question_tosql == '10.Which videos have the highest number of comments, and what are their corresponding channel names?':
    cur.execute("select `channel`.`channel_name`, `video`.`video_name` from video inner join channel on `video`.`playlist_id`=`channel`.`playlist_id` where `video`.`comments`= (select  max(`comments`) from video );")
    result10=cur.fetchall()
    df9= pd.DataFrame(result10)
    st.dataframe(df9)
myconnection.close()
    

