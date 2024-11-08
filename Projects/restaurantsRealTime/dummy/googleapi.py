import requests
import json

class GoogleAPI:
    # Function to extract desired information
    def extract_info(self, data):
        extracted_data = []
        for item in data['result']:
            extracted_item = {}
            extracted_item['business_status'] = item.get('business_status', False)
            extracted_item['formatted_address'] = item.get('formatted_address', False)
            extracted_item['open_now'] = item.get('opening_hours', {}).get('open_now', False)
            extracted_item['name'] = item.get('name', False)
            extracted_item['permanently_closed'] = item.get('permanently_closed', False)
            extracted_item['price_level'] = item.get('price_level', False)
            extracted_item['rating'] = item.get('rating', False)
            extracted_data.append(extracted_item)
        return extracted_data

    def query_google_places_api(self, api_key, query, location=None, radius=None, language=None, types=None):
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": query,
            "key": api_key
        }

        if location:
            params["location"] = location
        if radius:
            params["radius"] = radius
        if language:
            params["language"] = language
        if types:
            params["types"] = types

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print("Error:", data["error_message"])
            return None


    def googleapi(self):
        my_dic = {}
        query = "Indian restaurants"
        api_key = "Your API Key"
        query = query
        location = "42.560429036635405, -83.1608106317661"  # Latitude, Longitude of Troy MI
        radius = 5000  # Search within 5000 meters
        language = "en"  # English
        types = "restaurant"  # Limit results to restaurants

        result = self.query_google_places_api(api_key, query, location, radius, language, types)
        places = result['results']
        my_dic['result'] = places

        # Extract information
        extracted_info = self.extract_info(my_dic)
        print(extracted_info)

        return extracted_info