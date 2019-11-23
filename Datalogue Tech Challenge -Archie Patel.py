# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 22:47:25 2019

Prompt
Imagine that Datalogue is working with a customer in the Hospitality industry to develop a
solution that will standardize the way this customer ingests data from varied hotel vendors.
The customer would like the following: 
    1) to create a standardized, clean dataset of hotels in
Seattle, Washington; and 
    2) to have Datalogue assist them in discovering some valuable
insights on top of the clean data.

@author: Archie Patel
"""
# Importing the libraries
import pandas as pd
import json
import matplotlib.pyplot as plt

# Importing the datasets, csv first
data1 = pd.read_csv('vendor1.csv', encoding='utf-8')
#data list is to initialize the list that will hold each line of json data
datalist = []

#Begin "unwrapping json data line by line
#Note: For some reason the encoding = "utf-8" isn't working, not sure why?
with open("vendor2.json", encoding="utf-8") as file:
    for line in file:
        json_line = json.loads(line)
        address = json_line.get('address')
#unwrapping the address into the 4 parts
        street = address.get('street')
        city = address.get('city')
        state = address.get('state')
        zipc = address.get('zipcode')
#Initialize concatenated address variable, and address-quality variable
        paddress = ""
        #add_qual = 0
        description = json_line['description']
        
#Logic to create street, city, state, zip address. If something is missing, 
# then it's just not populated. Also creating add_qual variable to use when 
# matching rows with similar data. (Didn't end up using the add_qual variable,
# because I thought length of address could be used instead. Thought process
# was: the longer the address for the same location, the more complete it is)
        
        if street is None:
            paddress = ""
        else:
            paddress = street.strip()
            #add_qual +=1
            
        if city is None:
            paddress = paddress
        else:
            if paddress == "":
                paddress = city.strip()
                #add_qual +=1
            else:
                paddress = paddress + ", " + city.strip()
                #add_qual +=1
                
        if state is None:
            paddress = paddress
        else:
            if paddress == "":
                paddress = state.strip()
                #add_qual +=1
            else:
                paddress = paddress + ", " + state.strip()
                #add_qual +=1
        
        if zipc is None:
            paddress = paddress
        else:
            if paddress == "":
                paddress = zipc.strip()
                #add_qual +=1
            else:
                paddress = paddress + " " + zipc.strip()
                #add_qual +=1
                
#Create list to make the columns of the dataframe. Matched to the order of the csv file
        data = [json_line['name'], paddress, json_line['description'], json_line['rating']]
        datalist.append(data)  
        
#Convert list of lists into dataframe
data2 = pd.DataFrame(datalist, columns =['name', 'address', 'description', 'rating'])

#Vertically concat json and csv files
comb_data = pd.concat([data1, data2], axis=0)
comb_data = comb_data.reset_index(drop=True)

#Create address length variable, sort by descritpion and address length
#Remove duplicate descriptions, keeping the last row (i.e. the most complete address)
comb_data['add_len'] = comb_data['address'].str.len()
comb_data = comb_data.sort_values(['description', 'add_len'], ascending=[True, True])
comb_data =comb_data.drop_duplicates(subset='description', keep='last')
comb_data = comb_data.reset_index(drop=True)
del comb_data['add_len']

#Summary statistics
print("Number of hotels: ",comb_data['name'].count() )
print("Median rating: ",comb_data['rating'].median())
print("Average rating: ", comb_data['rating'].mean())
print("Standard deviation of rating: ", comb_data['rating'].std())

