import database_connector as db
import scraper as sc
from dog import *
import test_database_connect as db_test

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'database': 'wordpress_test',
  'raise_on_warnings': True,
  'port':'8889'
}
url = 'http://cafe.naver.com/ArticleList.nhn?search.clubid=26290786&search.menuid=32&search.boardtype=I'
#
# dog_name = 'Test Dog'
# test_guid = 'http://education.themerex.net/?p=424024xd'
# dummy_dog = Dog(test_guid, dog_name, 'This is a test lol.')
# dummy_dog_2 = Dog(test_guid+str('_new11'), dog_name+"_new11", 'This is a new test11 lol.')
# db_connector.insert_dog(dummy_dog_2)
# db_connector.commit_link()
# db_connector.disconnect_link()
if __name__ == "__main__":
    db_test.main()
    db_connector = db.DbConnector(config)
    db_connector.establish_link()
    dogs = sc.getHomePageDogs(url)
    #print len(dogs)
    for dog in dogs:
        db_connector.create_or_update(dog)
        db_connector.commit_link()
    db_connector.disconnect_link()
