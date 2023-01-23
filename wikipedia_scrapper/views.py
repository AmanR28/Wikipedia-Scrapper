import re 
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import lxml
from bs4 import BeautifulSoup
from .scrapper import Processor


class Wiki(APIView):
    def __init__(self):
        self.BASE_URL = 'https://en.wikipedia.org/wiki/'
        self.HEADERS = {  
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' 
        }


    def get(self, _, country:str = ""):
        # Validation 
        #    Valid Input : "Abc", "ABC", "abc", "A B", "a_b" 
        #    These are accepted by wikipedia
        pattern = re.compile(r"[a-zA-Z]+([\s_][a-zA-Z]+)*$")
        country = country.strip()
        if not pattern.match(country): 
            return Response("Invalid Input", 403)


        # Create Url
        URL = self.BASE_URL + country.lower()

        # Get Data
        try :
            html = requests.get(URL, headers=self.HEADERS)
        except :
            return Response("Something Went Wrong", 500)
        

        # Process Data
        soup = BeautifulSoup(html.content, 'lxml')
        data = soup.find('table', class_='infobox')
        if not data:
            return Response("Something Went Wrong", 500)
        if not 'ib-country' in data['class']:
            return Response('Invalid Input : Check if it a Country', 403)
                          
        # Extract Data
        processor = Processor(data)
        Required = [
            'flag_url',
            'capital',
            'largest_city',
            'official_languages',
            'area_total',
            'Population',
            'GDP_nominal'
        ]
        Result = {}
        for r in Required:
            Result[r] = processor.process[r]()

        return Response(Result)
