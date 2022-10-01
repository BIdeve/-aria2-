import os
import time
from pyaria2 import Aria2RPC


#目前适配以下网站：
#https://www.aixiaxsw.com
#



path = 'index.html'
url = input('请输入网站地址:\n')
if url.split('/')[2] == 'www.aixiaxsw.com':
    code =  'utf-8'
else:
    code = 'ansi'



#下载程序
def get_file_from_url(link, file_name):
    jsonrpc = Aria2RPC()
    set_dir = os.path.dirname(__file__)
    options = {"dir": set_dir, "out": file_name, }
    res = jsonrpc.addUri([link], options = options)

#按行读取
def readlines(path):
    f = open(path,'r',encoding= code)
    indexhtmls = f.readlines()
    f.close()
    return indexhtmls

#读取目录
def index_html_read(path):
    global url
    indexhtml = readlines(path)
    firsturl = url.split('/')[0] + '//' + url.split('/')[2]
    for i in indexhtml:
        global titlename
        if i.count('"') == 4 :
            i = i.split('"')
            if i[1] == 'og:title':
                titlename = i[3]
                print(i[3])
                break
    print(firsturl)#输出网站地址
    alldit = {}
    temp = 0
    for i in indexhtml:
        if i[-8:-1] == '正文</dt>':
            temp += 1
        if i[-6:-1] == '</dd>' and temp > 0:
            i = i.split('"')
            alldit[clane(i[-1][1:-10])] = firsturl+i[1]

    return alldit

#写入txt
def readhtml(path):
    global titlename
    TXT = ''
    while(1):
        time.sleep(0.01)
        if os.path.exists(titlename+'/'+path):
            break
    htmldata = readlines(titlename+'/'+path)
    TXT = TXT +'\n\n' + path + '\n\n'
    for j in range(len(htmldata)):
        if htmldata[j][-7:-1] == '<br />':
            line1 = htmldata[j].split('>')[1][0:-5].replace('&nbsp;&nbsp;&nbsp;&nbsp;','')
            TXT = TXT + line1 + '\n\n'
            break
    for i in htmldata:
        if i[0:5] == '&nbsp':
            TXT = TXT + i[24:-7] + '\n\n'
    return TXT

#特殊字符替换
def clane(s):
    s = s.replace('?','？')
    s = s.replace('*','﹡')
    s = s.replace('|','▕')
    s = s.replace('"','“')
    s = s.replace('<','《')
    s = s.replace('>','》')
    s = s.replace(':','：')
    return s

#txt导入
def inputtxt(url):

    get_file_from_url(url,'index.html')
    print('开始获取目录')
    while(1):
        time.sleep(0.01)
        if 0==os.path.exists(path):
            continue
        global alldit
        alldit = index_html_read(path)
        if confire(alldit):
            print('目录获取成功')
            break

    #下载小说原始资源
    print('小说数据下载开始')
    for i in alldit:
        get_file_from_url(alldit[i],titlename+'\\'+i)
    print('小说数据下载结束')

    #开始导入txt
    print('开始整合原始数据')
    f = open(titlename+'.txt','w',encoding= code)
    f.write(titlename+'\n\n\n')
    f.write('------------------------------------------------------------''\n\n\n')
    for i in alldit:
        if i == '':
            continue
        f.write(readhtml(i))
    f.close()
    print('数据整合结束')


#检查是否完整下载
def confire(alldit):
    allditlat = index_html_read(path)
    return allditlat == alldit

#清除缓存
def clean():
    chioce = input('是否清除缓存？（y/n)')
    if chioce == 'y' or chioce == '':
        del_files(titlename)
        try:
            os.rmdir(titlename)
            os.remove('index.html')
            for i in range(10):
                os.remove('index.'+str(i+1)+'.html')
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



#主体
inputtxt(url)
clean()
if confire(alldit):
    print('\n\n文件获取无误\n\n')
clean()


