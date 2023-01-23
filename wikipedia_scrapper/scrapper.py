import unicodedata

class Processor():
    def __init__(self, data):
        self.data = data
        self.process = {
            'flag_url': self.processFlag,
            'capital' : self.processCapital,
            'largest_city': self.processLargestCity,
            'official_languages': self.processOfficialLanguage,
            'area_total': self.processArea,
            'Population': self.processPopulation,
            'GDP_nominal': self.processGDP
        }

    def processFlag(self):
        SEARCH = 'Flag of'
        containers = self.data.find_all('a', class_='image')
        flag = None
        for container in containers:
            title = container.get('title')
            if title and SEARCH in title:
                flag = container.find('img')['src']
                break
        flagSrc = 'https:' + flag[:flag.rindex('/')].replace('/thumb', '', 1)
        return flagSrc

    def processCapital(self):
        SEARCH = 'Capital'
        containers = self.data.find_all('tr')
        capitals = []
        for container in containers:
            text = container.text.split()
            if text and SEARCH in text[0]:
                capitals = container.find('td', class_='infobox-data')\
                                        .find_all('a')
                capitals = [x.text for x in list(capitals) if x.text == x.get('title') ]
                
                if len(capitals) == 1:
                    return capitals[0]
                
                return capitals

    def processLargestCity(self):
        SEARCH = 'Largest city'
        SIZE = len('Largest City')
        containers = self.data.find_all('tr')
        cities = []
        for container in containers:
            text = container.text
            if text and SEARCH in text[:SIZE]:
                cities = container.find('td', class_='infobox-data')\
                                        .find_all('a')
                cities = [x.text for x in list(cities) if x.text == x.get('title') ]
                
                if len(cities) == 1:
                    return cities[0]
                
                return cities

    
    def processOfficialLanguage(self):
        SEARCH = 'Official languages'
        SIZE = len(SEARCH)
        containers = self.data.find_all('tr')
        languages = []
        for container in containers:
            text = unicodedata.normalize("NFKD",container.text)
            if text and SEARCH in text[:SIZE]:
                languages = container.find('td', class_='infobox-data')\
                                        .find_all('a')
                languages = [x.text for x in list(languages) if x.text in str(x.get('title')) ]


                if len(languages) == 1:
                    return languages[0]
                
                return languages

        
    def processArea(self):
        SEARCH = 'Area'
        SIZE = len(SEARCH)
        containers = self.data.find_all('tr')
        pos = 0
        for pos, container in enumerate(containers):
            text = container.text
            if text and SEARCH in text[:SIZE]:
                break

        areaContainer = containers[pos+1].find('td', class_='infobox-data')
        res = areaContainer.find(text=True).split()[0]
        return res


    def processPopulation(self):
        SEARCH = 'Population'
        SIZE = len(SEARCH)
        containers = self.data.find_all('tr')
        pos = 0
        for pos, container in enumerate(containers):
            text = container.text
            if text and SEARCH in text[:SIZE]:
                break

        popContainer = containers[pos+1].find('td', class_='infobox-data')
        res = popContainer.find(text=True).split()[0]
        return res


    def processGDP(self):
        SEARCH = 'GDP (nominal)'
        SIZE = len(SEARCH)
        containers = self.data.find_all('tr')
        pos = 0
        for pos, container in enumerate(containers):
            text = unicodedata.normalize("NFKD",container.text)
            if text and SEARCH in text[:SIZE]:
                break

        GDPContainer = containers[pos+1].find('td', class_='infobox-data')
        res = GDPContainer.text
        res = res[:res.index('[')]

        return res
    





