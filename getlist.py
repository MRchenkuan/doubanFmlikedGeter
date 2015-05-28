# -*- coding=utf-8 -*-
import urllib, json, re, GlobalVar
import cookielib, gzip
import urllib2
import StringIO, MyFrame1


class getlist:
    count = 0
    musiclist = ''

    def __init__(self):
        #固定的几个参数
        self.params = {"source": "radio", }
        #准备列表文件
        #self.listFile = open('list.txt', 'w')

        #设置网页Cookie，得到唯一的操作句柄
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

        #打开登录页
        suburl = 'http://douban.fm/common_login?redir=/mine'
        html = self.opener.open(urllib2.Request(suburl))

        #刷新取验证码ID
        captchaurl = 'http://douban.fm/j/new_captcha'
        data = urllib.urlencode({'ck': 'null'}).encode('unicode_escape')
        response = self.opener.open(captchaurl, data)
        self.params['captcha_id'] = response.read().decode('utf8').split('\"')[1]

        #通过验证码ID取验证码图片
        requrl = 'http://www.douban.com/misc/captcha?size=m&id=%s' % self.params['captcha_id']
        urllib.urlretrieve(requrl, 'v.jpg')
        print '获取验证码成功'

    def login(self, username, password, captcha):
        #提示用户输入图片中验证码
        self.params['alias'] = username
        self.params['form_password'] = password
        self.params['captcha_solution'] = captcha

        #初始化参数
        data = urllib.urlencode(self.params).encode('unicode_escape')

        #先获取dbcl2的cookie
        response = self.opener.open(urllib2.Request('http://douban.fm/j/login', data))
        #登录时的返回的
        ans = json.loads(response.read().decode('utf8'))
        if 'err_no' in ans:
            print(u'登录错误：%s' % ans['err_msg'])
            exit(0)
        else:
            print (u'登陆成功')
            print(u'累计收听：%s 首' % ans['user_info']['play_record']['played'])
            print(u'加红心：%s 首' % ans['user_info']['play_record']['liked'])
            print(u'不再收听：%s 首' % ans['user_info']['play_record']['banned'])
        self.userinfo = ans['user_info']['play_record']
        self.userinfo['name'] = ans['user_info']['name']
        print ans['user_info']
        #抓取红心歌曲表单
        #第一页歌曲列表url同时获得ck
        response = self.opener.open(urllib2.Request('http://douban.fm/mine'))



        #开始通过cookie初始化参数
        for eachcook in self.cookie:
            print eachcook.name, eachcook.value
            if eachcook.name == 'bid':
                bid = eachcook.value.split('\"')[1]
            if eachcook.name == 'ck':
                ck = eachcook.value.split('\"')[1]
            if eachcook.name == 'ac':
                ac = eachcook.value.split('\"')[1]

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'douban.fm',
            'Referer': 'http://douban.fm/mine',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        i = 0  #局部变量
        formatJSON = {u'songs': []}
        while True:
            coreUrl = 'http://douban.fm/j/play_record?ck=%s&spbid=::%s&type=liked&start=%s' % (ck, bid, i)
            #print coreUrl
            req = urllib2.Request(url=coreUrl, headers=headers)
            response = self.opener.open(req).read()
            #gzip数据的解压过程
            gzipString = StringIO.StringIO(response)
            compressedString = gzip.GzipFile(fileobj=gzipString)
            compressedJSON = compressedString.read()
            i = i + 15
            if i > 60: #默认4页
                break
            aPageOfFormatJSON = json.loads(compressedJSON)
            formatJSON['songs'].extend(aPageOfFormatJSON.get('songs'))
            if len(formatJSON['songs']) == 0:
                return ['', '', u'没有找到歌曲，请重试!']
            if len(aPageOfFormatJSON['songs']) <= 0:
                break

            #开始找歌的连接
            p = re.compile(r'[\d]+')
            STDSONGS = []
            for eachsong in formatJSON['songs']:
                #找专辑id和歌曲id
                songsAlbumID = p.findall(eachsong['path'])[0]
                #('http://music.douban.com/subject/3066936/','[\d]+')
                songsid = eachsong['id']
                #找专辑数据
                req = urllib2.Request(
                    'http://douban.fm/j/mine/playlist?type=n&sid=&pt=0.0&channel=0&context=channel:0|subject_id:%s&from=mainsite' % songsAlbumID)
                response = json.loads(self.opener.open(req).read())

                #开始筛选出response中的MP3
                for eachsongdetail in response["song"]:
                    if eachsongdetail['sid'] == songsid:
                        eachsong['url'] = eachsongdetail['url']
                        STDSONGS.append(eachsong)
                        print eachsongdetail
                        break
                self.count = self.count + 1
                self.musiclist = u'%s--%s' % (eachsong['title'], eachsong['artist'])
        return formatJSON