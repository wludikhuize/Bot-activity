"""
Author: Maximilien Zaleski © 2018

"""

import requests, lxml.html, re, datetime, time
from bs4 import BeautifulSoup

class Item (object):
    def __init__(self, name, type_, primary, secondary, time, date):
        self.name = name
        self.type_ = type_
        self.primary = primary
        self.secondary = secondary
        self.time = time
        self.date = date
            
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
        Each data type is sorted into a dictionary with it's index key. The idea is to loop through every single dict and assign all the data to the object values. 
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

    # # ==== Items ====
    
    # # - name & type
    # item_name_index = dict()
    # item_type_index = dict()
    
    # count = 0
    # for item_name in soup.find_all('span', attrs={'data-content': True}):
    #     strong_tag = item_name.find_all('strong', class_='text-Primal')
    #     item_type = item_name['class']
        
    #     item_name = item_name.text
    #     try:
    #         item_name = re.search('ncient.\s(.*)', item_name)
    #         item_name = item_name.group(1)
    #         item_name_index[count] = item_name

    #         if strong_tag:
    #             item_type_index[count] = "primal"
    #         elif item_type[0] == "text-Legendary":
    #             item_type_index[count] = "legendary"
    #         elif item_type[0] == "text-Set":
    #             item_type_index[count] = "set"
            
    #         count += 1
        
    #     except AttributeError:
    #         pass 


    # # print(item_name_index, item_type_index)
            
        
    # # print(item_name_index)
    
    # # - Stats
    # item_PrimaryStats_index = dict()
    # item_SecondaryStats_index = dict()
    
    # count = 0
    # for stats in soup.find_all('span', attrs={'data-content': True}):
    #     stats = str(stats['data-content']).replace('<br />', '')
        
    #     try: 
    #         stats = re.search('Primary(.*)Secondary(.*)', stats, re.DOTALL)
            
    #         primary_stats = stats.group(1)
    #         item_PrimaryStats_index[count] = primary_stats
            
    #         secondary_stats = stats.group(2)
    #         item_SecondaryStats_index[count] = secondary_stats
            
    #         count += 1

            

    #     except AttributeError:
    #         pass
  






