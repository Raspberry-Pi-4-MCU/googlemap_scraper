import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

class items:
    def __init__(self):
        self.star = 0
        self.address = ""
        self.comment_number = 0
        self.website = ""
        self.name = ""
        self.parking = []

class scrapy:
    def __init__(self):
        self.googlemaps_url = 'https://www.google.com.tw/maps/search'
        # self.place = None
        # self.keyword = None
        self.mutex_lock = False
        self.star = 'data=!4m4!2m3!5m1!4e8!6e5'
        self.ua = UserAgent()

    # find '[' and ']'
    def my_find_pair(self, pair_str, start_position, end_position):
        # find first '['
        first_pos = -1
        obj_str = pair_str[start_position]
        for pos in range(start_position, end_position):
            if obj_str == '[':
                first_pos = pos - 1
                break
            else:
                obj_str = pair_str[pos]
        
        # Can not find structure
        if first_pos == -1:
            return None

        counter = 0
        end_pos = 0
        for pos in range(first_pos, end_position):
            if pair_str[pos] == '[':
                counter = counter + 1
            elif pair_str[pos] == ']':
                counter = counter - 1

            if counter == 0:
                end_pos = pos + 1
                break
        
        return pair_str[first_pos:end_pos].split(']\\n,')

    def get_raw(self, keyword, place = None):
        # To avoid multi-thread call the function
        if self.mutex_lock == True:
            return []
        else:
            self.mutex_lock = True

        # position of string of script
        script_keyword_group = []

        # position of string of keyword
        keyword_group = []

        # Combin url
        if place != None:
            combin_urls = self.googlemaps_url + '/' + keyword + '/' + '@' + place + '/' + self.star
        else:
            combin_urls = self.googlemaps_url + '/' + keyword
        
        # Get response from google maps
        user_agent = self.ua.random

        headers = {'user-agent': user_agent}

        web_response = requests.get(combin_urls, headers=headers)

        # Wait for random time

        random_wait_time = random.randint(1, 5)

        time.sleep(random_wait_time)
    
        web_response_parser = BeautifulSoup(web_response.text, 'html.parser')

        web_response_parse_script = web_response_parser.findAll("script")

        # Find keyword script
        for web_sub in web_response_parse_script:
            script_keyword_group.append(web_sub.text)

        # Create keyword
        re_string = keyword.replace("+", " ")
        match_pair = re.compile(re_string)
        
        # Analysis keyword
        find_result = []

        # Analysis result
        analysis_result = None
        
        for script_keyword in script_keyword_group:   
            for m in match_pair.finditer(script_keyword):
                find_result = self.my_find_pair(script_keyword, m.start(), len(script_keyword))
                # Can not find result
                if find_result == None:
                    continue
                if (len(find_result) > 10):
                    analysis_result = self.analysis(find_result)
                    break
        # Unlock
        self.mutex_lock = False

        return analysis_result

    def analysis(self, raw_data):
        items_array = []

        # Record position of search
        record_pos = []

        counter = 0

        # find '篇評論'
        for result_idx in raw_data:
            if '篇評論' in result_idx:
                record_pos.append(counter)
            counter = counter + 1

        # Get information
        for record_pos_idx in record_pos:
            # 
            name_pos = 0
            
            # Create new items
            new_items = items()

            if "http" in raw_data[record_pos_idx+2]:
                # Website ripple
                raw_website = raw_data[record_pos_idx+2].split(',')[2]
                http_pos = raw_website.find('http')
                tail_pos = raw_website.find("\\",http_pos)
                new_items.website = raw_website[http_pos:tail_pos]
                name_pos = record_pos_idx+4
            else:
                name_pos = record_pos_idx+3

            # address ripple 
            address_raw = raw_data[name_pos+1].split(',')[4].replace('\\"',"")
            address_ripple_pos = address_raw.find('號')
            new_items.address = address_raw[0:address_ripple_pos+1]
            # Other 
            new_items.name = raw_data[name_pos].split(',')[1].replace('\\"',"")
            new_items.star = raw_data[record_pos_idx+1].split(',')[3]
            new_items.comment_number = raw_data[record_pos_idx+1].split(',')[4]
            items_array.append(new_items)

        # return result
        return items_array
        
    def find_parking(self, address):
        get_raw_result = self.get_raw(address + '+find parking')
        if get_raw_result == None:
            return []
        else:
            return get_raw_result

    def find_restaurant(self, keyword):
        get_raw_result = self.get_raw(keyword)
        if get_raw_result == None:
            return []
        else:
            return get_raw_result

    def find_restaurant_and_self_parking(self, keyword):
        restaurant = self.find_restaurant(keyword)
        if restaurant == []:
            return []

        Parking = []
        # Find parking by address
        for restaurant_item in restaurant:
            address = restaurant_item.address
            parking_info = self.find_parking(address)
            restaurant_item.parking = parking_info

        return restaurant
            
        


# https://www.google.com.tw/maps/search/桃園+燒肉/@24.9911045,121.2313636,13z/data=!4m4!2m3!5m1!4e8!6e5

#r = requests.get("https://www.google.com.tw/maps/search/%E6%A1%83%E5%9C%92+%E6%9E%9C%E6%B1%81/@24.9911045,121.2313636,13z")

#print(r.text)

if __name__ == "__main__":
    scr = scrapy()
    # scr.get_raw('330桃園市桃園區中華路8號+find parking')
    restaurant = scr.find_restaurant('桃園+田季發爺')
    for restaurant_item in restaurant:
        print(restaurant_item.name)

    # scr.find_parking('330桃園市桃園區大興路136號')
    '''
    restaurant_parking = scr.find_restaurant_and_self_parking('桃園+田季發爺+')
    for restaurant in restaurant_parking:
        for parking in restaurant.parking:
            print(parking.name, parking.address)
    '''