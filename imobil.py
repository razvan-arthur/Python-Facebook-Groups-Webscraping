
from selenium import webdriver
from plyer.utils import platform
from plyer import notification
import sqlite3
from post import Post
import time
from selenium.webdriver.common.keys import Keys

#Account to check facebook groups

username='user'
password='pass'

#Functions for database checking

def check_if_new(post):
    c.execute("SELECT * FROM postari WHERE url=:url AND user=:user AND cerere=:cerere", {'url':post.url, 'user':post.user, 'cerere':post.cerere})
    if c.fetchall()==[]:
        c.execute("SELECT * FROM int_posts WHERE url=:url AND user=:user AND cerere=:cerere", {'url':post.url, 'user':post.user, 'cerere':post.cerere})
        if c.fetchall() == []:
            return True
        else:
            return False
    else:
        return False

def get_all_posts():
    c.execute("SELECT * FROM postari")
    return c.fetchall()

def insert_post(post):
    with conn:
        c.execute("INSERT INTO int_posts VALUES (:url, :user, :cerere)", {'url': post.url, 'user': post.user, 'cerere': post.cerere})


def get_posts_by_user(user):
    c.execute("SELECT * FROM postari WHERE user=:user", {'user': user})
    all_posts=c.fetchall()
    for post_i in all_posts:
        print(post_i)

def remove_post(post):
    with conn:
        c.execute("DELETE from postari WHERE user = :user AND cerere = :cerere",
                  {'user': post.user, 'cerere': post.cerere})

#Connecting to the database

conn = sqlite3.connect('postari.db')

c = conn.cursor()

#Starting the web driver

urls = ['https://www.facebook.com/groups/apartamentestil?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/apartamentebucuresti?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/chiriebucuresti?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/208485706441961?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/1643051259339463?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/2677478325811805?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/2677478325811805?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/226303660885851?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/339740070189844?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/apartamentenoibucuresti?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/1427616497513161?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/Admin.Vanzari.Apartamente?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/2038823013000375?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/358979851113612?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/816178031749888?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/1657500911198407?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/204558550308607?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/ImobiliareBucurestiVanzare?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/121010902682088?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/1060545037346559?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/959363130804140?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/118204592204043?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/213923108780635?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/1836548776573323?sorting_setting=CHRONOLOGICAL','https://www.facebook.com/groups/GarsoniereSiApartamenteDeInchiriatBucuresti?sorting_setting=CHRONOLOGICAL']

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2, "profile.managed_default_content_settings.images": 2}
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome("chrome driver url", options=chrome_options)
driver.get(urls[0])

time.sleep(2)

#Logging in

driver.find_element_by_name('email').send_keys(username)
driver.find_element_by_name('pass').send_keys(password)
print("=== Email and password filled ===")
time.sleep(1)

driver.find_element_by_name("pass").send_keys(Keys.ENTER)
time.sleep(2)
print("=== Logged in ===")

#Scraping posts

wordsToSearchFor=["caut","cumpar","looking","buy"]
clienti=[]
failedGroups=0
urlNumber=1
#urls.clear()
for url in urls:
    try:
#        print(url[:-30])
        print("\r", 100 * float(urlNumber) / float(25), "%",end="")
        urlNumber += 1
        driver.get(url)
        time.sleep(2)
        html = driver.find_element_by_tag_name('html')
        for i in range(60):
            html.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
#        print("=== Scrolled ===")
        posts = driver.find_elements_by_xpath("//div[@data-testid='post_message']")
        posts = driver.find_elements_by_xpath("//div[starts-with(@class, 'du4w35lb')]")
        for post in posts:
            print (post.text)

#       print("=== Posts grabbed ===")
        for i in range(len(posts)):
            #du4w35lb
            parent=posts[i].find_element_by_xpath("..")
            post=posts[i].text
            if any(x in post.lower() for x in wordsToSearchFor):
                nume=parent.find_element_by_xpath("./div[1]/div/div/div[2]/div/div/div[2]/h5/span/span")
                start=nume.get_attribute('innerHTML').find('href="https://www.facebook.com/')+31
                end=nume.get_attribute('innerHTML').find('?',start)
                id=nume.get_attribute('innerHTML')[start:end]
                timp=parent.find_element_by_class_name('timestampContent').text
                """if timp[-1]=='z':
                    timp=timp[:-1]
                    timp=int(timp)*24
                elif timp[:-1]=='n':
                    timp=-1
                else:
                    timp = timp[:-1]
                    print(timp)"""
                post.replace('/n',' ')
                clienti.append((url,post,id,timp))
    except:
        failedGroups+=1
print ("=== Selection done ===")

#Getting the new posts
condition=False
url=' '
for client in clienti:
    if url!= client[0]:
        url=client[0]
#    print ("\n")
    post_i= Post(client[0],client[2],client[1])
    if check_if_new(post_i):
        print("Client Nou:")
        condition=True
        print(url)
        print (client[1],"\n",client[2],"\n",client[3])
        print("====================")
        insert_post(post_i)

if condition:
    notification.notify(
        title='Clienti noi',
        message='Posibili noi clienti au postat in grupurile de facebook',
        app_name='PythonScript',
    )

print(failedGroups)
print("====Finished====")
#c.execute('DELETE FROM postari;',)
#conn.commit()
#print(get_all_posts())
conn.close()









