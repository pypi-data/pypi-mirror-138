import pandas as pd
from sentence_transformers import SentenceTransformer
from autoads.keywords import get_keywords_from_api_and_url
from autoads.models import get_similarity_api,get_similarity_scrape

email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
seed_keywords = ['ARR Loans', 'Revenue Based Loans', 'Loans for SaaS Companies'] 
scrape = True # keep true if you want to scrap urls
depth = 1 # depth for scraping range from 1 to 4
urls = ['capchase.com','pipe.com'] # urls to scrape 
exclude = ['twitter', 'google', 'facebook', 'linkedin', 'youtube'] # sites to exclude
df_api_path = 'data/df_api.csv' # filename for api keywords
df_scrape_path = 'data/df_scrape.csv' # file name for scraped keywords
model_path = 'Maunish/ecomm-sbert' # this model is already uploaded on huggingface so no need to download

df_api,df_scrape = get_keywords_from_api_and_url(
        email= email, 
        api_key=api_key, 
        seed_keywords=seed_keywords, 
        depth=depth, 
        scrape=scrape, 
        urls=urls, 
        exclude=exclude, 
)

model = SentenceTransformer(model_path)

print("Calculating similarity for api keywords")
keywords1 = df_api['Keywords'].tolist()
keywords2 = df_api['Keywords2'].tolist()
df_api['similarity'] = get_similarity_api(model,keywords1,keywords2)

print("Calculating similarity for scraped keywords")
scrape_keywords = df_scrape['Keywords'].tolist()
for keyword in seed_keywords:
    df_scrape[keyword] = get_similarity_scrape(model,scrape_keywords,keyword)

df_api.to_csv(df_api_path,index=False)
df_scrape.to_csv(df_scrape_path,index=False)

print(df_api.head())
print(df_scrape.head())
