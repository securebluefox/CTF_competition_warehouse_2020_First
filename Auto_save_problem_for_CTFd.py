# -*- coding: UTF-8 -*-
# @Author   : ERROR404
# @Version  : 1.2
import requests,os,ssl,html,urllib.request,time,shutil

ssl._create_default_https_context = ssl._create_unverified_context
DEBUG = True # 将此处置位将会输出部分except的异常详细信息！
Save_File = True # 您是否想要自动化存储题目附件？

Headers={
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'csrf-token': '6056c8f6b07709306c2a6eae4f366717c2799e5c762da696bbdffd4425428b53'
}

Cookies={
    'session':''
}

def get_Problem(url,Problem_ID):
    API_url = url + '/api/v1/challenges/'+str(Problem_ID)
    problem = requests.get(API_url,headers=Headers,cookies=Cookies)
    return problem.json()['data']

def save_file(url,Problem_file_path,file_url):
    try:
        urllib.request.urlretrieve(url + file_url, os.path.expanduser(Problem_file_path))
        return True
    except Exception as e:
        if DEBUG:
            print(e)
        return False

def Check_and_make_dir(dir_path):
    if (os.path.exists(os.path.expanduser(dir_path))):
        pass
    else:
        os.makedirs(os.path.expanduser(dir_path), exist_ok=True)
        Log_content  = '[!]创建了新目录: %s !\n' % ( dir_path )
        print('\033[0;33m' + '[!]创建了新目录: %s !' % ( dir_path ) + '\033[0m')

def get_filename(url):
    file_name = ''
    for character in url[::-1]:
        if character == '/':
            return file_name
        if character == '?':
            file_name = ''
            continue
        file_name = character + file_name

