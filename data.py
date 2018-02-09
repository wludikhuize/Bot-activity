import requests, lxml.html 
from bs4 import BeautifulSoup
import re
import datetime, time

def dataCollection(name, pwd):
    # Login
    r = requests.session()

    # Getting all Hidden tags
    login_url = 'https://www.ros-bot.com/user/login'
    login = r.get(login_url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

    form['name'] = name
    form['pass'] = pwd
    response = r.post(login_url, data=form)
    
    # Feedback
    if response.url == login_url:
        print ("Error")
    else:
        print ("Login succesful")
    
    # Gathering the route for /user/[id]/bot-activity
    soup = BeautifulSoup(response.text, "lxml")
    a = str(soup.select_one("a[href*=/bot-activity]"))
    id_ = re.search('<a href="(.*)">Bot activity</a>', a)
    activity_route = 'https://www.ros-bot.com%s?item_destination=2&item_quality=All&ancient=All' % (id_.group(1), )
    # activity_route = 'https://www.ros-bot.com%s' % (id_.group(1), )
    
    # Gathering data
    sauce = r.get(activity_route)
    soup = BeautifulSoup(sauce.text, 'lxml')
    
    # date & time
    time_ago_index = dict()
    count = 0
    for t in soup.find_all('small'):
        time_ago = re.findall(r'[0-9]{1,2}\s[(min)|(hours)]{3,5}\s[0-9]{1,2}\s[(min\sago)|(ssec\sago)]{7}', t.text)
        try:
            time_ago_index[count] = time_ago[0]
        except IndexError:
            pass
        count += 1

    today_date = datetime.date.today()
    date = today_date.strftime('%d/%m/%y')

    # Item
    # - title
    item_title_index = dict()
    count = 0
    # for item in soup.find_all('span', attrs={'data-content': True}):
    #     print(item[0])
    # print(item_title_index)

    items = soup.find_all('span', attrs={'data-content': True})
    item = items[0]
    item = str(item['data-content'])

    print(item.replace('<br />', ''))
    

            
   
   
   
   
   
   
   
   
   
   

    # for d in range(len(item_title_index)):
    #     print("%s - %s %s" % (date, time_ago_index[d],item_title_index[d], ))
    # >>> <strong class="text-Primal">[Primal ancient]</strong> dayntee's binding
    # for item in soup.find_all('span', attrs={'data-content': True}):
    #     item = item.string
    #     print(item)