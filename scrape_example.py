import urllib2
from bs4 import BeautifulSoup
#TODO The information we might need to scrape is Dog breed,name
#TODO approx age, size or weight, health condition, and personality.

url = 'https://cafe.naver.com/forewl.cafe'
def getHomePageDogs(url,limit=None):
    #TODO filter out images in the result set, that aren't dogs. What is a 'dog'?
    """
    This is a function which takes a url, and scrapes the pictures and links to biographies
    of dogs on the homepage of Empathy for Life and returns it as a list of dogs.
    """
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'lxml')#specifiy parser "lxml"
    #find returns something searchable by bs and finall returns a list.
    # level01 = soup.find('div',attrs={"id":"cafe-body-skin"}).find('div',attrs={"id":"cafe-body"})
    # level23 = level01.find('div',attrs={"id":"content-area"}).find('div',attrs={"id":"main-area","class":"fr"})
    # level45_iframe = level23.find('iframe')
    #Remember Browsers load the iframe content in a separate request
    #will this link change each time??
    response = urllib2.urlopen('https://cafe.naver.com/MyCafeIntro.nhn?clubid=26290786') # how match links with
    iframe_soup = BeautifulSoup(response,'lxml').findAll('dt',attrs={"class":"photo"},limit=limit)
    return iframe_soup

def getDogStory(dogs):
    """
    This is a function which takes a list of 'dogs' and for each dog gets the
    biographical text associated with them and summarises it. This function will also get
    the first 3-4 pictures of the dog on Empathy for Life's naver page. This function should
    return a dictonary which will be then turned into a pandas dataframe.
    """
    #Help for links issues https://groups.google.com/forum/#!msg/beautifulsoup/hm3fh27NUkM/n1NyTqHg97kJ
    #Algorithm
    #Find dt, then look for href attribute, to go to this dog's page.
    href_begin = 'http://cafe.naver.com/forewl?iframe_url='#'http://cafe.naver.com'#this is added to an a front page href to get the article link
    for dog in dogs:

        dog_biography_link = href_begin + dog.a['href'].replace("&amp;", "&")
        page = urllib2.urlopen(dog_biography_link)
        soup = BeautifulSoup(page,'lxml')
        level0 = soup.find('div',attrs={'id':"cafe-body-skin"}).find('div',attrs={'id':"cafe-body"})
        level1 = level0.find('div',attrs={'id':"content-area"})
        dog_iframe = level1.find('iframe',attrs={"name":"cafe_main","id":"cafe_main"})#contains picts and dog bio.
        print(dog_iframe)
        #print(dog_biography_link)
        return
def getDogText(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def makeDogDB():
    return
homepage_dogs = getHomePageDogs(url)
getDogStory(homepage_dogs)
print(homepage_dogs)
# print(len(homepage_dogs))
url = 'http://cafe.naver.com/ArticleRead.nhn?&articleid=17967&clubid=26290786'
#dog_text = getDogText(url)
#print(dog_text)
#Does not make sense to get pictures from each dog page, because I'll have to manually input iframe anywaysself
#But getting an intial picture for each dog and then text might be do-able.
#use src link for dog icon to uniquely identify the dog.
