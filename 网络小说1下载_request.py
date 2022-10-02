import os
import time
from pyaria2 import Aria2RPC
import requests


url = input('请输入小说地址：\n')

#下载
def get_file_from_url(link, file_name):
    if os.path.exists(file_name) == 0 :
        jsonrpc = Aria2RPC()
        set_dir = os.path.dirname(__file__)
        options = {"dir": set_dir, "out": file_name, }
        res = jsonrpc.addUri([link], options = options)

#获取html
def get_html(part_url):
    global code
    if part_url.split('/')[2] == 'www.aixiaxsw.com':
        code =  'utf-8'
    else:
        code = 'gbk'
    res = requests.get(part_url)
    res.encoding = code
    print(res.text)
    if len(res.text.split('\n')) < 20:
        get_file_from_url(part_url,'index')
        while(1):
            time.sleep(0.01)
            if os.path.exists('index'):
                time.sleep(0.1)
                fo = open('index','r',encoding = code)
                break
        html = fo.readlines()
        fo.close()
        os.remove('index')
        for i in range(len(html)):
            html[i] = html[i][:-1]
        return html
    else:
        return res.text.split('\n')

#读取html
def readlines(path):
    f = open(path,'r',encoding= code)
    indexhtmls = f.readlines()
    f.close()
    return indexhtmls

#读取目录
def index_html_read(url):
    indexhtml = get_html(url)
    firsturl = url.split('/')[0] + '//' + url.split('/')[2]
    for i in indexhtml:
        if i.count('"') == 4 :
            i = i.split('"')
            if i[1] == 'og:title':
                global titlename
                titlename = i[3]
                print(i[3])
                break
    print(firsturl)
    alldit = {}
    temp = 0
    count = 0
    for i in indexhtml:
        if i[-7:-5] == '正文':
            temp += 1
        if i[-5:] == '</dd>' and temp > 0:
            count += 1
            i = i.split('"')
            if i[1][:len(firsturl)] == firsturl:
                alldit[str(count)] = i[1]
            else:
                alldit[str(count)] = firsturl+i[1]
    return alldit

#获取正文
def readhtml(path):
    global titlename
    TXT = ''
    while(1):
        time.sleep(0.01)
        if os.path.exists(titlename+'/'+path):
            break
    htmldata = readlines(titlename+'/'+path)
    for i in htmldata:
        if i[-6:-1] == '</h1>':
            TXT = TXT +'\n\n' + i.split('<h1>')[1][:-6] + '\n\n'
            break
    for j in range(len(htmldata)):
        if htmldata[j][-7:-1] == '<br />':
            line1 = htmldata[j].split('>')[1][0:-5].replace('&nbsp;&nbsp;&nbsp;&nbsp;','')
            TXT = TXT + line1 + '\n\n'
            break
    for i in htmldata:
        if i[0:5] == '&nbsp':
            TXT = TXT + i[24:-7] + '\n\n'
    return TXT

def inputtxt(alldit):
    #下载小说原始资源
    print('小说数据下载开始')
    for i in alldit:
        get_file_from_url(alldit[i],titlename+'\\'+i)
    print('小说数据下载结束')

    #开始导入txt
    print('开始整合原始数据')
    f = open(titlename+'.txt','w',encoding= 'utf-8')
    f.write(titlename+'\n\n\n')
    f.write('------------------------------------------------------------''\n\n\n')
    for i in alldit:
        f.write(readhtml(i))
    f.close()
    print('数据整合结束')

#清除缓存
def clean():
    chioce = input('是否清除缓存？（y/n)')
    if chioce == 'y' or chioce == '':
        del_files(titlename)
        try:
            os.rmdir(titlename)
        except:
            print('发生错误，请手动删除缓存')
        print('缓存删除结束')

# 删除(支持文件，文件夹不存在不报错)
def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            # if file_name != 'wibot.log':
            tf = os.path.join(dir_path, file_name)
            del_files(tf)

#小说下载流程
def novel_download(url):
    alldit = index_html_read(url)
    inputtxt(alldit)
    clean()

#novel_download(url)

get_html('https://www.um16.cn/info/7853/6080841.html')