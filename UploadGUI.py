#!/usr/bin/python
# -*- coding: utf-8 -*-

# UploadGUI.py

import wx
import time
from threading import *
import mapbox
import datetime
import os


EVT_RESULT_ID = wx.NewId()
def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

open('log.txt','w')

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('{%Y-%m-%d %H:%M:%S}  ')


class ResultEvent(wx.PyEvent):

    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data



# Thread class that executes processing
class WorkerThread(Thread):

    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.access_token='sk.eyJ1IjoiYmFzaG8xMzM3IiwiYSI6ImNqOWpzdWx5aDE4bXkycXMyY3hwdjJ4dXYifQ.lreabRuF1Az8TBsT34N8KQ'
        self.pfad = pfad
        self.dronename = dronename
        self.datatype = datatype
        self.starttileset = starttileset
        self.ts = time.time()
        self.st = datetime.datetime.fromtimestamp(self.ts).strftime('{%Y-%m-%d %H:%M:%S}  ')
        self.log = open('log.txt', 'a')

        self.start()

    def run(self):
        wx.PostEvent(self._notify_window, ResultEvent('---STARTED---\n'))
        self.log.write(self.st + '---STARTED---\n')
        wx.PostEvent(self._notify_window, ResultEvent('Path:  '+ self.pfad +'\n'))
        self.log.write(self.st + 'Path:  '+ self.pfad +'\n')
        wx.PostEvent(self._notify_window, ResultEvent('Dronename:  '+ self.dronename+'\n'))
        self.log.write(self.st + 'Dronename:  '+ self.dronename+'\n')
        wx.PostEvent(self._notify_window, ResultEvent('Datatype:  '+ self.datatype+'\n'))
        self.log.write(self.st + 'Datatype:  '+ self.datatype+'\n')
        wx.PostEvent(self._notify_window, ResultEvent('Starting Tileset:  '+ str(self.starttileset)+'\n' ))
        self.log.write(self.st + 'Starting Tileset:  '+ str(self.starttileset)+'\n')
        #j = 1

        while True:
            if os.path.isfile(self.pfad  + '/' + self.dronename + str(self.starttileset) + self.datatype) == True:
                wx.PostEvent(self._notify_window, ResultEvent('Data '+ self.dronename +str(self.starttileset)+ ' found! Preparing to upload:\n'))
                self.log.write(self.st + 'Data '+ self.dronename +str(self.starttileset)+ ' found! Preparing to upload:\n')

                res = mapbox.Uploader(access_token=self.access_token)._get_credentials()
                with open(self.pfad  + '/' + self.dronename + str(self.starttileset) + self.datatype, 'rb') as src:
                    stage_url = mapbox.Uploader(access_token=self.access_token).stage(src)

                wx.PostEvent(self._notify_window, ResultEvent('Data '+ self.dronename +str(self.starttileset)+ ' successfully staged. Start upload:\n'))
                self.log.write(self.st + 'Data '+ self.dronename +str(self.starttileset)+ ' successfully staged. Start upload:\n')

                def print_cb(num_bytes):
                    wx.PostEvent(self._notify_window, ResultEvent('{0} bytes uploaded\n'.format(num_bytes)))
                    self.log.write(self.st + '{0} bytes uploaded\n'.format(num_bytes))

                with open(self.pfad  + '/' + self.dronename + str(self.starttileset) + self.datatype, 'rb') as src:
                    res = mapbox.Uploader(access_token=self.access_token).upload(src, self.dronename + str(self.starttileset), callback=print_cb)
                    wx.PostEvent(self._notify_window, ResultEvent('Data '+ self.dronename +str(self.starttileset)+ ' successfully uploaded. Search for next:\n'))
                    self.log.write(self.st + 'Data '+ self.dronename +str(self.starttileset)+ ' successfully uploaded. Search for next:\n')
                    self.starttileset += 1
                    time.sleep(3)

            else:
                wx.PostEvent(self._notify_window, ResultEvent('Data '+ self.dronename +str(self.starttileset)+ ' not found. Sleep 3 seconds:\n'))
                self.log.write(self.st + 'Data '+ self.dronename +str(self.starttileset)+ ' not found. Sleep 3 seconds:\n')
                time.sleep(3)
            if self._want_abort:
                wx.PostEvent(self._notify_window, ResultEvent('---STOPPED---\n'))
                self.log.write(self.st + '---STOPPED---\n')
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return

    def abort(self):

        self._want_abort = 1

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
            size=(750, 520))
        favicon = wx.Icon(os.path.dirname(__file__)+'/images/UAV_Icon.svg.png',wx.BITMAP_TYPE_PNG, 128,128)
        self.SetIcon(favicon)

        EVT_RESULT(self,self.OnResult)
        self.worker = None

        self.InitUI()
        self.Centre()
        self.Show()


    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        hitem = helpMenu.Append(wx.ID_ANY, 'About', 'About this program')
        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.Bind(wx.EVT_MENU, self.OnAbout, hitem)

        self.SetTitle('Upload GUI')
        self.Centre()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Choose Data Directory:')
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1,0))
        self.tc = wx.TextCtrl(panel, style= wx.TE_READONLY)
        hbox1.Add(self.tc, flag=wx.ALIGN_RIGHT, border=8, proportion=1)
        cbtn = wx.Button(panel, label='Browse Directory' )

        cbtn.Bind(wx.EVT_BUTTON, self.OnBrowse)

        hbox1.Add(cbtn, flag=wx.RIGHT)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))
        ddlabel = wx.StaticText(panel, label='Choose UAV:    ')
        hboxdd = wx.BoxSizer(wx.HORIZONTAL)

        Drones = ['Test', 'Testdrohne', 'Testgebiet', 'Live', 'Name', 'rot_', 'Datensatz_', 'Elbe_']  #Dropdown für Drohnenname
        self.dd = wx.ComboBox(panel, choices=Drones, style=wx.TE_READONLY)
        hboxdd.Add(ddlabel)
        hboxdd.Add(self.dd, flag=wx.ALIGN_RIGHT, border=8 , proportion=1)
        vbox.Add(hboxdd, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1,10))

        sblabel = wx.StaticText(panel, label='Starting Tileset:   ')
        hboxsb = wx.BoxSizer(wx.HORIZONTAL)
        self.spinbox= wx.SpinCtrl(panel, value='1')
        self.spinbox.SetRange(1,1000)
        hboxsb.Add(sblabel)
        hboxsb.Add(self.spinbox, flag=wx.RIGHT, border=8, proportion=1)
        vbox.Add(hboxsb, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1,10))


        ddlabel2 = wx.StaticText(panel, label='Data Format:       ')
        hboxdd2 = wx.BoxSizer(wx.HORIZONTAL)

        Formats = ['.mbtiles', '.tif']  #Dropdown für Dateiformat
        self.dd2 = wx.ComboBox(panel, choices=Formats, style=wx.TE_READONLY)
        hboxdd2.Add(ddlabel2)
        hboxdd2.Add(self.dd2, flag=wx.ALIGN_RIGHT, border=8 , proportion=1)
        vbox.Add(hboxdd2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1,10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Log:')
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hbox3.Add(self.tc2, proportion=1, flag=wx.EXPAND)

        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        vbox.Add((-1, 25))


        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.Button(panel, label='Run')
        cb1.Bind(wx.EVT_BUTTON, self.OnRun)
        hbox4.Add(cb1)
        cb2 = wx.Button(panel, label='Stop')
        cb2.Bind(wx.EVT_BUTTON, self.OnStop)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        btn2.Bind(wx.EVT_BUTTON, self.OnQuit)
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        self.dd.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.dd2.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
    def OnAbout(self, e):

        wx.MessageBox('Mapbox Upload GUI - Technical University of Braunschweig, IFF - Copyright by M. Steinborn', 'About',wx.OK)
        favicon = wx.Icon(os.path.dirname(__file__)+'/images/UAV_Icon.svg.png',wx.BITMAP_TYPE_PNG, 128,128)
        self.SetIcon(favicon)

    def OnQuit(self, e):
        self.Close()

    def OnBrowse(self,e):

        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.tc.SetValue(dialog.GetPath())
            global pfad
            pfad = dialog.GetPath().replace('\\','/')
            dialog.Destroy()

    def OnRun(self,e):
        global starttileset
        starttileset = self.spinbox.GetValue()

        if not self.worker:
            self.worker = WorkerThread(self)



    def OnSelect(self,e):
        self.select = e.GetString()
        global dronename
        dronename = e.GetString()


    def OnSelect2(self,e):
        self.select2 =e.GetString()
        global datatype
        datatype = e.GetString()

    def OnStop(self,e):
        if self.worker:
            self.worker.abort()
            self.worker = None

    def OnResult(self, event):
        if event.data is None:
            print('none')
        else:
            self.tc2.AppendText(str(event.data))

    def OnChange(self, e):
        global starttileset
        self.starttileset = e.GetValue()
        print self.starttileset

if __name__ == '__main__':

    app = wx.App()
    Example(None, title='Upload GUI')
    app.MainLoop()
