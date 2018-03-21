import urllib
import expanddouban
import requests
import time
from bs4 import BeautifulSoup
from lxml import etree
import os

#define a class
class Movie:
    def __init__(self,name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link


"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category, location)
    return url


"""
return a list of Movie objects with the given category and location.
"""
def getMovies(movie):
    array = []
    record = []
    array.append(movie.name)
    array.append(movie.rate)
    array.append(movie.location)
    array.append(movie.category)
    array.append(movie.info_link)
    array.append(movie.cover_link)
    record.append(array)
    return record

def crawl_Douban(drama_types,countrys):
    drama_mov = []
    roman_mov = []
    come_mov = []
    index = 0
    ranking = []
    dataFilePath = "E:\jnu\year 2 sem B\Project2-Crawling\ movies.csv"
    resultFilePath = "E:\jnu\year 2 sem B\Project2-Crawling\ movies.csv"
    outputFile = "E:\jnu\year 2 sem B\Project2-Crawling\ output.txt"

    # find the data from these country about three types of movie
    for j in range(len(drama_types)):
        for i in range(len(countrys)):
            url_need = []           #存电影 store the movie
            html = expanddouban.getHtml(getMovieUrl(drama_types[j], countrys[i]))
            soup = BeautifulSoup(html)
            for link in soup.find_all('a', {'class': 'item'}):
                info_link = link.get('href')
                a = link.find('div',{'class': 'cover-wp'}).find('span', {'class': 'pic'}).find('img')
                cover_link = a.get('src')
                name = a.get('alt')
                rate = link.find('p').find('span', {'class': 'rate'}).contents
                m = Movie(name,rate,countrys[i],drama_types[j],info_link,cover_link)
                url_need.append(getMovies(m))
            if index == 0:  #这是剧情类drama
                if countrys[i] != countrys[-1]:  #last one country
                    drama_mov.append(url_need)
                else:
                    drama_mov.append(url_need)
                    index += 1
            elif index == 1:   #爱情love
                if countrys[i] != countrys[-1]:  # last one country
                    roman_mov.append(url_need)
                else:
                    roman_mov.append(url_need)
                    index += 1
            elif index == 2:   #comedy type
                if countrys[i] != countrys[-1]:  # last one country
                    come_mov.append(url_need)
                else:
                    come_mov.append(url_need)
                    index += 1
    url_need = []
    url_need.append(drama_mov)
    url_need.append(roman_mov)
    url_need.append(come_mov)
    write_result(url_need,resultFilePath)

    


def sum_each_type(read_file):
    array = [0, 0, 0]
    for line in read_file:
        if line.find('剧情'):
            print(line)
            array[0] += 1
        elif line.find('爱情'):
            print(line)
            array[1] += 1
        elif line.find('喜剧'):
            print(line)
            array[2] += 1

    return array

def read_line(file_path):
    if os.path.exists(file_path):
            array = []
            with open(file_path, 'r') as lines:
                for line in lines:
                    array.append(line)
            return array
    else:
        print('file not exist: ' + file_path)
        return None

def write_result(array, outputFilePath):
    with open(outputFilePath, 'w') as output_file:
        for item in array:   #1st type
            for i in item:    #1st country
                for j in i:    #1st movie
                    output_file.write("%s\n" % j)



""" ranking 1st 2nd 3rd"""
def rank(type_arrays):
    dict_num = {}
    rank_country = []

    #dict_num = sum_movie(type_arrays)
    for elements in dict_num:
        count1 = 0
        count2 = 0
        count3 = 0
        for element in elements:   #每种类型所有国家电影数量第一多
            if elements[element] > count1:
                count1 = elements[element]
        rank_country.append(element)    #add champion to list
        for element in elements:        #每类型所有国家电影数量第二多
            if elements[element] > count2 and elements[element] < count1:
                count2 = elements[element]
        rank_country.append(element)     #2nd to list
        for element in elements:        #每类型所有国家电影数量第三多
            if elements[element] > count3 and elements[element] < count2:
                count3 = elements[element]
        rank_country.append(element)    #3rd to list

    return rank_country



#country's list
countrys = ["大陆", "美国", "香港", "台湾", "日本", "韩国", "英国", "法国", "德国", "意大利", "西班牙", "印度", "泰国", "俄罗斯", "伊朗", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]
test = ["大陆", "美国", "香港", "台湾"]
#type list
drama_types = ["剧情","爱情","喜剧"]



#crawl_Douban(drama_types,test)

array = read_line("E:\jnu\year 2 sem B\Project2-Crawling\ movies.csv")

print(sum_each_type(array))