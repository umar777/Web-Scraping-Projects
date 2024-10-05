import requests
import pandas as pd

# Add your Google Maps API key here
GOOGLE_MAPS_API_KEY = ""

def search_google_places(queries, api_key=GOOGLE_MAPS_API_KEY):
    places = []

    for query in queries: 
        print(query)
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': query,
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        results = response.json().get('results', [])
        
        for result in results:
            place_id = result.get('place_id')
            place_details = get_place_details(place_id, api_key)
            
            places.append({
                'name': result.get('name'),
                'address': result.get('formatted_address'),
                'phone': place_details.get('formatted_phone_number'),
                'website': place_details.get('website')
            })
    
    return places

def get_place_details(place_id, api_key):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'formatted_phone_number,website',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json().get('result', {})

def export_to_csv(places, filename='places_data.csv'):
    df = pd.DataFrame(places)
    df.to_csv(filename, index=False)
    print(f"Data exported successfully to {filename}")

queries = [
    'Sample Search',
    'Sample Search',
    'Sample Search'
]

def main():
    results = search_google_places(queries)
    
    if results:
        export_to_csv(results, filename='perfume_shops_data.csv')
    else:
        print("No results found.")

if __name__ == '__main__':
    main()
