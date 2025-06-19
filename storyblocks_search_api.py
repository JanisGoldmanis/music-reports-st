import time
import hmac
import hashlib
import requests
import json
import streamlit as st


def search_audio(keywords, page, results_per_page):
    # Provided by Storyblocks (replace with your actual keys)
    publicKey = 'test_29c9931ed920fdbf22e24704a1c5fc9784d01551acd6f5a5e348e5c1768'
    privateKey = 'test_e2cd94b1c00e25004716f27aabfab57d061bcf347ad61d44cdf7b55ef84'

    # URL and resource info
    baseUrl = "https://api.storyblocks.com"
    resource = "/api/v2/audio/search"

    # Create full URL for the search
    url = baseUrl + resource

    # HMAC generation
    expires = str(int(time.time()))
    hmacBuilder = hmac.new(bytearray(privateKey + expires, 'utf-8'), resource.encode('utf-8'), hashlib.sha256)
    hmacHex = hmacBuilder.hexdigest()

    # Query parameters (these need to be passed in the URL)
    params = {
        'APIKEY': publicKey,
        'EXPIRES': expires,
        'HMAC': hmacHex,
        'keywords': keywords,
        'page': page,
        'results_per_page': results_per_page,
        'user_id': 'test1',
        'project_id': 'test2'
    }

    # Make the request
    response = requests.get(url, params=params)

    # Debugging: Print response content and status code
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Raw Response Text: {response.text}")

    if response.status_code == 404:
        return []

    # Check if the response is in JSON format
    try:
        response_json = response.json()
        print("Search Results:", json.dumps(response_json, indent=4))
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return []

    return response_json


def get_search_id(keyword):
    search_results = search_audio(
        keywords=f"SBA-{keyword}",
        page=1,
        results_per_page=10
    )
    if not search_results:
        return False
    try:
        result_length = len(search_results['results'])
    except:
        st.write(f'Search API failed for {keyword}')
        return False

    if result_length != 1 or result_length == 0:
        return False

    result_id = search_results['results'][0]['id']
    return result_id

if __name__ == '__main__':
    get_search_id('300515818')
    pass


