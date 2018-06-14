import urllib2
from bs4 import BeautifulSoup
from dog import *

def download_file(url,file_name):
    """
    This takes a url and saves the file to disk.
    """
    #http://stackabuse.com/download-files-with-python/
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()
    with open(file_name, 'wb') as f:
        f.write(datatowrite)

#TODO After scraping all dog text, maybe look at on average in data where the name might be?
def getHomePageDogs(url,limit=None):
    """
    This is a function which takes a url, and scrapes the pictures and links to biographies
    of dogs on the homepage of Empathy for Life and returns it as a list of dogs.
    """
    href_begin = 'http://cafe.naver.com/forewl?iframe_url='
    page = urllib2.urlopen(url)
    soup_ul = BeautifulSoup(page,'lxml').find('ul','article-album-sub border-sub')#specifiy parser "lxml"
    soup_a = soup_ul.findAll('a') #This has the link to a dog's page on naver and picture
    soup_dl = soup_ul.findAll('dt')#.a['title']#this will be used to dog dog name

    # For dog(a), get the text,get it's image and assign it a name
    # A Dog eventually needs to be (guid,name,description)
    count = 0
    dogs_scraped = []
    for a in soup_a:
        if a.img and a.span and a.span['class'] ==['border_absolute']:
            guid = str(a.img['src'])
            text_length = len(guid)//2
            dog_name = str(guid[text_length:text_length+20]) #soup_dl[count].a['title']
            dog_text_link = href_begin + a['href'].replace("&amp;", "&")
            dog_description = getDogText(dog_text_link)
            #print(guid[text_length:text_length+20])
            dog_disk_loc = '/Applications/MAMP/htdocs/wordpress/wp-content/uploads/dogs/'
            download_file(guid,dog_disk_loc+str(guid[text_length:text_length+20])+".jpg")
            #urllib.request.urlretrieve(guid, dog_disk_loc+str(dog_name)+".jpg")
            dog = Dog(guid,dog_name,dog_description[:10])
            dogs_scraped.append(dog)
            count+=1
            if count==1:
                break
    return dogs_scraped

def get_catalog_pages(url):
    href_begin = 'http://cafe.naver.com/'
    page = urllib2.urlopen(url)
    catalog_pages_navi = BeautifulSoup(page,'lxml').find('div','prev-next').find('table','Nnavi')
    catalog_pages = [href_begin+cat.a['href'] for cat in catalog_pages_navi.findAll('td')]
    #print len(catalog_pages)
    return catalog_pages

#TODO figure out how to scrape until the end of the page.
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

def get_dog_from_each_home_page(url):
    dog_list = []
    for catalog in get_catalog_pages(url):
        dog_list+=getHomePageDogs(catalog)
    return dog_list
# url = 'http://cafe.naver.com/ArticleList.nhn?search.clubid=26290786&search.menuid=32&search.boardtype=I'
# print len(get_dog_from_each_home_page(url))
