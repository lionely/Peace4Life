import datetime
import mysql.connector
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
dog_name = 'Jetta'
test_guid = 'http://education.themerex.net/?p=424024xd'
test_dog = (test_guid,
            'Test Dog',
            'Test Content',
            'Test Excerpt',
            'Test_Ping',
            'pinged',
            'post_content_filtered')

def find_existing_dog(dog_guid):
    """
    Takes a dog's guid and checks if it is in the database of dogs.
    """
    #https://stackoverflow.com/questions/4253960/sql-how-to-properly-check-if-a-record-exists
    query = ("SELECT COUNT(1) FROM wp_posts WHERE guid = %(guid)s")
    cursor.execute(query,{ 'guid': test_guid })
    result_set = cursor
    for result in result_set:#iterating gives a tuple.
        if result[0] == 0:
            print("Does not exist.")
            return False
        elif result[0] == 1:
            print("Exists.")
            return True

def insert_dog(dog):
    """
    Takes a tuple representing a dog,and if it is not in the database
    then it inserts the dog into the database.
    """
    if dog and not find_existing_dog(dog[0]):
        today = datetime.date.today()
        add_dog = ("INSERT INTO wp_posts "
               "(guid, post_title, post_content,post_excerpt,to_ping,pinged,\
               post_content_filtered,post_date) "
               "VALUES (%s, %s, %s, %s,%s,%s,%s,%s)")
        data_dog = (dog[0],
                    dog[1],
                    dog[2],
                    dog[3],
                    dog[4],
                    dog[5],
                    dog[6],
                    today)
        cursor.execute(add_dog, data_dog)
        print("New dog inserted!")
#TODO update Test dog with a description and a picture
def update_dog(dog):
    """
    If a dog already exists but the new tentative entry differs,
    we may update the entry. The difference is determined by if the post_content
    is different.

    To insert a dog, we need atleast post_content,post_excerpt,to_ping,pinged and post_content_filtered
    """
    if dog and find_existing_dog(dog[0]):
        get_dog = ("SELECT post_content FROM wp_posts WHERE guid = %(guid)s")
        cursor.execute(get_dog,{ 'guid': dog[0] })
        result_set = cursor
        for content in result_set:
            print(content[0])
            #If not same content do an update
            if content[0] != dog[2]:
                add_dog = ("UPDATE  wp_posts SET post_content = %(post_content)s \
                WHERE guid = %(guid)s ")
                cursor.execute(add_dog, { 'guid': dog[0] ,'post_content':dog[2]})
                print("Dog updated!")


#insert_dog(test_dog)
test_dog_updated = (test_guid,
            'Test Dog',
            'Test Content Updated Bro',
            'Test Excerpt',
            'Test_Ping',
            'pinged',
            'post_content_filtered')
update_dog(test_dog_updated)
# Make sure data is committed to the database
link.commit()
cursor.close()
link.close()
