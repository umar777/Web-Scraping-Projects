import requests
import pandas as pd

# Add your Google Maps API key here
GOOGLE_MAPS_API_KEY = ""

def search_google_places(query, location='52.4862,-1.8904', radius=5000, api_key=GOOGLE_MAPS_API_KEY):
    """
    Searches for places using Google Places API.
    
    Args:
        query (str): The search query, e.g., 'perfume shops in Birmingham'.
        location (str): The latitude,longitude of the place to search around (Birmingham in this case).
        radius (int): Radius in meters to search within.
        api_key (str): Your Google Maps API key.
    
    Returns:
        list: A list of dictionaries containing place details like name, address, phone number, and website.
    """
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': query,
        'location': location,
        'radius': radius,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    
    places = []
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
    """
    Retrieves details about a place using its place_id.
    
    Args:
        place_id (str): The Google Places place ID.
        api_key (str): Your Google Maps API key.
    
    Returns:
        dict: A dictionary containing the details of the place like phone number and website.
    """
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'formatted_phone_number,website',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json().get('result', {})

def export_to_csv(places, filename='places_data.csv'):
    """
    Exports the list of places to a CSV file using pandas DataFrame.
    
    Args:
        places (list): A list of dictionaries containing place information.
        filename (str): The filename for the output CSV.
    """
    df = pd.DataFrame(places)
    df.to_csv(filename, index=False)
    print(f"Data exported successfully to {filename}")

def main():
    query = 'perfume shops in Birmingham'
    results = search_google_places(query)
    
    if results:
        export_to_csv(results, filename='perfume_shops_birmingham.csv')
    else:
        print("No results found.")

if __name__ == '__main__':
    main()
