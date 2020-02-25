# -*- coding: UTF-8 -*-
# @Author   : ERROR404
# @Version  : 1.0
import requests,os,ssl,html,urllib.request,time,shutil

ssl._create_default_https_context = ssl._create_unverified_context
DEBUG = False # 将此处置位将会输出部分except的异常详细信息！

Headers={
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'SIGN': '',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

Cookies={
    '__jsluid_s':'',
    'chkphone':'',
    'ci_session_race':''
}

def Check_and_make_dir(dir_path):
    if (os.path.exists(os.path.expanduser(dir_path))):
        pass
    else:
        os.makedirs(os.path.expanduser(dir_path), exist_ok=True)
        print('\033[0;33m' + '[!]创建了新目录:' + dir_path + '!' + '\033[0m')

def Save(race_name,post_data):
    Log_content  = '本程序在 %s 启动，开始自动储存题目!\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
    save_success_num = 0
    race_path = '~/Desktop/CTF_question/' + race_name + '/'

    try:
        detail_API_url = 'https://race.ichunqiu.com/api/question/detail'
        
        All_detail = requests.post(detail_API_url,headers=Headers,cookies=Cookies,data=post_data)
        detail_list = All_detail.json()['data']
    except:
        if(All_detail.json()['message'] == '暂无数据'):
            print('\033[0;31m' + '[-]已经与服务器建立连接!但是暂未放出题目，请耐心等待!' + '\033[0m')
            exit(0)
        print('\033[0;31m' + '[-]与服务器链接失败或服务器返回值异常!请检查Cookie或URL是否正确设置!' + '\033[0m')
        exit(0)

    question_list = detail_list['data']
    for question in question_list:
        question_path = race_path + question['category'] + '/' + question['title'] + '/'
        Check_and_make_dir(question_path)

        # Save Description
        description_path = question_path + '题目描述.txt'
        print('\033[0;33m' + '[!]开始写入题目 ' + question['title'] + ' 的题目描述!' + '\033[0m')
        try:
            description_file = open(os.path.expanduser(description_path),'w')
            description_file.write(html.unescape(question['content']))
            print('\033[0;32m' + '[+] ' + question['title'] + ' 的题目描述写入成功!' + '\033[0m')
        except Exception as e:
            shutil.rmtree(os.path.expanduser(question_path))
            print('\033[0;31m' + '[-] ' + question['title'] + ' 的题目描述写入失败!题目文件夹已被清除!' + '\033[0m')
            Log_content += '%s 方向新增题目 %s 失败!请尝试再次存储!\n' % (question['category'],question['title'])
            continue

        # Save Hint
        if question['tips'] != "":
            hint_path = question_path + 'Hint.txt'
            print('\033[0;33m' + '[!]开始写入题目 ' + question['title'] + ' 的Hint!' + '\033[0m')
            try:
                hint_file = open(os.path.expanduser(hint_path),'w')
                hint_file.write(html.unescape(question['tips']))
                print('\033[0;32m' + '[+] ' + question['title'] + ' 的Hint写入成功!' + '\033[0m')
            except Exception as e:
                shutil.rmtree(os.path.expanduser(question_path))
                print('\033[0;31m' + '[-] ' + question['title'] + ' 的Hint写入失败!题目文件夹已被清除!' + '\033[0m')
                Log_content += '%s 方向新增题目 %s 失败!请尝试再次存储!\n' % (question['category'],question['title'])
                continue

        save_success_num = save_success_num + 1
        Log_content += '%s 方向新增题目 %s !\n' % (question['category'],question['title'])

    #Save Log
    Log_content += '本程序在 %s 成功存储了 %d 道题目。\n\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),save_success_num)
    Log_file_path = '~/Desktop/CTF_question/' + race_name + '/Auto_Save_Result.txt'
    Log_file = open(os.path.expanduser(Log_file_path),'a')
    Log_file.write(Log_content)
    
    print('\033[0;32m' + '[+]ALL Done!i春秋竞赛系统使用了百度云 or 腾讯微云作为题目存储位置，请手动下载!' + '\033[0m')
        

if __name__ == "__main__": 
    print('\033[0;32m' + '欢迎使用由 ERROR404 开发的自动存题脚本~' + '\033[0m')
    print('\033[0;32m' + '如遇任何问题或有建议欢迎在Github提issue~' + '\033[0m')

    #以下为用户预定义部分↓
    # 你打算把本赛事的题目丢到哪个文件夹去呢~
    race_name = ''
    # 请从浏览器获取该字段然后填在这里哦~
    Headers['SIGN'] = ''
    Cookies['__jsluid_s'] = ''
    Cookies['chkphone'] = ''
    Cookies['ci_session_race'] = ''
    post_data = {
        'k': '',
        'rs': ''
    }
    #以上为用户预定义部分↑

    if race_name != '' and Headers['SIGN'] != '' and Cookies['__jsluid_s'] != '' and Cookies['chkphone'] != '' and Cookies['ci_session_race'] != '' and post_data['k'] != '' and post_data['rs'] != '' :
        print('\033[0;32m' + '[+]现在开始自动化存储 ' + race_name + '的题目!' + '\033[0m')
        Save(race_name,post_data)
    else :
        print('\033[0;33m' + '[-]程序缺少关键参数!请检查源码中的用户预定义部分是否填写完毕!' + '\033[0m')