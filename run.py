#coding=utf-8
import urllib.request
import re
import os
import socket
import shutil
from urllib.request import urlretrieve
from progress.bar import Bar
socket.setdefaulttimeout(2)

warning='''
您好，欢迎使用贴吧下载器1.0版，以下为使用说明：
1.请保证css目录与运行目录相同
2.只能下载主题贴的第一页，且无楼中楼
3.只能查看图片
4.下载中若出现错误(自动退出)，请检查网络并重启
2020.2.9
'''



swr='''
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>Index</title>
<link rel="icon" href="favicon.ico" type="image/ico">
<link href="css/bootstrap.min.css" rel="stylesheet">
<link href="css/materialdesignicons.min.css" rel="stylesheet">
<link href="css/style.min.css" rel="stylesheet">
'''

fi='''
<table class="table table-striped">
<tr>
<th>名称</th>
<th>作者</th>
<th>时间</th>
<th>链接</th>
</tr>
'''
def save_img(img_url,file_name,file_path):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
	dj=0
	while(dj<=5):
		dj=dj+1
		if(dj==5):
			exit()
		try:
			if (not os.path.exists(file_path)):
				print ('文件夹',file_path,'不存在，重新建立')
				#os.mkdir(file_path)
				os.makedirs(file_path)
			filename = '{}{}{}'.format(file_path,os.sep,file_name)
		       #下载图片，并保存到文件夹中
			urlretrieve(img_url,filename=filename)
			dj=100
		except socket.timeout:
			dj=dj
		except IOError as e:
			dj=dj
		except Exception as e:
			dj=dj
snd=b'''
<link rel="stylesheet" href="../../css/a_007.css">
<link rel="stylesheet" href="../../css/a_004.css">
<link rel="stylesheet" href="../../css/a_006.css">
<link rel="stylesheet" href="../../css/a_008.css">
<link rel="stylesheet" href="../../css/a_005.css">
<link rel="stylesheet" href="../../css/a_003.css">
<link rel="stylesheet" href="../../css/a.css">
<link rel="stylesheet" href="../../css/a_002.css">
'''

#获取所有帖子的id
print(warning)
sasaas=input('输入您要下载的贴吧名(不要“吧”字，如：逗比)')
tiebaname=str(sasaas.encode(encoding='utf-8',errors='ignore'))
tiebaname=tiebaname.replace("b'",'')
tiebaname=tiebaname.replace("'",'')
tiebaname=tiebaname.replace("\\x",'%')
#1.先获取总页数
ktmp=1
while (ktmp==1):
	try:
		file=urllib.request.urlopen("http://tieba.baidu.com/f?kw="+tiebaname+"&pn=0")
		data=file.read()
		ktmp=0
	except Exception as e:
		ktmp=1
reg=r'pn=(.*?)" class="last pagination-item " >尾页'
ia=re.compile(reg)
sa=re.findall(ia,data.decode('utf-8',errors='ignore'))
maxpage=0
for x in sa:
	maxpage=int(x)
print('总页数为：'+str(maxpage))
k=0
list=[]

