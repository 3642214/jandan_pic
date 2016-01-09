#!/usr/bin/python
#-*-coding:utf-8-*-

import urllib,urllib2,re,time,random,os
from BeautifulSoup import BeautifulSoup

class picInfo:
    
    def __init__(self,soup,id):
        if soup is None:
            return
        else:
            self.__author = ""
            self.__url = []
            self.__text = ""
            self.__vote = {"oo":0,"xx":0,"comment":0}

            self.__id = id
            self.__setAuthor(soup)
            self.__setUrl(soup)
            self.__setText(soup)
            self.__setVote(soup)

    def __setAuthor(self,soup):
        self.__author = soup.find('strong').string
#        print "author:",self.__author

    def __setUrl(self,soup):
        urls = soup.find('div',attrs={"class":"text"})\
                   .findAll('a',attrs={"class":"view_img_link"})
        for url in urls:
            self.__url.append(url['href'])
#        print "pic url:",self.__url

    def __setText(self,soup):
        text = soup.find('div',attrs={"class":"text"})\
                    .find('p')
        self.__text = text.string
#        print "text:",self.__text

    def __setVote(self,soup):        
        self.__vote['oo'] = soup.find('span',id="cos_support-"+str(self.__id)).string
        self.__vote['xx'] =  soup.find('span',id="cos_unsupport-"+str(self.__id)).string
        self.__vote['comment'] = soup.find('span',attrs={"class":"ds-thread-count"})
#        print "vote:",self.__vote

    def getVote(self):
        return self.__vote

    def getUrl(self):
        return self.__url

class analyzeHTML:
    last_page = 0
    current_page = 0
    current_page_html = None
    picList = []

    def __init__(self):
        self.getHTML(None)

    def getHTML(self,page):
        user_agent = ['User-Agent:Mozilla/5.0',\
                      'User-Agent:AppleWebKit/537.36 (KHTML, like Gecko)',\
                      'User-Agent:Chrome/45.0.2454.101 Safari/537.36',\
                      'User-Agent:Mozilla/5.0',\
                      'User-Agent:Mozilla/3.1',\
                      'User-Agent:Mozilla/3.3',\
                      'User-Agent:Mozilla/3.4',\
                      'User-Agent:Mozilla/5.1',\
                      'User-Agent:Mozilla/5.2',\
                      'User-Agent:Mozilla/4.0'] 
        headers = { 'User-Agent' : random.choice(user_agent)} 
        if page is None:
            url = 'http://jandan.net/pic'                                   
        else:
            url = 'http://jandan.net/pic/page-' + str(page) + '#comments'
        response = urllib2.urlopen(urllib2.Request(url,headers=headers))
        self.current_page_html = response.read()
        self.getCurrentPage()
        if page is None:
            self.last_page = self.current_page

    def getCurrentPage(self):
        soup = BeautifulSoup(self.current_page_html)
        self.current_page = soup.find(name='span',attrs={"class":"current-comment-page"}).string[1:-1]
        print "current_page=",self.current_page 

    def getPageAllCommentID(self):
        soup = BeautifulSoup(self.current_page_html)
        for comment in soup.findAll('li'):
            id = re.sub(r'\D',"",str(comment.get('id')))
            if id is not "":
#                print "id=",id
                pic_info = picInfo(comment,id)
#                print " ",pic_info
                if int(pic_info.getVote()['oo']) > 300:
                    self.picList.append(pic_info)


if __name__ == '__main__':             
   s = analyzeHTML()
   page = int(s.current_page)
   while page > 8180:
       page = page - 1
       print page
       s.getPageAllCommentID()
       s.getHTML(page)
#       time.sleep(3)
 
#   print s.picList

   for picurls in s.picList:
       for picurl in picurls.getUrl():
           os.system('wget ' + str(picurl))
#           urllib.urlretrieve(picurl,str(picurl))


