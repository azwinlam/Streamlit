# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 18:56:09 2021

@author: azwin
"""
import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image, ImageOps
import cv2 
import re
from os.path import join
from glob import glob
import time


def load_logo():
    files = []
    for ext in ('*.gif', '*.png', '*.jpg'):
        files.extend(glob(join("./logo", ext)))
    beer_list = {}
    for i in files:
        key = re.findall(r"./logo\/(.+)\.",i)
        img1 = cv2.imread(str(i)) 
        img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        sift = cv2.ORB_create()
        keypoints, descriptors = sift.detectAndCompute(img2,None)
        img3 = cv2.drawKeypoints(img2,keypoints,img1)
        beer_list[key[0]] = img2, keypoints, descriptors
    return beer_list

beer_list = load_logo()


st.set_page_config(
    page_title="Beer Price Checker!",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache
def load_csv():
    return pd.read_csv("df_price.csv",header=0,index_col=0)

@st.cache(suppress_st_warning=True)
def load_model(original_image):
       
    fixed_image = ImageOps.exif_transpose(original_image)
    image_to_resize = img_to_array(fixed_image)
      
    resized = tf.image.resize(image_to_resize, [224, 168], method="bilinear",antialias=False)
    img_array = tf.keras.preprocessing.image.img_to_array(resized)
      
    img_array = tf.expand_dims(img_array, 0) # Create a batch
      
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
      
    img_show = tf.squeeze(img_array , axis=None, name=None)
    
    
    predicted_class = class_names[np.argmax(score)]
      
    st.write(f"This image most likely belongs to {predicted_class}")
      
    percentages = [i * 100 for i in predictions.tolist()[0]]
      
    results = zip(class_names, percentages)
    sorted_by_second = sorted(results, key=lambda tup: tup[1],reverse=True)
    for i in sorted_by_second[:2]:
        st.write(i)
    
    return predicted_class, sorted_by_second[:3]
      


st.title("Beer Price Check V6 CNN + SIFT")
st.subheader("By Alex, Azwin, Jason")


uploaded_file = st.file_uploader("Upload Image of Beer Logo")


col1, col2 = st.beta_columns(2)
sample = False
if uploaded_file is None:
    if st.button('Load Demo'):
        image_path = "./sample/blueicetest1.jpg"
        st.write('Sample Loaded')
        sample = Image.open(image_path)
        col1.image(sample)
        uploaded_file = True
        sample = True

## Model Loading
model = tf.keras.models.load_model('MAR25AFTERNOON.h5')
class_names = ['Asahi', 'Blue Girl', 'Blue Ice', 'Budweiser', 'Carlsberg', 'Corona Extra', 'Guinness', 'Heineken', 'Kingway', 'Kirin', 'San Mig', 'San Miguel', 'Skol Beer', 'Sol', 'Stella Artois', 'Tiger', 'Tsingtao Beer', 'Yanjing Beer']


if uploaded_file is not None:
    if sample == True:
        try:
            original_image = Image.open(image_path)
            predicted_class, top3 = load_model(original_image)
        except:
          pass
    else:
        try:
            col1.image(Image.open(uploaded_file))
            
            col1.write("")
            original_image = Image.open(uploaded_file).convert("RGB")
            predicted_class, top3 = load_model(original_image)
            original_image = Image.open(uploaded_file).convert("RGB")
            original_image.save("./sample/test.jpg")

            def input_image():
                img1 = cv2.imread("./sample/test.jpg") 
                img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                sift = cv2.ORB_create()
                keypoints, descriptors = sift.detectAndCompute(img2,None)
                img3 = cv2.drawKeypoints(img2,keypoints,img1)
                return img2, keypoints, descriptors
            
            def check_image(base,test="Test"):
                bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
                matches = bf.match(beer_list[base][2],beer_list[test][2])
                matches = sorted(matches, key = lambda x:x.distance)
                imgA = cv2.drawMatches(beer_list[base][0],beer_list[base][1], beer_list[test][0], beer_list[test][1], matches[:50], beer_list[test][0], flags=2)
                st.image(imgA, width = 300)
                st.write(base)
                st.write(f"Matches: {len(matches)} out of Total: {len(beer_list[base][1])}") 
                st.write(f"Percent Match: {round(len(matches)/len(beer_list[base][1])*100,2)} ")
                return base, len(matches)/len(beer_list[base][1])   
            
            beer_list["Test"] = input_image()  
            answer = []
            for i in top3:
                answer.append(check_image(i[0],"Test"))
            final_answer = sorted(answer, key = lambda x: x[1],reverse=True)[0][0] 
            st.write(final_answer)
            
                   
        except:
          pass
    
    df = load_csv()
    # df = df.fillna("--") 
    st.header("Best Prices Found")
    
    @st.cache
    def temp_df():
        return df[df.Brand==predicted_class.title()]
    
    temp_df = temp_df()
    
    
   
    st.table(temp_df.style.highlight_min(subset=['Wellcome','PARKnSHOP','Market_Place','Watsons','Aeon','DCH Food Mart'],color = '#D3D3D3', axis = 1))
    correct = "None"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    col2.header("Is this {pronoun} {beer_class}?".format(pronoun = "a" if predicted_class[0].lower() not in ['a','e','i','o','u'] else "an", beer_class=final_answer))
    if col2.button("Yes"):
        col2.text("Thank you!")
        correct = "True"
        original_image = original_image.save(f"./pictures/{correct}_{predicted_class}_{timestr}.jpg")

    if col2.button("No"):
        col2.text("Please take a photo with focus on the logo")
        correct = "False"
        original_image = original_image.save(f"./pictures/{correct}_{predicted_class}_{timestr}.jpg")

    

    if correct != "True" and correct != "False":
        original_image = original_image.save(f"./pictures/None_{predicted_class}_{timestr}.jpg")
    