# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from getlist import getlist
import threading

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"豆瓣红星歌曲下载程序", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.username = wx.TextCtrl(self, wx.ID_ANY, u"adol.890206@163.com", wx.DefaultPosition, wx.Size(200, 30), 0)
        bSizer2.Add(self.username, 0, wx.ALL, 5)

        self.password = wx.TextCtrl(self, wx.ID_ANY, u"2222222", wx.DefaultPosition, wx.Size(200, 30), 0)
        bSizer2.Add(self.password, 0, wx.ALL, 5)

        self.captcha = wx.TextCtrl(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(200, 30), 0)
        bSizer2.Add(self.captcha, 0, wx.ALL, 5)

        #初始化浏览器
        self.browserHander = getlist()

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(u"./v.jpg", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.Size(-1, -1), 0)
        bSizer2.Add(self.m_bitmap1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"登录豆瓣 FM", wx.DefaultPosition, wx.Size(150, 40), 0)
        bSizer2.Add(self.m_button1, 0, wx.ALL, 5)

        #动作条
        self.m_gauge2 = wx.Gauge(self,wx.ID_ANY,100,wx.DefaultPosition,(250,-1),wx.GA_HORIZONTAL)
        self.m_gauge2.SetValue(0)
        bSizer2.Add(self.m_gauge2,0,wx.ALL,5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.UserInfoLabel = wx.StaticText(self, wx.ID_ANY, u'用户信息:>>#######<<', wx.DefaultPosition, (250, 60), 0)
        self.UserInfoLabel.Wrap(-1)
        bSizer4.Add(self.UserInfoLabel, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        m_listBox1Choices = [
            u'登录之后',
            u'在下面会展示',
            u'加红星的歌曲',
            u'请登录'
        ]

        self.m_listBox1 = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, (250, 400), m_listBox1Choices,
                                     wx.LB_ALWAYS_SB, )
        bSizer4.Add(self.m_listBox1, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        #消息显示
        self.m_infoCtrl1 = wx.InfoBar(self)
        self.m_infoCtrl1.SetShowHideEffects(wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE)
        self.m_infoCtrl1.SetEffectDuration(500)
        bSizer4.Add(self.m_infoCtrl1, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.submitToDouban)
        self.m_gauge2.Bind(wx.EVT_IDLE,self.m_gauge2LDLE)
        self.m_listBox1.Bind(wx.EVT_IDLE,self.listbox1IDLE)

    def listbox1IDLE(self,event):
        if self.browserHander.musiclist != '':
            self.m_listBox1.Append(self.browserHander.musiclist)
            self.browserHander.musiclist = ''
        pass

    musicDowned = 100
    def m_gauge2LDLE(self,event):
        try:
            self.musicDowned = self.browserHander.count*100/self.browserHander.userinfo['liked']
            self.m_gauge2.SetValue(self.musicDowned)
        except:
            pass


    # Virtual event handlers, overide them in your derived class
    def submitToDouban(self, event):
        Tlogin = threading.Thread(target=self.login,args=())
        Tlogin.start()

    def login(self):
        self.m_listBox1.SetItems([u'加载中……'])
        username = self.username.GetValue()
        password = self.password.GetValue()
        captcha = self.captcha.GetValue()
        formatJSON = self.browserHander.login(username, password, captcha)
        self.musicTotle = int(self.browserHander.userinfo['liked'])
        self.UserInfoLabel.SetLabel(
            u'你好，%s\n累计收听歌曲：%s 首\n总共加★歌曲：%s 首\n不再收听：%s首' % (
                self.browserHander.userinfo['name'],
                self.browserHander.userinfo['played'],
                self.browserHander.userinfo['liked'],
                self.browserHander.userinfo['banned']))
        self.m_listBox1.Append(u'加载完成，写入文件……')
        songlist = [
            u'歌曲名,歌手名,专辑名,下载地址',
        ]

        listFile = open('./list.csv', 'w')
        for eachsong in formatJSON['songs']:
            songlist = u'%s,%s,%s,%s\n' % (
                eachsong['title'],
                eachsong['artist'],
                eachsong['subject_title'],
                eachsong['url'],
                #eachsong['path'],
            )
            print eachsong
            #self.m_listBox1.Append(songlist)
            #准备列表文件
            #listFile.write(u'\n'.join(songlist).encode('utf8'))
            listFile.write(songlist.encode('utf8'))
            print '完成'
        listFile.close()
        #self.m_listBox1.SetItems(songlist)

    def __del__(self):
        self.browserHander = None
        #杀掉线程
        pass