def Save(url,race_name):
    Log_content  = '本程序在 %s 启动，开始自动储存题目!\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
    save_success_num = 0

    if not save_file:
        Log_content += '[!] 本次存储中，附件存储功能已关闭！这将极大地提升存储速度，您需要稍后手动存储附件！'
        print('\033[0;31m' + '[!] 本次存储中，附件存储功能已关闭！这将极大地提升存储速度，您需要稍后手动存储附件！' + '\033[0m')

    race_path = '~/Desktop/CTF_question/' + race_name + '/'

    try:
        API_url = url + 'api/v1/challenges'
        All_challenges = requests.get(API_url,headers=Headers,cookies=Cookies)
        challenges_list = All_challenges.json()['data']
    except Exception as e:
        if DEBUG:
            print(e)
        if( ('message' in All_challenges.json().keys()) and (All_challenges.json()['message'] == 'You don\'t have the permission to access the requested resource. It is either read-protected or not readable by the server.') ):
            print('\033[0;31m' + '[-] 已与服务器建立链接!但比赛仍未开始!' + '\033[0m')
        else:
            print('\033[0;31m' + '[-] 与服务器链接失败或服务器返回值异常!请检查Cookie或URL是否正确设置!' + '\033[0m')
        exit(0)

    for challenges in challenges_list:
        problem = get_Problem(url,challenges['id'])
        category = problem['category']
        description = problem['description']
        problem_name = problem['name']

        upgrade = False
        challenge_path = '~/Desktop/CTF_question/' + race_name + '/' + category + '/' + problem_name + '/'
        Check_and_make_dir(challenge_path)

        challenge_exist_file_path = challenge_path + 'Auto_save.flag'
        description_file_path = challenge_path + '题目描述.txt'
        if os.path.exists(os.path.expanduser(description_file_path)):
            if os.path.exists(os.path.expanduser(challenge_exist_file_path)):
                Log_content += '[-] 题目 %s 已存在!\n' % (problem_name)
                print('\033[0;31m' + '[-] 题目 %s 已存在!' % (problem_name) + '\033[0m')
                continue
            else:
                Log_content += '[!] 题目 %s 已存在,但标志文件丢失，开始更新题目描述!\n' % (problem_name)
                upgrade = True
                print('\033[0;33m' + '[!] 题目 %s 已存在,但标志文件丢失，开始更新题目描述!' % (problem_name) + '\033[0m')
        
        Log_content += '[!] 开始写入题目 %s 的题目描述!\n' % (problem_name)
        print('\033[0;33m' + '[!] 开始写入题目 %s 的题目描述!' % (problem_name) + '\033[0m')
        try:
            description_file = open(os.path.expanduser(description_file_path),'w')
            description_file.write(html.unescape(description))
            Log_content += '[!] 题目 %s 的题目描述写入成功!\n' % (problem_name)
            print('\033[0;32m' + '[!] 题目 %s 的题目描述写入成功!' % (problem_name) + '\033[0m')
            description_file.close()
        except Exception as e:
            if DEBUG:
                print(e)
            shutil.rmtree(os.path.expanduser(challenge_path))
            Log_content += '[-] 题目 %s 的题目描述写入失败!题目文件夹已被清除!\n' % (problem_name)
            print('\033[0;31m' + '[-] 题目 %s 的题目描述写入失败!题目文件夹已被清除!' % (problem_name) + '\033[0m')
            Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,problem_name)
            print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,problem_name) + '\033[0m')
            continue

        if len(problem['hints']) != 0:
            hint_file_path = challenge_path + 'Hint.txt'
            Log_content += '[!] 开始写入题目 %s 的Hint!\n' % (problem_name)
            print('\033[0;33m' + '[!] 开始写入题目 %s 的Hint!' % (problem_name) + '\033[0m')
            try:
                hint_file = open(os.path.expanduser(hint_file_path),'w')
                hint_text = ""
                for hint in problem['hints']:
                    hint_text += hint + '\n'
                hint_file.write(html.unescape(hint_text))
                Log_content += '[!] 题目 %s 的Hint写入成功!\n' % (problem_name)
                print('\033[0;32m' + '[!] 题目 %s 的Hint写入成功!' % (problem_name) + '\033[0m')
                description_file.close()
            except Exception as e:
                if DEBUG:
                    print(e)
                shutil.rmtree(os.path.expanduser(challenge_path))
                Log_content += '[-] 题目 %s 的Hint写入失败!题目文件夹已被清除!\n' % (problem_name)
                print('\033[0;31m' + '[-] 题目 %s 的Hint写入失败!题目文件夹已被清除!' % (problem_name) + '\033[0m')
                Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,problem_name)
                print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,problem_name) + '\033[0m')
                continue

        if save_file:
            if len(problem['files']) != 0 and upgrade == False:
                remaining_file_number = len(problem['files'])
                Log_content += '[!] 题目 %s 共计有 %d 个附件!\n' % (problem_name,remaining_file_number)
                print('\033[0;33m' + '[!] 题目 %s 共计有 %d 个附件!' % (problem_name,remaining_file_number) + '\033[0m')
                for index in range(remaining_file_number):
                    Log_content += '[!] 开始存储题目 %s 的第 %d 个附件!\n' % (problem_name,index+1)
                    print('\033[0;33m' + '[!] 开始存储题目 %s 的第 %d 个附件!' % (problem_name,index+1) + '\033[0m')
                    if (save_file(url,challenge_path + get_filename(problem['files'][index]),problem['files'][index])):
                        Log_content += '[!] 题目 %s 的第 %d 个附件存储成功!\n' % (problem_name,index+1)
                        print('\033[0;32m' + '[!] 题目 %s 的第 %d 个附件存储成功!' % (problem_name,index+1) + '\033[0m')
                        Save_fail = False
                    else:
                        shutil.rmtree(os.path.expanduser(challenge_path))
                        Log_content += '[!] 题目 %s 的第 %d 个附件存储失败!题目文件夹已被清除!!\n' % (problem_name,index+1)
                        print('\033[0;31m' + '[!] 题目 %s 的第 %d 个附件存储失败!题目文件夹已被清除!' % (problem_name,index+1) + '\033[0m')
                        Save_fail = True
                        break
                if Save_fail :
                    Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,problem_name)
                    print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,problem_name) + '\033[0m')
                    continue

        try:
            challenge_exist_file = open(os.path.expanduser(challenge_exist_file_path),'w')
            challenge_exist_file.write("此文件由自动存题脚本生成，如需更新题目描述，请删除本文件！")
            challenge_exist_file.close()
            save_success_num = save_success_num + 1
        except Exception as e:
            if DEBUG:
                print(e)
            shutil.rmtree(os.path.expanduser(challenge_path))
            Log_content += '[-] %s 方向新增题目 %s 失败!请尝试再次存储!\n' % (category,problem_name)
            print('\033[0;31m' + '[-] %s 方向新增题目 %s 失败!请尝试再次存储!' % (category,problem_name) + '\033[0m')
            continue

    #Save Log
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
    url = ''
    Cookies['session'] = ''
    # Cookies['Other'] = 'Other'
    #以上为用户预定义部分↑

    if race_name != '' and Cookies['session'] != '' and url != '':
        print('\033[0;32m' + '[+]现在开始自动化存储 ' + race_name + '的题目!' + '\033[0m')
        Save(url,race_name)
    else :
        print('\033[0;33m' + '[-]程序缺少关键参数!请检查源码中的用户预定义部分是否填写完毕!' + '\033[0m')