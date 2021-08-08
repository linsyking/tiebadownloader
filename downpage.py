#!/usr/bin/env python
# coding=utf-8
import requests
from progress.bar import Bar
import os
import re

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

cookies = {
    'PSTM': '1628174644',
    'BAIDUID': '461218646534E0FDC31D373550706CF4:FG=1',
    'BIDUPSID': '8014F6D7BFA37DC87A5BF49985C84287',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    '__yjs_duid': '1_be83af0d77043f30fc776d9513ecdeec1628174652362',
    'BDUSS': 'lEtYnRlVDhoMi02WHplandEbUN-dWFieVdUUXNtam9SbXhFVllBU3Z2MGNoek5oRVFBQUFBJCQAAAAAAAAAAAEAAADRKZukMTMzX0JBXzk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz6C2Ec-gthZ',
    'BDUSS_BFESS': 'lEtYnRlVDhoMi02WHplandEbUN-dWFieVdUUXNtam9SbXhFVllBU3Z2MGNoek5oRVFBQUFBJCQAAAAAAAAAAAEAAADRKZukMTMzX0JBXzk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz6C2Ec-gthZ',
    'STOKEN': 'a40d55ef379d56900e4d7c417479b9b2bf9d09227ef2f85dbe49e1ebb9482609',
    'bdshare_firstime': '1628227231590',
    'BAIDUID_BFESS': '461218646534E0FDC31D373550706CF4:FG=1',
    'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628232398,1628232992,1628233921,1628340185',
    'st_key_id': '17',
    'wise_device': '0',
    'st_data': 'a9712517b40ee61c2708af9db58f92239b830ae9420f01dfabe564675b8a1aceafd42accebcbead9f2a3be3e4fcf316910feddf116b73dc904f35b1d6024fd8c692a1c9c5a604c988dc1d9e44dafefbc3f2b1b7debdb4dadfe777a417b47fb8371653d3f04e05f201c523f4bd1badedd67561814ca92a7bd0ce9d1cfac82dd9d',
    'st_sign': '16214376',
    'ab_sr': '1.0.1_NWE1MzAxMzRkMWEyNmM3ZDQ0ODRlNjcyZTA4MGNkZDFmZTE1OGM0NzVkZTJhYTIwY2JhMDQ4ZGEzOWRhNGFhN2Y5MmJiOGEwNGRmN2Y4MzYwZGI3NTY1YzdkMWMwNDdkMGQ5MGVlNWQ1ZGNkMWE3OWI3NjExYThmNTcwZWUzNjBkMWM4ZWNhMmMxNmVkOTg5NzdkMDExZWRhMTU2ZDg0NA==',
    'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628340212',
}


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
			file=requests.get("http://tieba.baidu.com/p/"+str(x),headers=headers,cookies=cookies)
			data=file.content
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
