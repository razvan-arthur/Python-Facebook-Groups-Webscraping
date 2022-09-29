from selenium import webdriver
import sqlite3
from post import Post
import time

username="user"
password="pass"

def get_all_posts():
    c.execute("SELECT * FROM postari")
    return c.fetchall()

def insert_post(post):
    with conn:
        c.execute("INSERT INTO int_posts VALUES (:url, :user, :cerere)", {'url': post.url, 'user': post.user, 'cerere': post.cerere})
def move_post(post):
    with conn:
        c.execute("DELETE from int_posts WHERE user = :user AND cerere = :cerere",
                    {'user': post.user, 'cerere': post.cerere})
#        print(post.url,post.user,post.cerere)
        c.execute("INSERT INTO postari VALUES (:url, :user, :cerere)",
                  {'url': post.url, 'user': post.user, 'cerere': post.cerere})


#int_posts
conn = sqlite3.connect('postari.db')

c = conn.cursor()
"""   CREATE TABLE int_posts(
                url text,
                user text,
                cerere text)"""
test_post1= Post("test1","test1","test1")
test_post2= Post("test2","test2","test2")
test_post3= Post("test3","test3","test3")
#insert_post(test_post1)
#insert_post(test_post2)
#insert_post(test_post3)
users_to_message=[]
message=" . ."
def send_message(user):

    print("Message sent to :", "https://www.facebook.com/messages/t/"+user)


def verify_int_posts():
    c.execute('SELECT * FROM int_posts')
    res=c.fetchall()
    for row in res:
        post_i = Post(row[0],row[1],row[2])
        print(row[0],"\n",row[1],"\n",row[2])
        if input("Send message?: [Y]/[N]")=='y':
            users_to_message.append(post_i)
        move_post(post_i)
    if users_to_message:
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "profile.managed_default_content_settings.images": 2}
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome("/Users/Arthur/Downloads/chromedriver.exe", options=chrome_options)
        driver.get("https://www.facebook.com/messages/t/RazvanVilceanu")
        time.sleep(2)
        driver.find_element_by_name('email').send_keys(username)
        driver.find_element_by_name('pass').send_keys(password)

        for user in users_to_message:
            send_message(user.user)

verify_int_posts()
print(get_all_posts())
#c.execute("DELETE from postari")
#conn.commit()