bar=Bar('Processing',max=maxpage/50+1,suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
while k<=maxpage:
	ktmp=1
	while (ktmp==1):
		try:
			file=urllib.request.urlopen("http://tieba.baidu.com/f?kw="+tiebaname+"&ie=utf-8&pn="+str(k))
			data=file.read()
			ktmp=0
		except Exception as e:
			ktmp=1
	reg=r'href="/p/(.+?)" title="(.+?)".*?j_th_tit[\s\S]*?主题作者: (.+?)"[\s\S]*?创建时间">(.+?)<'
	ia=re.compile(reg)
	sa=re.findall(ia,data.decode('utf-8',errors='ignore'))
	list=list + sa
	bar.next()
	k=k+50
list=sorted(list, key=lambda i:int(i[0]))
fhandle=open('./pb.html','w',encoding='utf-8',errors='ignore')
fhandle.write(swr+'\n<h3>'+sasaas+'</h3>\n'+fi)
for x in list:
	fhandle.write('<tr>\n<td>'+str(x[1])+'</td>\n<td>'+str(x[2])+'</td>\n<td>'+str(x[3])+'</td>\n<td><a href="http://tieba.baidu.com/p/'+str(x[0])+'">Link</a></td>\n</tr>\n')
fhandle.write('</table>')
fhandle.close()
bar.finish
print('\n开始下载帖子')
#以下过程为下载所有帖子
k=1
file=open('pb.html','rb')
data=file.read()
reg=r'/p/(.*?)"'
ia=re.compile(reg)
sat=re.findall(ia,data.decode('utf-8',errors='ignore'))
lts=len(sat)
if (not os.path.exists('downloadserver')):
	os.mkdir('downloadserver')
bar=Bar('Processing',max=lts,suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')

for x in sat:
	if(os.path.exists('downloadserver/'+str(x)+'/'+str(x)+'.html')):
		bar.next()
		k=k+1
		continue
	ktmp=1
	while (ktmp==1):
		try:
			file=urllib.request.urlopen("http://tieba.baidu.com/p/"+str(x),timeout=2)
			data=file.read()
			ktmp=0
		except Exception as e:
			ktmp=1
	if(not os.path.exists('downloadserver/'+str(x))):
		os.mkdir('downloadserver/'+str(x))
	fhandle=open('downloadserver/'+str(x)+'/'+str(x)+'.html','wb')
	fhandle.write(data)
	fhandle.close()
	bar.next()
	k=k+1
k=1
bar.finish
print('\n网页文档下载完毕，开始下载图片')
#下载图片
bar=Bar('Processing',max=lts,suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
for x in sat:
	file=open('downloadserver/'+str(x)+'/'+str(x)+'.html','rb')
	data=file.read()
	reg=r'src="(http://imgsrc\.baidu\.com/forum/w%3D580/sign=.*?jpg)"'
	ia=re.compile(reg)
	sa=re.findall(ia,data.decode('utf-8',errors='ignore'))

	reg=r'src="(http://tiebapic.*?jpg)"'
	ia=re.compile(reg)
	sb=re.findall(ia,data.decode('utf-8',errors='ignore'))

	reg=r'src="(http://imgsrc\.baidu\.com/forum/w%3D580%.*?jpg)"'
	ia=re.compile(reg)
	sc=re.findall(ia,data.decode('utf-8',errors='ignore'))
	

	reg=r'src="(https://imgsa\.baidu\.com/forum/w%3D580/sign=.*?jpg)"'
	ia=re.compile(reg)
	sd=re.findall(ia,data.decode('utf-8',errors='ignore'))

	ndata=data
	nsla=bytes('', encoding = "utf8")
	ndata=ndata.replace(snd,nsla)
	for y in sa:
		p=y.replace("http://imgsrc.baidu.com/forum/w%3D580/sign=","")	
		p=p.replace("/","")
		if(os.path.exists('downloadserver/'+str(x)+'/'+str(p))):
			continue	
		sh=bytes('./'+p, encoding = "utf8")
		sx=bytes(y, encoding = "utf8")
		ndata=ndata.replace(sx,sh)
		save_img(y,p,'downloadserver/'+str(x)+'/')
	for y in sb:
		p=y.replace("http://tiebapic.baidu.com/forum/w%3D580/sign=","")
		p=p.replace("/","")
		if(os.path.exists('downloadserver/'+str(x)+'/'+str(p))):
			continue
		sh=bytes('./'+p, encoding = "utf8")
		sx=bytes(y, encoding = "utf8")
		ndata=ndata.replace(sx,sh)
		save_img(y,p,'downloadserver/'+str(x)+'/')
	for y in sc:
		p=y.replace("http://imgsrc.baidu.com/forum/w%3D580%","")
		p=p.replace("/","")
		p=p.replace("%","")
		if(os.path.exists('downloadserver/'+str(x)+'/'+str(p))):
			continue
		sh=bytes('./'+p, encoding = "utf8")
		sx=bytes(y, encoding = "utf8")
		ndata=ndata.replace(sx,sh)
		save_img(y,p,'downloadserver/'+str(x)+'/')
	for y in sd:
		p=y.replace("https://imgsa.baidu.com/forum/w%3D580/sign=","")
		p=p.replace("/","")
		if(os.path.exists('downloadserver/'+str(x)+'/'+str(p))):
			continue
		sh=bytes('./'+p, encoding = "utf8")
		sx=bytes(y, encoding = "utf8")
		ndata=ndata.replace(sx,sh)
		save_img(y,p,'downloadserver/'+str(x)+'/')
	fhandle=open('downloadserver/'+str(x)+'/'+str(x)+'.html','wb')
	fhandle.write(snd+ndata)
	fhandle.close()
	bar.next()
	k=k+1
bar.finish
print('\n更新完成!')
#重新排版

file=open('pb.html','rb')
data=file.read()

reg=r'/p/(.*?)">Link'
ia=re.compile(reg)
sa=re.findall(ia,data.decode('utf-8',errors='ignore'))
for x in sa:
	sx=bytes('http://tieba.baidu.com/p/'+str(x), encoding = "utf8")
	sy=bytes('downloadserver/'+str(x)+'/'+str(x)+'.html', encoding = "utf8")
	data=data.replace(sx,sy)
fhandle=open('pb.html','wb')
fhandle.write(data)
fhandle.close()


print('\n排版完成!您可以打开pb.html访问离线页面.')
stras="pause"
os.system(stras)




