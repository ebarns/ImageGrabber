# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:17:18 2017

@author: erikb
"""

import nltk
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler, GreedyImageCrawler

class NounParser:

    def parse(self, sentence):
        nouns = []
        word_tokens = nltk.tag.pos_tag(nltk.word_tokenize(sentence))
        #if the word is a noun of pural noun add to list
        for word_tuple in word_tokens:
            if word_tuple[1] == 'NN' or word_tuple[1] == 'NS':
                nouns.append(word_tuple[0])
                
        return nouns
                
        
class Crawler:
    def __init__(self, width=800, height=600, num_pics = 10):
        self.min_height = height
        self.min_width = width
        self.num_of_images = num_pics
        
    def setMinResolution(self, min_width, min_height):
        self.min_width = min_width
        self.min_height = min_height
    
    def setNumOfImages(self, num):
        self.num_of_images = num
    
    def getImagesFromDomain(self, query, domain_url, num_pics): 
        greedy_crawler = GreedyImageCrawler()
        greedy_crawler.crawl(domains=domain_url, max_num=self.num_of_images,
                     min_size=(self.min_width,self.min_height), max_size=None)
    
    def Search(self, query):
        print("Using Google as a Default Implementation")
    
class GoogleSearch(Crawler):
    def __init__(self, width, height, num_pics):
        Crawler.__init__(self, width, height)
        
    def Search(self, query):
        self.getImagesFromGoogle(query)
        
    def getImagesFromGoogle(self, query):
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, storage={'root_dir': query+"_images"})
        google_crawler.crawl(keyword=query, max_num=self.num_of_images,
                             date_min=None, date_max=None,
                             min_size=(self.min_width,self.min_height), max_size=None)
class BingSearch(Crawler):
    def __init__(self, width, height, num_pics):
        Crawler.__init__(self, width, height)
        
    def Search(self, query):
        self.getImagesFromBing(query)
        
    def getImagesFromBing(self, query):                     
        bing_crawler = BingImageCrawler(downloader_threads=4)
        bing_crawler.crawl(keyword=query, offset=0, max_num=self.num_of_images,
                   min_size=(self.min_width,self.min_height), max_size=None)
                   
class BaiduSearch(Crawler):
    def __init__(self, width, height, num_pics):
        Crawler.__init__(self, width, height)
        
    def Search(self, query):
        self.getImagesFromBaidu(query)
        
    def getImagesFromBaidu(self, query):
        baidu_crawler = BaiduImageCrawler()
        baidu_crawler.crawl(keyword=query, offset=0, max_num=self.num_of_images,
                    min_size=(self.min_width,self.min_height), max_size=None)


class Main:
    def __init__(self):
        self.noun_parser = NounParser()
        self.crawler = Crawler()
        self.image_height = 600
        self.image_width = 800
        self.num_pics = 10
        self.keep_searching = True
        #CONSTANTS    
        self.GOOGLE = 1
        self.BING = 2
        self.BAIDU = 3
        self.DOMAINSEARCH = 4
        
    def getInputOption(self):
        return int(input(" [1] Search Google \n [2] Search Baidu \n [3] Search Bing \n [4] Search URL Domain \n [5] STOP \n" + \
            "[6] Change Settings"))
    
    def setSettings(self):
        choice = int(raw_input(" [1] Set min resolution \n [2] Set number of pictures per noun \n"))
        if(choice == 1):
            self.width = int(raw_input("Min width: "))
            self.height = int(raw_input("Min height: "))
        elif(choice == 2):
            self.num_pics = int(raw_input("Number of pictures per noun: "))
        else:
            print("Enter a correct number")
    
    def handleSearch(self, search_engine, nouns, domain=""):
        if(search_engine == self.GOOGLE):
            self.crawler = GoogleSearch(self.width, self.height, self.num_pics)
        elif(search_engine == self.BING):
            self.crawler = BingSearch(self.width, self.height, self.num_pics)
        elif(search_engine == self.BAIDU):
            self.crawler = BaiduSearch(self.width, self.height, self.num_pics)
        else: #breaking point
            num_pics = int(raw_input("Number of pictures: "))
            self.crawler.getImagesFromDomain(nouns, domain, num_pics)
            return
        
        for noun in nouns:
            self.crawler.Search(noun)
        
    
    def main(self):
        while self.keep_searching:
            option = self.getInputOption()
            domain = ""
            if(option == 4):
                domain = raw_input("Enter a URL to search: ")
                
            if(option <= 4): #searching for images 
                query = raw_input("Enter a sentence: ")
                nouns = self.noun_parser.parse(query)
                self.handleSearch(option, nouns, domain)
            else:
                print("STOPPING - LATER")
                self.keep_searching = False
            

i = Main()
i.main()