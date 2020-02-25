# -*- coding: UTF-8 -*-
# @Author  : ERROR404
# @Version  : 1.0
import requests,os,ssl,html,urllib.request,time,shutil

ssl._create_default_https_context = ssl._create_unverified_context
DEBUG = False # 将此处置位将会输出部分except的异常详细信息！

Headers={
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'adworld.xctf.org.cn',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'X-CSRF-Token': ''
}

Cookies={
    'session':'',
    'X-CSRF-Token':''
}

def save_file(url,Problem_file_path,file_url):
    try:
        urllib.request.urlretrieve(url + file_url, os.path.expanduser(Problem_file_path))
        return True
    except Exception as e:
        if DEBUG:
            print(e)
        return False

def get_filename(url):
    file_name = ''
    for character in url[::-1]:
        if character == '/':
            return file_name
        if character == '?':
            file_name = ''
            continue
        file_name = character + file_name

def Check_and_make_dir(dir_path):
    if (os.path.exists(os.path.expanduser(dir_path))):
        pass
    else:
        os.makedirs(os.path.expanduser(dir_path), exist_ok=True)
        Log_content  = '[!]创建了新目录: %s !\n' % ( dir_path )
        print('\033[0;33m' + '[!]创建了新目录: %s !' % ( dir_path ) + '\033[0m')

