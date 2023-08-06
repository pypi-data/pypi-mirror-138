import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
from autoads.keywords import get_keywords_from_api_and_url
from autoads.models import get_similarity_api,get_similarity_scrape,get_lfmfuf_predictions

email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
seed_keywords = ["crypto 401k", "real estate 401k", "esg 401k", "business 401k", "business crypto 401k", "business esg 401k",] 
scrape = True # keep true if you want to scrap urls
depth = 1 # depth for scraping range from 1 to 4
urls = ['capchase.com','pipe.com'] # urls to scrape 
exclude = ['twitter', 'google', 'facebook', 'linkedin', 'youtube'] # sites to exclude
df_api_path = 'data/df_api.csv' # filename for api keywords
df_scrape_path = 'data/df_scrape.csv' # file name for scraped keywords
similarity_model_path = 'Maunish/ecomm-sbert' # this model is already uploaded on huggingface so no need to download
lfmfuf_model_path = '' 

df_api,df_scrape = get_keywords_from_api_and_url(
        email= email, 
        api_key=api_key, 
        seed_keywords=seed_keywords, 
        depth=depth, 
        scrape=scrape, 
        urls=urls, 
        exclude=exclude, 
)

model = SentenceTransformer(similarity_model_path)

print("Calculating similarity for api keywords")
keywords1 = df_api['Keywords'].tolist()
keywords2 = df_api['Keywords2'].tolist()
df_api['similarity'] = get_similarity_api(model,keywords1,keywords2)

if scrape:
    print("Calculating similarity for scraped keywords")
    scrape_keywords = df_scrape['Keywords'].tolist()
    for keyword in seed_keywords:
        df_scrape[keyword] = get_similarity_scrape(model,scrape_keywords,keyword)

## LF MF UF prediction
map_group = {
    0:"LF",
    1:"MF",
    2:"UF",
    3:"competitor",
    4:"brand"}

config = AutoConfig.from_pretrained('roberta-base',num_labels=3)
model2 = AutoModelForSequenceClassification.from_config(config=config)
tokenizer = AutoTokenizer.from_pretrained('roberta-base')

api_predictions = get_lfmfuf_predictions(df_api,model2,tokenizer)
df_api['lf/mf/uf'] = np.argmax(api_predictions,axis=1)
df_api['lf/mf/uf'] = df_api['lf/mf/uf'].map(map_group)
df_api.loc[:,["LF","MF","UF"]] = api_predictions
df_api.to_csv(df_api_path,index=False)

if scrape:
    scrape_predictions = get_lfmfuf_predictions(df_scrape,model2,tokenizer)
    df_scrape['lf/mf/uf'] = np.argmax(scrape_predictions,axis=1)
    df_scrape['lf/mf/uf'] = df_scrape['lf/mf/uf'].map(map_group)
    df_scrape.loc[:,["LF","MF","UF"]] = scrape_predictions
    df_scrape.to_csv(df_scrape_path,index=False)

print(df_api.head())
print(df_scrape.head())
