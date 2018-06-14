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

if __name__ == "__main__":
    db_test.main()
    db_connector = db.DbConnector(config)
    db_connector.establish_link()
    dogs = sc.get_dog_from_each_home_page(url)
    for dog in dogs:
        db_connector.create_or_update(dog)
        db_connector.commit_link()
    db_connector.disconnect_link()
