from bs4 import BeautifulSoup
import requests
import json

gapPage = 10
baseUrl = 'https://quotes.toscrape.com'

def createTags(element):
    element = element.find_all('a', class_='tag')
    tags = []
    
    class Tag(object):
        def __init__(self, name, link):
            self.name = name
            self.link = link
    
    for el in element:
        name = el.getText()
        link = baseUrl + el['href']
        tag = Tag(name, link)
        tags.append(tag.__dict__)     

    return tags

def createAuthor(element):
    class Author(object):
        def __init__(self, name, linkAbout):
            self.name = name
            self.linkAbout = linkAbout
            
    nameAuthor = element.find('small', class_='author').getText()
    linkAuthor = baseUrl + element.find_all('span')[1].find('a')['href']
    
    author = Author(nameAuthor, linkAuthor)
    
    return author.__dict__

def createCard(soup):
    
    array = []
    htmlCards = soup.find_all('div', class_='quote')
    
    class Card(object):
        def __init__(self, text, tags, author):
            self.text = text
            self.tags = tags
            self.author = author

    for element in htmlCards:
        
        text = element.find('span').getText()   
        tags = createTags(element)
        author = createAuthor(element)
        card = Card(text, tags, author)
        array.append(card.__dict__)
        
    return array

def createTopTenTags(element):
    element = element.find_all('span', class_='tag-item')
    top = []
    
    class TopTag(object):
        def __init__(self, name, link):
            self.name = name
            self.link = link
    
    for el in element:
        name = el.a.getText()
        link = baseUrl + el.a['href']
        tag = TopTag(name, link)
        top.append(tag.__dict__)     

    return top

def init():
    
    arrayCards = []
    
    class Data(object):
        def __init__(self, data):
                self.data = data
    
    for page in range(gapPage):
        
        url = baseUrl + '/page/' + str(page + 1)

        request = requests.get(url)

        soup = BeautifulSoup(request.content, 'html.parser')
        
        class Cards(object):
            def __init__(self, cards, title, page, topTenTags):
                self.page = page + 1
                self.title = title
                self.topTenTags = topTenTags
                self.cards = cards


        array = createCard(soup)
        title = soup.find(class_='row header-box').a.getText()
        topTenTags = createTopTenTags(soup)
        arrayCards.append(Cards(array, title, page, topTenTags).__dict__)


    data = Data(arrayCards)
    
    with open('CMtecnologia.json', 'w', encoding='utf-8') as f:
        json.dump(data.__dict__, f, ensure_ascii=False, indent=4)


init()
