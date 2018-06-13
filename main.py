import database_connector as db
from dog import *
config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'database': 'wordpress_test',
  'raise_on_warnings': True,
  'port':'8889'
}

db_connector = db.DbConnector(config)
db_connector.establish_link()
dog_name = 'Test Dog'
test_guid = 'http://education.themerex.net/?p=424024xd'
dummy_dog = Dog(test_guid, dog_name, 'This is a test lol.')
dummy_dog_2 = Dog(test_guid+str('_new11'), dog_name+"_new11", 'This is a new test11 lol.')
db_connector.insert_dog(dummy_dog_2)
db_connector.commit_link()
db_connector.disconnect_link()
