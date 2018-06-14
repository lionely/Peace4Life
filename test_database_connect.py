import database_connector as db
from dog import *
import mysql.connector
#TODO to clean up the connectors.
config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'database': 'wordpress_test',
  'raise_on_warnings': True,
  'port':'8889'
}
link = mysql.connector.connect(**config)
assert(link)
cursor = link.cursor()

db_connector = db.DbConnector(config)
#TODO develop a list of test dogs
def create_test_dogs():
    test_dog_name = 'Test-Suite-Dog_'
    test_guid = 'http://test-suite-dog_'
    test_dogs = []
    for i in range(10):
        test_dog = Dog(test_guid+str(i), test_dog_name+str(i), 'This is a dog created by the test py.')
        test_dogs.append(test_dog)
    return test_dogs

def insert_test_dogs(test_dogs):
    for dog in test_dogs:
        db_connector.insert_dog(dog)
        db_connector.commit_link()
    assert(count_all_test_dogs(test_dogs)==10)
    return

def delete_test_dogs(test_dogs):
    for dog in test_dogs:
        delete_post_query = ("DELETE FROM wp_posts WHERE guid = %(guid)s")
        cursor.execute(delete_post_query, {'guid':dog.guid})
        delete_term_relationship_cat = ("DELETE FROM wp_term_relationships where object_id=%(object_id)s")
        object_id = db_connector.get_primary_key(dog.guid)
        cursor.execute(delete_term_relationship_cat, {'object_id':object_id})

        #Deleting Picture
        delete_pict_post = ("DELETE FROM wp_posts WHERE guid = %(guid)s ")
        cursor.execute(delete_post_query, {'guid':dog.guid+"_picture"})
        delete_picture_meta = ("DELETE FROM wp_postmeta WHERE post_id = %(post_id)s and meta_key='_wp_attached_file' ")
        object_meta_value = db_connector.get_primary_key(dog.guid+"_picture")
        cursor.execute(delete_picture_meta, {'post_id':object_meta_value})
        link.commit()
        db_connector.commit_link()
    assert(count_all_test_dogs(test_dogs)== 0)
    return

def count_all_test_dogs(test_dogs):
    count_dog = ("SELECT COUNT(guid) FROM wp_posts WHERE guid = %(guid)s")
    overall_dog_count = 0
    for dog in test_dogs:
        cursor.execute(count_dog, {'guid':dog.guid})
        result_set = [result[0] for result in cursor][0]
        #print(result_set)
        overall_dog_count+=result_set
    return overall_dog_count

def test_get_primary_key():
    pass

def run_tests():
    passed = False
    test_dogs = create_test_dogs()
    insert_test_dogs(test_dogs)
    delete_test_dogs(test_dogs)
    passed = True
    assert(passed)
    print('Passed tests.')

def main():
    db_connector.establish_link()
    run_tests()
    db_connector.disconnect_link()

if __name__ == "__main__":
    db_connector.establish_link()
    run_tests()
    db_connector.disconnect_link()
