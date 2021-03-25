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

import time



st.set_page_config(
    page_title="Beer Price Checker!",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache
def load_csv():
    return pd.read_csv("df_price.csv",header=0,index_col=0)


st.title("Beer Price Check V3")
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
class_names = ['Asahi', 'Blue Girl', 'Blue Ice', 'Budweiser', 'Carlsberg', 'Corona', 'Guinness', 'Heineken', 'Kingway', 'Kirin', 'San Miguel', 'San Miguel Light', 'Skol', 'Sol', 'Stella Artois', 'Tiger', 'Tsingtao', 'Yanjing']


if uploaded_file is not None:
    if sample == True:
        try:
          original_image = Image.open(image_path)
          fixed_image = ImageOps.exif_transpose(original_image)
          image_to_resize = img_to_array(fixed_image)
        
          resized = tf.image.resize(image_to_resize, [224, 224], method="bilinear",antialias=False)
          img_array = tf.keras.preprocessing.image.img_to_array(resized)
        
          img_array = tf.expand_dims(img_array, 0) # Create a batch
        
          predictions = model.predict(img_array)
          score = tf.nn.softmax(predictions[0])
        
          img_show = tf.squeeze(
              img_array , axis=None, name=None)
          
          predicted_class = class_names[np.argmax(score)]
        
          st.write(f"This image most likely belongs to {predicted_class}")
        
          percentages = [i * 100 for i in predictions.tolist()[0]]
        
          results = zip(class_names, percentages)
          sorted_by_second = sorted(results, key=lambda tup: tup[1],reverse=True)
        
        
          for i in sorted_by_second[:2]:
            st.write(i)
        
        except:
          pass
    else:
        try:
          original_image = Image.open(uploaded_file)
          col1.image(original_image)
          fixed_image = ImageOps.exif_transpose(original_image)
          image_to_resize = img_to_array(fixed_image)
        
          resized = tf.image.resize(image_to_resize, [224, 168], method="bilinear",antialias=False)
          img_array = tf.keras.preprocessing.image.img_to_array(resized)
        
          img_array = tf.expand_dims(img_array, 0) # Create a batch
        
          predictions = model.predict(img_array)
          score = tf.nn.softmax(predictions[0])
        
          img_show = tf.squeeze(
              img_array , axis=None, name=None)
          
          
          predicted_class = class_names[np.argmax(score)]
        
          st.write(f"This image most likely belongs to {predicted_class}")
        
          percentages = [i * 100 for i in predictions.tolist()[0]]
        
          results = zip(class_names, percentages)
          sorted_by_second = sorted(results, key=lambda tup: tup[1],reverse=True)
          for i in sorted_by_second[:2]:
            st.write(i)
                   
        except:
          pass
    
    # #Grab Test Pictures
    # test_dir = pathlib.Path("./pictures/")
    # TEST = list(test_dir.glob("*"))
    # len(TEST)
    
    # for string in TEST: 
    #       # print(string)
    #       try:
    #         original_image = Image.open(str(string))
    #         fixed_image = ImageOps.exif_transpose(original_image)
    #         image_to_resize = img_to_array(fixed_image)
    
    #         resized = tf.image.resize(image_to_resize, [224, 224], method="bilinear",antialias=False)
    #         img_array = tf.keras.preprocessing.image.img_to_array(resized)
    
    #         img_array = tf.expand_dims(img_array, 0) # Create a batch
    
    #         predictions = model.predict(img_array)
    #         score = tf.nn.softmax(predictions[0])
    
    #         img_show = tf.squeeze(
    #             img_array , axis=None, name=None)
    
    
    #         print(
    #             "This image most likely belongs to {} with a {:.2f} percent confidence."
    #             .format(class_names[np.argmax(score)], 100 * np.max(score))
    #         )
    
    #         percentages = [i * 100 for i in predictions.tolist()[0]]
    
    #         results = zip(class_names, percentages)
    #         sorted_by_second = sorted(results, key=lambda tup: tup[1],reverse=True)
    
    
    #         for i in sorted_by_second[:2]:
    #           print(i)
    
    #         plt.imshow(resized/255.);
    #         plt.axis(False);
    #         plt.show()
    #         print("----------------------------------------------")
    #         print(" ")
    
    #       except:
    #         pass
        
    # ##------------------------------------------------------------------------    
    df = load_csv()
    # df = df.fillna("--")
    st.header("Best Prices Found")
    temp_df = df[df.Brand==predicted_class.title()]
    
    
   
    st.table(temp_df.style.highlight_min(subset=['Wellcome','PARKnSHOP','Market_Place','Watsons','Aeon','DCH Food Mart'],color = '#D3D3D3', axis = 1))
    correct = "None"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    col2.header("Is this {pronoun} {beer_class}?".format(pronoun = "a" if predicted_class[0].lower() not in ['a','e','i','o','u'] else "an", beer_class=predicted_class))
    if col2.button("Yes"):
        col2.text("Thank you!")
        correct = "True"
        original_image = original_image.save(f"./pictures/{correct}_{predicted_class}_{timestr}.jpg")

    if col2.button("No"):
        col2.text("Please take another photo")
        correct = "False"
        original_image = original_image.save(f"./pictures/{correct}_{predicted_class}_{timestr}.jpg")

    
    time.sleep(10)
    if correct != "True" and correct != "False":
        original_image = original_image.save(f"./pictures/None_{predicted_class}_{timestr}.jpg")
    
    

    
