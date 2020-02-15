#coding:utf-8
import requests
import urllib.request
import os
import ssl
import html
ssl._create_default_https_context = ssl._create_unverified_context

headers={
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc19hZG1pbiI6ZmFsc2UsInN1YiI6MTEwOSwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo2NTUzNS9UZWFtL2luZm8iLCJpYXQiOjE1ODA5ODkwNjQsImV4cCI6MTU4MDk5NDkwMSwibmJmIjoxNTgwOTkxMzAxLCJqdGkiOiI4eFcyd1FTTXhVSWhIQmtsIn0._JxOpc6e3_1uA--KyJ_-J46SvalhvodkLxEFZvh7p6c',
    'referer': 'https://hgame.vidar.club/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
cookies={
    'laravel_session':'eyJpdiI6Imk4RGpBZEtPT0lEbjhHMWc5Mk13NWc9PSIsInZhbHVlIjoieU5lRWRzNklPNjdvNkM0d1NQQUducmg5OHRGMTJIOGdoWFlqcG82OTlkU2VYZWZPUDZ4RWVBbm5QakRCOGwxViIsIm1hYyI6IjU3MzZhMTJlNmRhZjdhZDhmYmRkYmIyMzljZDdlZjc4MDkxMjMwNjNjNTcyZTE0MzVmNTQ5NDU1NDJjODk4YzAifQ%3D%3D'
}
url='https://hgame.vidar.club/API/Challenge/list?language=en'
Problem_list=requests.get(url,headers=headers,cookies=cookies)

def Pwn_save(week):
    dir_path = './' + week + '/Pwn/'
    for Problem in Problem_list.json()['data']['challenges']['Pwn'][week]:
        Problem_path = dir_path + Problem['title']
        if os.path.exists(Problem_path):
            pass
        else:
            os.makedirs(Problem_path, exist_ok=True)
        Problem_description_file_path=Problem_path + '/题目描述.txt'
        print(Problem_description_file_path)
        Problem_description_file = open(Problem_description_file_path,'w')
        Problem_description_file.write(html.unescape(Problem['description']))
        Problem_file_name = Problem_path + '/' + Problem['title']
        urllib.request.urlretrieve(Problem['url'], Problem_file_name)

def Misc_save(week):
    dir_path = './' + week + '/Misc/'
    for Problem in Problem_list.json()['data']['challenges']['Misc'][week]:
        Problem_path = dir_path + Problem['title']
        if os.path.exists(Problem_path):
            pass
        else:
            os.makedirs(Problem_path, exist_ok=True)
        Problem_description_file_path=Problem_path + '/题目描述.txt'
        print(Problem_description_file_path)
        Problem_description_file = open(Problem_description_file_path,'w')
        Problem_description_file.write(html.unescape(Problem['description']))
        Problem_file_name = Problem_path + '/' + Problem['title']
        urllib.request.urlretrieve(Problem['url'], Problem_file_name)

def Crypto_save(week):
    dir_path = './' + week + '/Crypto/'
    for Problem in Problem_list.json()['data']['challenges']['Crypto'][week]:
        Problem_path = dir_path + Problem['title']
        if os.path.exists(Problem_path):
            pass
        else:
            os.makedirs(Problem_path, exist_ok=True)
        Problem_description_file_path=Problem_path + '/题目描述.txt'
        print(Problem_description_file_path)
        Problem_description_file = open(Problem_description_file_path,'w')
        Problem_description_file.write(html.unescape(Problem['description']))
        Problem_file_name = Problem_path + '/' + Problem['title']
        urllib.request.urlretrieve(Problem['url'], Problem_file_name)

def Reverse_save(week):
    dir_path = './' + week + '/Reverse/'
    for Problem in Problem_list.json()['data']['challenges']['Reverse'][week]:
        Problem_path = dir_path + Problem['title']
        if os.path.exists(Problem_path):
            pass
        else:
            os.makedirs(Problem_path, exist_ok=True)
        Problem_description_file_path=Problem_path + '/题目描述.txt'
        print(Problem_description_file_path)
        Problem_description_file = open(Problem_description_file_path,'w')
        Problem_description_file.write(html.unescape(Problem['description']))
        Problem_file_name = Problem_path + '/' + Problem['title']
        urllib.request.urlretrieve(Problem['url'], Problem_file_name)

try:
    # Pwn_save('Week1')
    # Misc_save('Week1')
    # Crypto_save('Week1')
    # Reverse_save('Week1')
    # Pwn_save('Week2')
    # Misc_save('Week2')
    # Crypto_save('Week2')
    # Reverse_save('Week2')
    # Pwn_save('Week3')
    # Misc_save('Week3')
    # Crypto_save('Week3')
    # Reverse_save('Week3')
    Pwn_save('Week4')
    Misc_save('Week4')
    Crypto_save('Week4')
    Reverse_save('Week4')
except:
    pass
