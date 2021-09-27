import requests
import json
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.cluster import MiniBatchKMeans

tmdb_api_key = "TMDB API KEY HERE"

BASE_URL = "https://api.themoviedb.org/3"
POSTER_SMALL_BASE_URL = "https://www.themoviedb.org/t/p/w45/"
POSTER_BASE_URL = "https://www.themoviedb.org/t/p/w500/"

def lambda_handler(event, context):
    movie = event['queryStringParameters']["query"]

    response = requests.get(f"{BASE_URL}/search/movie?api_key={tmdb_api_key}&query={movie}")
    poster_path = json.loads(response.text)["results"][0]["poster_path"]
    
    response = requests.get(f"{POSTER_SMALL_BASE_URL}{poster_path}")
    img = Image.open(BytesIO(response.content))
    pix_val = np.array(list(img.getdata()))
    
    kmeans = MiniBatchKMeans(n_clusters=7, random_state=0).fit(pix_val)
    colors = ['#' + ''.join(f'{i:02X}' for i in [int(color) for color in colortuple]) for colortuple in kmeans.cluster_centers_]
    props = list(np.bincount(kmeans.labels_))
    
    result = list(zip(colors, props))
    result = sorted(result, key=lambda a: a[1], reverse=True)
    
    totalOthers = sum([x[1] for x in result[1:]])
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            "poster":f"{POSTER_BASE_URL}{poster_path}", 
            "primaryColor":result[0][0], 
            "otherColors":[{"color": col[0], "proportion": col[1]/totalOthers} for col in result[1:]]
        })
    }