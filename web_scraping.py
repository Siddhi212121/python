import requests
from bs4 import BeautifulSoup
import pandas

oyo_url="https://www.oyorooms.com/hotels-in-bangalore/"
page_num_max=3
scraped_info_list =[]

for page_num in range(1, page_num_max):
    req=requests.get(oyo_url+ str(page_num))
    content=req.content

soup=BeautifulSoup(content,"html.parser")

all_hotels=soup.find_all("div",{"class":"hotelCradListing"})

for hotel in all_hotels:
    hotel_dict={}
    hotel_dict["name"]=hotel.find("h3",{"class":"ListingHotelDescription__hotelName"}).text
    hotel_dict["address"]=hotel.find("span",{"itemprop":"streetAddress"}).text   
    hotel_dict["price"]=hotel.find("span",{"class":"listingPrice__finalPrice"}).text
    #try....except
    try:
        hotel_dict["rating"]=hotel.find("span",{"class":"hotelRating__ratingSummary"}).text
    except AttributeError:
            pass
    parent_ammenities_element = hotel.find("div",{"class":"amenitWrapper"})
    
    amenities_list=[]
    for amenity in parent_ammenities_element.find_all("div",{"class":"amenityWrapper__amenity"}):
        amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
        
    hotel_dict["amenities"]=','.join(amenities_list[:-1])
    
    scraped_info_list.append(hotel_dict)
    
    dataFrame=pandas.dataFrame(scraped_info_list)
    dataFrame.to_scv("Oyo.csv")
    

    
        
      
