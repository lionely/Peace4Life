from time import gmtime, strftime
import mysql.connector
from dog import *


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

def get_primary_key(guid):
    """
    Returns the ID for a row in the wp_posts tables.
    This ID is used to assign the tag/category.
    """
    query = ("SELECT ID FROM wp_posts WHERE guid = %(guid)s")
    cursor.execute(query,{ 'guid': guid })
    result_set = [result[0] for result in cursor][0]
    return result_set

def find_existing_dog(guid):
    """
    Takes a Dog guid and checks if it is in the database of dogs.
    returns dog's guid
    """
    #https://stackoverflow.com/questions/4253960/sql-how-to-properly-check-if-a-record-exists
    query = ("SELECT guid FROM wp_posts WHERE guid = %(guid)s")
    cursor.execute(query,{ 'guid': guid })
    result_set = [result[0] for result in cursor]
    num_results = len(result_set)
    if num_results == 0:
        return None
    elif num_results == 1:
        return result_set
    else:
        print("Expected 1 guid but got: "+str(num_results))
        return result_set

def insert_dog(dog):
    """
    Takes a Dog object and inserts it into the database by
    editing the wp_posts,wp_postmeta and wp_term_relationships tables.
    """
    today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    add_posts = ("INSERT INTO wp_posts "
           "(guid, post_title, post_content,post_excerpt,to_ping,pinged,\
           post_content_filtered,post_date,post_status) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    posts_data = (dog.guid,
                dog.name,
                dog.description,
                dog.excerpt,
                dog.ping,
                dog.pinged,
                dog.post_content_filtered,
                today,
                'publish') # ??????
    cursor.execute(add_posts, posts_data)
    # This allows WordPress to display the pet on the 'Adoptions' page.
    # Also need to add Dog tag, as if there is no Dog tag, the post is archived.
    add_term_relationship_cat = ("INSERT INTO wp_term_relationships"
    "(object_id, term_taxonomy_id , term_order) "
    "VALUES (%s,%s,%s)")
    # 85 is the Adoption category in this theme.
    # 0 is a default term_order. Plays no significance to my knowledge so far.
    object_id = get_primary_key(dog.guid)
    term_relationship_cat_data = (object_id,85,0)
    cursor.execute(add_term_relationship_cat, term_relationship_cat_data)

    add_term_relationship_tag = ("INSERT INTO wp_term_relationships"
    "(object_id, term_taxonomy_id , term_order) "
    "VALUES (%s,%s,%s)")
    # 23 is Adoption tag, so we can just add an animal whether its specicies
    term_relationship_tag_data = (object_id,23,0)
    cursor.execute(add_term_relationship_tag, term_relationship_tag_data)
    insert_pict_post(dog)
    print("New dog inserted!")

def insert_pict_post(dog):
    add_pict_post = ("INSERT INTO wp_posts "
           "(guid, post_title, post_content,post_excerpt,to_ping,pinged,\
           post_content_filtered,post_date,post_type,post_mime_type,post_status) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)")
    pict_data = (dog.guid+"_picture",
                dog.name+"_name",
                "",
                "",
                "",
                "",
                "",
                today,
                "attachment",
                "image/jpeg",
                "inherit")
    cursor.execute(add_pict_post, pict_data)
    #Next we need to add the picture information into wp_postmeta
    #Dealing with pictures
    add_thumbnail_id_row = ("INSERT INTO wp_postmeta"
    "(post_id, meta_key , meta_value) "
    "VALUES (%s,%s,%s)")
    object_id = get_primary_key(dog.guid)
    object_meta_value = get_primary_key(dog.guid+"_picture")
    thumbnail_row_data = (object_id,'_thumbnail_id',object_meta_value)
    cursor.execute(add_thumbnail_id_row, thumbnail_row_data)
    #TODO meta_value will eventually be the path of where dog picts are saved
    add_picture_meta = ("INSERT INTO wp_postmeta"
    "(post_id, meta_key , meta_value) "
    "VALUES (%s,%s,%s)")
    picture_row_data = (object_meta_value,'_wp_attached_file','dogs/test_dog.jpg')
    cursor.execute(add_picture_meta, picture_row_data)


#TODO update Test dog with a description and a picture
#TODO this should take a guid
def update_dog(dog,update_query=''):
    #https://www.tutorialspoint.com/sql/sql-update-query.htm
    """
    To insert a dog, we need atleast post_content,post_excerpt,to_ping,pinged and post_content_filtered
    """
    update_query = ("UPDATE wp_posts SET post_content = %(post_content)s \
                WHERE guid = %(guid)s ")
    cursor.execute(update_query, { 'post_content':dog.description,'guid': dog.guid})
    print("Dog updated!")

def create_or_update(dog):
    """
    If a dog already exists but the new tentative entry differs,
    we may update the entry. The difference is determined by if the post_content
    is different.
    """
    dog_guid = find_existing_dog(dog.guid)
    if dog_guid:
        update_dog(guid)
    else:
        insert_dog(dog)

dog_name = 'Test Dog'
test_guid = 'http://education.themerex.net/?p=424024xd'
dummy_dog = Dog(test_guid, dog_name, 'This is a test lol.')
dummy_dog_2 = Dog(test_guid+str('_new10'), dog_name+"_new10", 'This is a new test10 lol.')
#update_dog(dummy_dog_2.guid+"_picture",update_query)
#insert_dog(dummy_dog_2)


# Make sure data is committed to the database
link.commit()
cursor.close()
link.close()