def Save(race_name,evt):
    Log_content  = '本程序在 %s 启动，开始自动储存题目!\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
    save_success_num = 0
    race_path = '~/Desktop/CTF_question/' + race_name + '/'

    try:
        detail_API_url = 'https://adworld.xctf.org.cn/api/evts/challenges?evt=' + evt
        All_detail = requests.get(detail_API_url,headers=Headers,cookies=Cookies)
        category_list = All_detail.json()['rows'][0].keys()
    except Exception as e:
        if DEBUG:
            print(e)
        print('\033[0;31m' + '[-] 与服务器链接失败或服务器返回值异常!请检查Cookie或URL是否正确设置!' + '\033[0m')
        exit(0)

    Log_content += '[+] 当前已放出 %d 道题目，存储就绪!\n' % ( All_detail.json()['total'] )
    print('\033[0;33m' + '[+] 当前已放出 %d 道题目，存储就绪!' % ( All_detail.json()['total'] ) + '\033[0m')

    for category in category_list:
        category_path = race_path + category + '/'
        Check_and_make_dir(category_path)

        challenge_list = All_detail.json()['rows'][0][category]
        for challenge in challenge_list:
            upgrade = False
            challenge_path = category_path + challenge['task']['title'] + '/'
            Check_and_make_dir(challenge_path)

            challenge_exist_file_path = challenge_path + 'Auto_save.flag'
            description_file_path = challenge_path + '题目描述.txt'
            if os.path.exists(os.path.expanduser(description_file_path)):
                if os.path.exists(os.path.expanduser(challenge_exist_file_path)):
                    Log_content += '[-] 题目 %s 已存在!\n' % (challenge['task']['title'])
                    print('\033[0;31m' + '[-] 题目 %s 已存在!' % (challenge['task']['title']) + '\033[0m')
                    continue
                else:
                    Log_content += '[!] 题目 %s 已存在,但标志文件丢失，开始更新题目描述!\n' % (challenge['task']['title'])
                    upgrade = True
                    print('\033[0;33m' + '[!] 题目 %s 已存在,但标志文件丢失，开始更新题目描述!' % (challenge['task']['title']) + '\033[0m')
            
            Log_content += '[!] 开始写入题目 %s 的题目描述!\n' % (challenge['task']['title'])
            print('\033[0;33m' + '[!] 开始写入题目 %s 的题目描述!' % (challenge['task']['title']) + '\033[0m')
            try:
                description_file = open(os.path.expanduser(description_file_path),'w')
                description_file.write(html.unescape(challenge['task']['content']))
                Log_content += '[!] 题目 %s 的题目描述写入成功!\n' % (challenge['task']['title'])
                print('\033[0;32m' + '[!] 题目 %s 的题目描述写入成功!' % (challenge['task']['title']) + '\033[0m')
                description_file.close()
            except Exception as e:
                if DEBUG:
                    print(e)
                shutil.rmtree(os.path.expanduser(challenge_path))
                Log_content += '[-] 题目 %s 的题目描述写入失败!题目文件夹已被清除!\n' % (challenge['task']['title'])
                print('\033[0;31m' + '[-] 题目 %s 的题目描述写入失败!题目文件夹已被清除!' % (challenge['task']['title']) + '\033[0m')
                Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,challenge['task']['title'])
                print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,challenge['task']['title']) + '\033[0m')
                continue
            
            if len(challenge['notice']) != 0:
                hint_file_path = challenge_path + 'Hint.txt'
                Log_content += '[!] 开始写入题目 %s 的Hint!\n' % (challenge['task']['title'])
                print('\033[0;33m' + '[!] 开始写入题目 %s 的Hint!' % (challenge['task']['title']) + '\033[0m')
                try:
                    hint_file = open(os.path.expanduser(hint_file_path),'w')
                    notice_text = ""
                    for notice in challenge['notice']:
                        notice_text += notice + '\n'
                    hint_file.write(html.unescape(notice_text))
                    Log_content += '[!] 题目 %s 的Hint写入成功!\n' % (challenge['task']['title'])
                    print('\033[0;32m' + '[!] 题目 %s 的Hint写入成功!' % (challenge['task']['title']) + '\033[0m')
                    description_file.close()
                except Exception as e:
                    if DEBUG:
                        print(e)
                    shutil.rmtree(os.path.expanduser(challenge_path))
                    Log_content += '[-] 题目 %s 的Hint写入失败!题目文件夹已被清除!\n' % (challenge['task']['title'])
                    print('\033[0;31m' + '[-] 题目 %s 的Hint写入失败!题目文件夹已被清除!' % (challenge['task']['title']) + '\033[0m')
                    Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,challenge['task']['title'])
                    print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,challenge['task']['title']) + '\033[0m')
                    continue
            
            if len(challenge['task']['file']) != 0 and upgrade == False:
                file_url = 'https://adworld.xctf.org.cn/'
                remaining_file_number = len(challenge['task']['file'])
                Log_content += '[!] 题目 %s 共计有 %d 个附件!\n' % (challenge['task']['title'],remaining_file_number)
                print('\033[0;33m' + '[!] 题目 %s 共计有 %d 个附件!' % (challenge['task']['title'],remaining_file_number) + '\033[0m')
                for index in range(remaining_file_number):
                    Log_content += '[!] 开始存储题目 %s 的第 %d 个附件!\n' % (challenge['task']['title'],remaining_file_number)
                    print('\033[0;33m' + '[!] 开始存储题目 %s 的第 %d 个附件!' % (challenge['task']['title'],remaining_file_number) + '\033[0m')
                    if (save_file(file_url,challenge_path + '/' + get_filename(challenge['task']['file'][index]),challenge['task']['file'][index])):
                        Log_content += '[!] 题目 %s 的第 %d 个附件存储成功!\n' % (challenge['task']['title'],index+1)
                        print('\033[0;32m' + '[!] 题目 %s 的第 %d 个附件存储成功!' % (challenge['task']['title'],index+1) + '\033[0m')
                        Save_fail = False
                    else:
                        shutil.rmtree(os.path.expanduser(challenge_path))
                        Log_content += '[!] 题目 %s 的第 %d 个附件存储失败!题目文件夹已被清除!!\n' % (challenge['task']['title'],index+1)
                        print('\033[0;31m' + '[!] 题目 %s 的第 %d 个附件存储失败!题目文件夹已被清除!' % (challenge['task']['title'],index+1) + '\033[0m')
                        Save_fail = True
                        break
                if Save_fail :
                    Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,challenge['task']['title'])
                    print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,challenge['task']['title']) + '\033[0m')
                    continue
            try:
                challenge_exist_file = open(os.path.expanduser(challenge_exist_file_path),'w')
                challenge_exist_file.write("此文件由自动存题脚本生成，如需更新题目描述，请删除本文件！")
                challenge_exist_file.close()
            except Exception as e:
                if DEBUG:
                    print(e)
                shutil.rmtree(os.path.expanduser(challenge_path))
                Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,challenge['task']['title'])
                print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,challenge['task']['title']) + '\033[0m')
                continue

    Log_content += '本程序在 %s 成功存储了 %d 道题目。\n\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),save_success_num)
    Log_file_path = '~/Desktop/CTF_question/' + race_name + '/Auto_Save_Result.txt'
    Log_file = open(os.path.expanduser(Log_file_path),'a')
    Log_file.write(Log_content)
    print('\033[0;32m' + '[+]ALL Done!' + '\033[0m')
        

if __name__ == "__main__": 
    print('\033[0;32m' + '欢迎使用由 ERROR404 开发的自动存题脚本~' + '\033[0m')
    print('\033[0;32m' + '如遇任何问题或有建议欢迎在Github提issue~' + '\033[0m')

    #以下为用户预定义部分↓
    # 你打算把本赛事的题目丢到哪个文件夹去呢~
    race_name = ''
    # 请从浏览器获取该字段然后填在这里哦~
    Headers['X-CSRF-Token'] = ''
    Cookies['session'] = ''
    Cookies['X-CSRF-Token'] = Headers['X-CSRF-Token']
    evt = ''
    #以上为用户预定义部分↑

    if race_name != '' and Headers['X-CSRF-Token'] != '' and evt != '':
        print('\033[0;32m' + '[+]现在开始自动化存储 ' + race_name + '的题目!' + '\033[0m')
        Save(race_name,evt)
    else :
        print('\033[0;33m' + '[-]程序缺少关键参数!请检查源码中的用户预定义部分是否填写完毕!' + '\033[0m')