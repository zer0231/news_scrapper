from nepali_unicode_converter.convert import Converter
import requests
import json

converter = Converter()

base_url = "https://bg.annapurnapost.com/api/search?title="
search_term = str(input("Enter a subject to search\n>"))
encoded_search_term = converter.convert(search_term)
search_term = search_term.replace(" ","_")


def extract_news(json_text):
    newslist = json.loads(json_text)
    newsitem = []
    try:
        news = newslist["data"]["items"]
    except:
        print("Not found")
        return newsitem
    for i in news:
        newsitem.append(i)
    return newsitem

def save_page_no(search_term,page_number):
    file = open(search_term+"_page","w")
    file.write(str(page_number))
    file.close

def retrive_page_no(search_term):
    try:
        file = open(search_term+"_page","r")
        page_number = file.read()
        file.close()
    except:
        print("ERrro")
        page_number = 0
        save_page_no(search_term,"0")
    return page_number


def write_json(search_term,news_list):
    file_obj = open(search_term+".json","w",encoding="utf-8")
    news_list = json.dumps(news_list, indent=4)
    file_obj.write(news_list)
    file_obj.close

def read_json(search_term):
    file_obj = open(search_term+".json","r",encoding="utf-8")
    file_content = file_obj.read()
    file_obj.close()
    if file_content == "":
        return ""
    else:
        return file_content


page = 1
news_list = []
skip_this = False
previous_page = int(retrive_page_no(search_term))
print(previous_page)
while page < 4:
    if previous_page == 3:
        skip_this = True
        break

    request_url = base_url+""+encoded_search_term+"&page="+str(page)
    
    try:
        news_list=json.loads(read_json(search_term))
        if len(news_list) < 30 and previous_page < 3:
            print("Continuing . . .")
            page = 2
        if len(news_list) > 30 and previous_page == 1:
            page = 500
            break
        
    except:
        print("result found:")
    
   
    json_text = requests.get(request_url).text
    news_list = news_list+extract_news(json_text)
    save_page_no(search_term,page)
    page = page + 1
    if len(news_list) == 0:
        break

    
if skip_this == False:
     write_json(search_term,news_list)
   

if len(news_list) == 30:
    print("We got 30 article")
elif page == 500 or skip_this:
    print("already got 30 newsarticle")
else:
    print("Sorry couldnt find please try again")
