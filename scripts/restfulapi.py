#!/usr/bin/python3
from flask import Flask, request
import scrapy_google_maps
import json

app = Flask(__name__)
scr = None

def items_convert_to_json(items_body):
    items_array = []

    for items_item in items_body:
        items_json = {}
        # Exapnd item
        items_json["address"] = items_item.address
        items_json["star"] = items_item.star
        items_json["comment_number"] = items_item.comment_number
        items_json["name"] = items_item.name
        items_json["website"] = items_item.website
        items_json["map_website"] = items_item.map_website

        # Exapnd parking
        if len(items_item.parking) > 0:
            items_json["parking"] = []
            for parking_item in items_item.parking:
                items_parking = {}
                items_parking["address"] = parking_item.address
                items_parking["star"] = parking_item.star
                items_parking["comment_number"] = parking_item.comment_number
                items_parking["name"] = parking_item.name
                items_parking["website"] = parking_item.website
                items_parking["map_website"] = parking_item.map_website
                items_json["parking"].append(items_parking)

        items_array.append(items_json)

    return items_array

@app.route('/find_restaurant', methods = ['POST'])
def find_restaurant():
    content = request.get_json()
    keyword = content.get('restaurant')
    location = content.get('location')

    return_data = {"Header":"header", "Search_result":"fail"}
    search_word = keyword + '+' + location

    restaurant_parking = None
    if content.get('parking') == "True":
        restaurant_parking = scr.find_restaurant_and_self_parking(search_word)
    else:
        restaurant_parking = scr.find_restaurant(search_word)

    if len(restaurant_parking) > 0 and restaurant_parking is not None:
        return_data["Search_result"] = "success"
        return_data["Result"] = items_convert_to_json(restaurant_parking)
    else:
        return_data["Search_result"] = "fail"
        return_data["Result"] = "None"

    return return_data

if __name__ == "__main__":
    scr = scrapy_google_maps.scrapy()
    app.run(host = '0.0.0.0', port = 5000)