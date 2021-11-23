# Srilankan_ODI_Cricket_Players_Search_Engine

This Repository includes the frontend,backend implementaion for a search query.
After configruing the elasticsearch, the sample search engine is used to try the query searches.

Directory Structure
---
```
 ├── corpus : Contains raw and pre-processed data 
 ├── templates : The resultpage for UI (of Flask)
 ├── app.py : Flask backend to have transaction with ElasticSearch APIs
 ├── index.py : Python file that converts JSON and uploads to ElasticSearch Bulk API
 ├── preprocessed_scrapper.py : Preprocess scrapped data
 ├── query_types.py : ElasticSearch search queries inclusive of advanced queries
 ├── raw_data_scrapper.py : Data scrapper to scrap data from espncricinfo.com
 ├── search.py : Search API call
 ├── similarity_checker.py : Calculate cosine similarity between query and data
 ├── synonyms.py : Contains synonyms for some keywords
```

Setup
---
* Install ElasticSearch 
* Run ElasticSearch
* Run 'preprocessed_scrapper.py' to add index and add data
* Run 'index.py' to add index and add data
* Run 'app.py' (You should have Flask frame work installed)
* Go to http://127.0.0.1:5000
* Type some queries and search

SampleQueries
---
* அவிஷ்கா பெர்னாண்டோ
* 1000 ஒட்டங்களுக்கு மேல் எடுத்த வீரர்கள்
* 150 விக்கெட்டுகளுக்கு மேல் எடுத்த வீரர்கள் 
* 500 ஒட்டங்களுக்கு குறைவாக எடுத்த வீரர்கள்
* புனித செபஸ்டியன் கல்லூரி படித்த வீரர்கள்
* 100 போட்டிகளில் ஆடிய வீரர்கள்
