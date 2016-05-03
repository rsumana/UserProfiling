# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "sumanaravikrishnan"
__date__ = "$29-Jan-2016 19:06:24$"

import facebook
import csv
import json
import string
import requests
import os

csvParams = ['category', 'website', 'about', 'talking_about_count', 'name', 'products', 'company_overview', 'has_added_app', 'can_post', 'link', 'likes', 'parking', 'is_community_page', 'were_here_count', 'checkins', 'id', 'is_published', 'bio', 'cover', 'username', 'affiliation', 'personal_info', 'personal_interests', 'category_list', 'location', 'phone', 'general_info', 'description', 'hours', 'birthday', 'public_transit', 'founded', 'mission', 'awards', 'price_range', 'studio', 'produced_by', 'directed_by', 'genre', 'plot_outline', 'daily_active_users', 'icon_url', 'namespace', 'monthly_active_users', 'weekly_active_users', 'logo_url', 'daily_active_users_rank', 'monthly_active_users_rank', 'hometown', 'current_location', 'band_members', 'record_label', 'general_manager', 'network', 'schedule', 'season', 'starring', 'release_date', 'press_contact', 'booking_agent', 'band_interests', 'influences', 'artists_we_like', 'written_by', 'screenplay_by', 'payment_options', 'attire', 'restaurant_services', 'culinary_team', 'restaurant_specialties', 'app_id', 'company', 'members', 'subcategory', 'global_brand_root_id', 'mobile_web_url', 'parent_page', 'features', 'built']

inputPath = "";
outputPath = "";

def getAPIKey():
    with open('E:/PythonProjects/PageLikes/src/apiKey.txt', 'r') as f:
        api_key = f.readline()
    f.close();
    return api_key

def getRelationFile():
    #f = open('E:/UWT/2_Winter2016_TCSS555B_MachineLearning/Assignments/Project/Dataset/FacebookDataTCSS555Project/TCSS555/Train/Relation/Relation.csv');
    f = open ('uniquePages.csv');
    csv_file = csv.reader(f)
    return csv_file

def jsonToList(json):
    jsonList = []
    for i in range(len(csvParams)):
        param = csvParams[i]
        try:
            value = json.get(param)
            value = string.replace(value, "\r", " ");
            value = string.replace(value, "\t", " ");
            value = string.replace(value, "\"", " ");
            jsonList.append(value.encode('utf-8'))
        except:
            jsonList.append("")
            continue
    #print jsonList
    return jsonList

def relation():
    jsonPages = open(outputPath+"/jsonPages.csv", 'w+')
    jsonPagesWriter = csv.writer(jsonPages, quoting=csv.QUOTE_ALL)
    jsonPagesWriter.writerow(csvParams)
    count = 0
    for f in os.listdir(inputPath):
        count += 1
        if(count%10000 == 0):
            print(count)
        filePath = inputPath + "/" + f;
        postJson = json.load(open(filePath))
        rowList = jsonToList(postJson)
        jsonPagesWriter.writerow(rowList)
    jsonPages.close()
    
if __name__ == "__main__":
    inputPath = raw_input('Enter a input folder: ')
    outputPath = raw_input('Enter a output folder: ')
    print inputPath
    print outputPath
    relation()