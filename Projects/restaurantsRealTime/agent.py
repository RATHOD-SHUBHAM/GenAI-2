import json
import requests


class Agent:
    def query_google_places_api(self, api_key, keyword, location=None, radius=4828, language=None, types=None):
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        params = {
            "key": api_key
        }

        if keyword:
            params["keyword"] = keyword
        if location:
            params["location"] = location
        if radius:
            params["radius"] = radius
        if language:
            params["language"] = language
        if types:
            params["types"] = types

        # params["strictbounds"] = True

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print("Error:", data["error_message"])
            return None

    # Function to extract desired information
    def extract_info(self, data):
        extracted_data = []
        for item in data['result']:
            extracted_item = {}
            extracted_item['business_status'] = item.get('business_status', False)
            extracted_item['formatted_address'] = item.get('vicinity', False)
            extracted_item['open_now'] = item.get('opening_hours', {}).get('open_now', False)
            extracted_item['name'] = item.get('name', False)
            extracted_item['permanently_closed'] = item.get('permanently_closed', False)
            extracted_item['price_level'] = item.get('price_level', False)
            extracted_item['rating'] = item.get('rating', False)
            extracted_data.append(extracted_item)
        return extracted_data

    def agent(self, keyword, radius):
        my_dic = {}
        # Example usage:
        api_key = "AIzaSyBCHjJyTXEb3mz6LxJncFvj83FvM0g1ocE"
        keyword = keyword
        location = "42.560429036635405, -83.1608106317661"  # Latitude, Longitude of Troy MI
        radius = radius
        language = "en"  # English
        types = "restaurant"  # Limit results to restaurants

        result = self.query_google_places_api(api_key, keyword, location, radius, language, types)
        places = result['results']

        my_dic['result'] = places
        # Extract information
        extracted_info = self.extract_info(my_dic)
        # print(extracted_info)

        return extracted_info
