# Googlemap_scraper

## Description:
  Scraper for google maps with chinese.

## Test environment:
  - Ubuntu 20.04 x86_64

## Dependance:
  - docker
  - docker-compose
  
## Using:
  - Server
    ```bash
    git clone https://github.com/Raspberry-Pi-4-MCU/googlemap_scraper
    cd googlemap_scraper
    sudo docker-compose up -d
    ```
  - Client(HTTP):
     - URL: http://127.0.0.1:5000/find_restaurant
     - Method: POST
     - Header: Content-Type: application/json
  - Example:
    ```bash
    curl --header "Content-Type: application/json"   \
    --request POST \
    --data '{"restaurant":"宵夜", "location":"土城", "parking":"True"}' \
    http://127.0.0.1:5000/find_restaurant
    ```
 
 



