"""
Author: Maximilien Zaleski © 2018

"""

import requests, lxml.html, re, datetime, time
from bs4 import BeautifulSoup

def dataCollection(name, pwd):
    # ==== Login ====
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
    # activity_route = 'https://www.ros-bot.com%s' % (id_.group(1), )
    
    # ============ Gathering data ============ 
    sauce = r.get(activity_route)
    soup = BeautifulSoup(sauce.text, 'lxml')
    
    number_of_rows = soup.find_all('div', class_="timeline-item")
    counter = len(number_of_rows)

    # ==== date & time ====
    time_ago_index = dict()
    
    count = 0
    for t in soup.find_all('small'):
        time_ago = re.findall(r'[0-9]{1,2}\s[(min)|(hours)|(day)]{3,5}\s[0-9]{1,2}\s[(min\sago)|(ssec\sago)]{7}', t.text)
        try:
            time_ago_index[count] = time_ago[0]
            
            count += 1
        
        except IndexError:
            pass

    today_date = datetime.date.today()
    date = today_date.strftime('%d/%m/%y')

    # ==== Items ====
    
    # - name & type
    item_name_index = dict()
    
    count = 0
    for item_name in soup.find_all('span', attrs={'data-content': True}):
        stong_tag = item_name.find_all('strong', class_='text-Primal')
        item_type = item_name['class']
        
        item_name = item_name.text
        try:
            item_name = re.search('ncient.\s(.*)', item_name)
            item_name = item_name.group(1)
    
            # if item_type == 'text-Legendary':
            #     item_name_index[count] = item_name.capitalize(), 'ancient'

            # elif item_type == 'text-Set':
            #     item_name_index[count] = item_name.capitalize(), 'set'
            
            # elif item_type == 'text-Primal':
            #     item_name_index[count] = item_name.capitalize(), 'primal'

            count += 1
        
        except AttributeError:
            pass 
        
    # print(item_name_index)
    
    # - Stats
    item_PrimaryStats_index = dict()
    item_SecondaryStats_index = dict()
    
    count = 0
    for stats in soup.find_all('span', attrs={'data-content': True}):
        stats = str(stats['data-content']).replace('<br />', '')
        try: 
            stats = re.search('Primary(.*)Secondary(.*)', stats, re.DOTALL)
            
            primary_stats = stats.group(1)
            item_PrimaryStats_index[count] = primary_stats
            
            secondary_stats = stats.group(2)
            item_SecondaryStats_index[count] = secondary_stats
            
            count += 1

        except AttributeError:
            pass
  
    # class Item ()
    #     def __init__(name, type, index):
            





