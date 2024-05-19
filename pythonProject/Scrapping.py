from bs4 import BeautifulSoup
import requests


hotels_data = []


def scrap_hotel(city, check_in, check_out):
    hotels_data.clear()
    url = 'https://www.booking.com/searchresults.html?ss='+city+'&checkin='+check_in+'&checkout='+check_out
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.findAll('div', {'data-testid': 'property-card'})

        #--------------------------------------------Loop over the hotel elements and find the desired data------------------------------------------
        # If any data is not valid that info will be "Not Given"
        for hotel in hotels:
            name_element = hotel.find('div', {'data-testid': 'title'})
            name = name_element.text.strip()

            address_element = hotel.find('span', {'data-testid': 'address'})
            if address_element is not None:
                address = address_element.text.strip()
            else:
                address = "NOT GIVEN"

            distance_element = hotel.find('span', {'data-testid': 'distance'})
            if distance_element is not None:
                distance = distance_element.text.strip()
            else:
                distance = "NOT GIVEN"

            rating_element = hotel.find('a', {'data-testid': 'secondary-review-score-link'})
            if rating_element is not None:
                rating = rating_element.text.strip()
            else:
                rating = "NOT GIVEN"

            price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
            if price_element is not None:
                price = price_element.text.strip()[3:]
            else:
                price = "NOT GIVEN"


            #---------------------------------------------Append hotels_data with info about hotel---------------------------------------------------
            hotels_data.append({
                'Name': name,
                'Address': address,
                'Distance': distance,
                'Rating': rating,
                'Price': price
            })
    except requests.exceptions.RequestException as e:
        hotels_data.append({
            #Only name is enough. Because in GUI class and line 128 name is the only thing if it is "Connection Error" or not
            'Name': "Connection Error",
        })



