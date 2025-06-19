import time
import hmac
import hashlib
import requests
import json
from storyblocks_search_api import get_search_id

import streamlit as st


def get_api_info(stock_item_id, using_alt = False):

    if len(str(stock_item_id)) == 0:
        return False


    # Provided by Storyblocks (replace with your actual keys)
    publicKey = 'test_29c9931ed920fdbf22e24704a1c5fc9784d01551acd6f5a5e348e5c1768'
    privateKey = 'test_e2cd94b1c00e25004716f27aabfab57d061bcf347ad61d44cdf7b55ef84'


    # stock_item_id = '300537745'
    # URL and resource info
    baseUrl = "https://api.storyblocks.com"
    resource = f"/api/v2/audio/stock-item/details/{stock_item_id}"


    # Create full URL for the audio item
    url = baseUrl + resource

    # HMAC generation
    expires = str(int(time.time()))
    hmacBuilder = hmac.new(bytearray(privateKey + expires, 'utf-8'), resource.encode('utf-8'), hashlib.sha256)
    hmacHex = hmacBuilder.hexdigest()

    # Query parameters (these need to be passed in the URL)
    params = {
        'APIKEY': publicKey,
        'EXPIRES': expires,
        'HMAC': hmacHex
    }

    # Make the request
    response = requests.get(url, params=params)

    if response.status_code == 404:
        if not using_alt:
            alt_id = get_search_id(stock_item_id)
            api_result = get_api_info(alt_id, using_alt=True)
            return api_result

        return False

    # Debugging: Print response content and status code
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Raw Response Text: {response.text}")

    if response.status_code == 404:
        return {}

    # Check if the response is in JSON format

    try:
        # Pretty-print the JSON response
        print("Stock Item Details:", json.dumps(response.json(), indent=4))
    except ValueError as e:
        print(f"Error parsing JSON: {e}")


    raw_response_text = json.dumps(response.json(), indent=4)

    # Parse the JSON response
    response_json = json.loads(raw_response_text)

    # print(raw_response_text)

    # Extract the required information dynamically
    try:
        response_data = {
            "name": response_json.get("title").strip(),
            "composer": response_json.get("artists", [{}])[0].get("alias"),
            "musician": f"{response_json.get('artists', [{}])[0].get('firstName')} {response_json.get('artists', [{}])[0].get('lastName')}",
            "producer": response_json.get("artists", [{}])[0].get("publisher"),
            "record_company": response_json.get("artists", [{}])[0].get("publisherPro"),
            "sba": response_json.get("asset_id")
        }
    except:
        return False
    print(f'ID: {stock_item_id}')
    print(response_data)

    st.write(response_data)

    return response_data


if __name__ == '__main__':

    # get_api_info('179350')
    id = '300515818'

    result = get_api_info(id)

    if not result:
        get_search_id(id)
