# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 08:40:27 2020

@author: ramesh.v
"""


import pandas as pd
import numpy as np
import streamlit as st

### Adding title to app

##st.title("Pattern Levelled Production Webapp")

### Reading Pattern Sheet

uploaded_file = st.file_uploader("Upload your Pattern excel sheet", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
### Extracting data from excel file
    
new_df = pd.DataFrame()
new_df = df.groupby(['color','cavity',"Freq"])['req/day'].sum().reset_index()

new_df["jig_req/day"]=new_df["req/day"]/new_df["Freq"]
new_df["jig_req/day"]=round(new_df["jig_req/day"])
new_df["lot size"]=(new_df["jig_req/day"]/new_df["cavity"])
new_df["lot size"] = round(new_df["lot size"])
#new_df["Freq"]=round(new_df["Freq"]).astype(int)
#for i in range(0,len(new_df)):
    #if new_df["Freq"].loc[i]==0:
        #new_df["Freq"].loc[i]=1
new_df.sort_values("Freq",ascending = False , inplace = True , ignore_index = True)
Freq_sum = new_df["Freq"].sum()
col_range = Freq_sum + 100

### Creating final DF
final_df = pd.DataFrame(np.nan,index=range(0,col_range),columns = ["color","lot_size"])
final_df= final_df.fillna(value="null")

### Creating function

def move(x,i):
    global y
    if x >=Freq_sum:
        x=0
    while final_df["color"].loc[x]!="null" and x < Freq_sum: 
        if x >= Freq_sum :
            x=0
        else:
             x=x+1
        print("x=",x)
    if x < Freq_sum:
        if final_df["color"].loc[x]=="null":
            final_df["color"].loc[x]=new_df["color"].loc[i]
            ##final_df["part name"].loc[x]=new_df["Part Name"].loc[i]
            final_df["lot_size"].loc[x]=new_df["lot size"].loc[i]
            final_df
        
        y=x
        
for i in range(0,len(new_df)):
    y=0
    ##print("I=",i)
    freq=new_df["Freq"].loc[i]
    ##print("freq=",freq)
    for j in range(0,freq):
        if j!=0:
            x=(Freq_sum//freq)+y
            if x >= Freq_sum:
                x=0
            print("forloop x =",x)
        else:
            x=0
        move(x,i)
        
final_df.drop(final_df[final_df["color"]=="null"].index,inplace = True)


### Adding round no:
Jig_length = 378
sum1= 0
final_df.insert(0,"Round_no",value = "null")
final_df
g = 1
b=0
s1=0
s2=0
jig_length = 378
for i in range (0,10):
    while s1 <= jig_length:
        final_df["Round_no"].loc[b] = g
        s2 = final_df["lot_size"].loc[b]
        #print("s2",s2)
        s1 = s1+s2
        #print("s1",s1)
        b=b+1
        #print("b",b)
        if b>=Freq_sum:
            break
    if b>=Freq_sum:
        break
    g=g+1
    ##print("g",g)
    jig_length = 378*g
    ##print("jig_length",jig_length)


### Create a header 

st.header("Levelled Pattern Production Plan")
st.dataframe(final_df)

### Downloading your pattern file

download=st.button('Download Excel File')

if download:
    final_df.to_excel("pattern_levelled.xlsx")

