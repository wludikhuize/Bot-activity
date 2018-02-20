"""
Author: Maximilien Zaleski © 2018

"""

import requests, lxml.html, re, datetime, time
from bs4 import BeautifulSoup

class Item (object):
    def __init__(self, name, type_, primary, secondary):
        self.name = name
        self.type_ = type_
        self.primary = primary
        self.secondary = secondary
        # self.time = time
        # self.date = date

items = list()
            
def dataCollection(name, pwd):
    '''
    This function retreives the name, type, date, time, primary, secondary. 
    The object *name of item from timeline* is then created and placed into a list 'timeline_items'.

    Code structure
        1. Find all <span> tags with <strong> child-tag
            <strong>Ancient/Primal ancient<strong> name = type_
        class=text-Legendary/text-Set/text-Primal = item_class
            - Frontend: we can assign the proper colours for earch

        2.  We starts the data gathering.
        For earch span tag, we retreive the data-content attribute. We devide said attribute by primary & secondary stats. 

        3. We sort the data.
    '''
    
    # ============ Login ============
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
    
    try:
        id_ = re.search('<a href="(.*)">Bot activity</a>', a)
    
    except AttributeError:
        pass
    
    activity_route = 'https://www.ros-bot.com%s?item_destination=2&item_quality=All&ancient=All' % (id_.group(1), )
    
    # ============ Gathering data ============ 
    sauce = r.get(activity_route)
    soup = BeautifulSoup(sauce.text, 'lxml')
    span = soup.find_all('span', attrs={'data-content': True})
    
    for s in span:
        if s.findChildren('strong'):
            
            class_tag = s['class'][0]
            print(class_tag)
            stats = str(s['data-content']).replace('<br />', '')
   
    # name & type
            name = s.text
            name = re.search('ncient.\s(.*)', name)
            name = name.group(1)
        
            try:
                strong = s.find('strong')
                strong = strong.text
                
                if class_tag == "text-Set":
                    type_ = "set"
                elif strong == "[Primal ancient]":
                    type_ = "primal" 
                elif strong == "[Ancient]":
                    type_ = "ancient"
                

            except AttributeError:
                pass
   
    # stats - primary & secondary 
            try: 
                stats = re.search('Primary(.*)Secondary(.*)', stats, re.DOTALL)
                
                primary = stats.group(1)
                secondary = stats.group(2)
                
            except AttributeError:
                primary = "N/A"
                secondary = "N/A"

    # time & date
    
    # new Item():
            item = Item(name, type_, primary, secondary)
            items.append(item)

def returnAllValues():
    for i in items:
        print(i.name, i.type_)


    # ================================================================================================================================ #

    # ==== date & time ====
    # time_ago_index = dict()
    
    # count = 0
    # for t in soup.find_all('small'):
    #     time_ago = re.findall(r'[0-9]{1,2}\s[(min)|(hours)|(day)]{3,5}\s[0-9]{1,2}\s[(min\sago)|(ssec\sago)]{7}', t.text)
    #     try:
    #         time_ago_index[count] = time_ago[0]
    #         print(time_ago[0])
            
    #         count += 1
        
    #     except IndexError:
    #         pass

    # today_date = datetime.date.today()
    # date = today_date.strftime('%d/%m/%y')