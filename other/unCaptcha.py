# -*- coding: utf-8 -*-

import random
import re
import time
import urlparse, urllib,urllib2,cookielib

from base64 import b64encode
import base64
import xbmc
import xbmcgui,xbmcaddon,os
__scriptID__ = 'plugin.video.live.streamspro'
__addon__ = xbmcaddon.Addon(__scriptID__)

class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        
        bg_image =  os.path.join( __addon__.getAddonInfo('path'), 'Images/' ) + "background.png"
        check_image =  os.path.join( __addon__.getAddonInfo('path'), 'Images/' ) + "trans_checked.png"
        uncheck_image =  os.path.join( __addon__.getAddonInfo('path'), 'Images/' ) + "trans_unchecked1.png"
        self.ctrlBackgound = xbmcgui.ControlImage(
            0,0, 
            1280, 720, 
            bg_image
        )
        self.cancelled=False
        self.addControl (self.ctrlBackgound)
        self.msg = kwargs.get('msg')+'\nNormally there are 3-4 selections and 2 rounds of pictures'
        self.roundnum=kwargs.get('roundnum')
        self.strActionInfo = xbmcgui.ControlLabel(335, 120, 700, 300, self.msg, 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)
        
        self.strActionInfo = xbmcgui.ControlLabel(335, 20, 724, 400, 'Captcha round %s'%(str(self.roundnum)), 'font40', '0xFFFF00FF')
        self.addControl(self.strActionInfo)
        
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,200,624,400,self.cptloc)
        self.addControl(self.img)
        
        self.chk=[0]*9
        self.chkbutton=[0]*9
        self.chkstate=[False]*9
        
        #self.chk[0] = xbmcgui.ControlCheckMark(335,200,200,200,'select',checkWidth=30, checkHeight=30)
        if 1==2:
            self.chk[0]= xbmcgui.ControlCheckMark(335, 190, 220, 150, '1', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[1]= xbmcgui.ControlCheckMark(335+200, 190, 220, 150, '2', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[2]= xbmcgui.ControlCheckMark(335+400, 190, 220, 150, '3', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            
            self.chk[3]= xbmcgui.ControlCheckMark(335, 190+130, 220, 150, '4', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[4]= xbmcgui.ControlCheckMark(335+200, 190+130, 220, 150, '5', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[5]= xbmcgui.ControlCheckMark(335+400, 190+130, 220, 150, '6', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
          
            
            self.chk[6]= xbmcgui.ControlCheckMark(335, 190+260, 220, 150, '7', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[7]= xbmcgui.ControlCheckMark(335+200, 190+260, 220, 150, '8', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[8]= xbmcgui.ControlCheckMark(335+400, 190+260, 220, 150, '9', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
        else:
        
            self.chk[0]= xbmcgui.ControlImage(335, 190, 220, 150,check_image)# '', font='font1',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[1]= xbmcgui.ControlImage(335+200, 190, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[2]= xbmcgui.ControlImage(335+400, 190, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            
            self.chk[3]= xbmcgui.ControlImage(335, 190+130, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[4]= xbmcgui.ControlImage(335+200, 190+130, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[5]= xbmcgui.ControlImage(335+400, 190+130, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
          
            
            self.chk[6]= xbmcgui.ControlImage(335, 190+260, 220, 150,check_image)#, '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[7]= xbmcgui.ControlImage(335+200, 190+260, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[8]= xbmcgui.ControlImage(335+400, 190+260, 220, 150,check_image)# '', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
        
        
            self.chkbutton[0]= xbmcgui.ControlButton(335, 190, 210, 150, '1', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[1]= xbmcgui.ControlButton(335+200, 190, 220, 150, '2', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[2]= xbmcgui.ControlButton(335+400, 190, 220, 150, '3', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            
            self.chkbutton[3]= xbmcgui.ControlButton(335, 190+130, 210, 150, '4', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[4]= xbmcgui.ControlButton(335+200, 190+130, 220, 150, '5', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[5]= xbmcgui.ControlButton(335+400, 190+130, 220, 150, '6', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
          
            
            self.chkbutton[6]= xbmcgui.ControlButton(335, 190+260, 210, 150, '7', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[7]= xbmcgui.ControlButton(335+200, 190+260, 220, 150, '8', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            self.chkbutton[8]= xbmcgui.ControlButton(335+400, 190+260, 220, 150, '9', font='font1');#,focusTexture=check_image ,noFocusTexture=uncheck_image);#,checkWidth=220,checkHeight=150)
            
        

        
        for obj in self.chk:
            self.addControl(obj )
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj )
        
        
        
        #self.chk[0].setSelected(False)
        
        self.cancelbutton = xbmcgui.ControlButton(335+312-100,610,100,40,'Cancel',alignment=2)
        self.okbutton = xbmcgui.ControlButton(335+312+50,610,100,40,'OK',alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[6].controlDown(self.cancelbutton);  self.chkbutton[6].controlUp(self.chkbutton[3])
        self.chkbutton[7].controlDown(self.cancelbutton);  self.chkbutton[7].controlUp(self.chkbutton[4])
        self.chkbutton[8].controlDown(self.okbutton);      self.chkbutton[8].controlUp(self.chkbutton[5])
        
        
        self.chkbutton[6].controlLeft(self.chkbutton[8]);self.chkbutton[6].controlRight(self.chkbutton[7]);
        self.chkbutton[7].controlLeft(self.chkbutton[6]);self.chkbutton[7].controlRight(self.chkbutton[8]);
        self.chkbutton[8].controlLeft(self.chkbutton[7]);self.chkbutton[8].controlRight(self.chkbutton[6]);
        
        self.chkbutton[3].controlDown(self.chkbutton[6]);  self.chkbutton[3].controlUp(self.chkbutton[0])
        self.chkbutton[4].controlDown(self.chkbutton[7]);  self.chkbutton[4].controlUp(self.chkbutton[1])
        self.chkbutton[5].controlDown(self.chkbutton[8]);  self.chkbutton[5].controlUp(self.chkbutton[2])
        
        self.chkbutton[3].controlLeft(self.chkbutton[5]);self.chkbutton[3].controlRight(self.chkbutton[4]);
        self.chkbutton[4].controlLeft(self.chkbutton[3]);self.chkbutton[4].controlRight(self.chkbutton[5]);
        self.chkbutton[5].controlLeft(self.chkbutton[4]);self.chkbutton[5].controlRight(self.chkbutton[3]);

        self.chkbutton[0].controlDown(self.chkbutton[3]);  self.chkbutton[0].controlUp(self.cancelbutton)
        self.chkbutton[1].controlDown(self.chkbutton[4]);  self.chkbutton[1].controlUp(self.cancelbutton)
        self.chkbutton[2].controlDown(self.chkbutton[5]);  self.chkbutton[2].controlUp(self.okbutton)
        
        self.chkbutton[0].controlLeft(self.chkbutton[2]);self.chkbutton[0].controlRight(self.chkbutton[1]);
        self.chkbutton[1].controlLeft(self.chkbutton[0]);self.chkbutton[1].controlRight(self.chkbutton[2]);
        self.chkbutton[2].controlLeft(self.chkbutton[1]);self.chkbutton[2].controlRight(self.chkbutton[0]);
        
        self.cancelled=False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton);self.okbutton.controlRight(self.cancelbutton); 
        self.cancelbutton.controlLeft(self.okbutton); self.cancelbutton.controlRight(self.okbutton);
        self.okbutton.controlDown(self.chkbutton[2]);self.okbutton.controlUp(self.chkbutton[8]); 
        self.cancelbutton.controlDown(self.chkbutton[0]); self.cancelbutton.controlUp(self.chkbutton[6]);         
        #self.kbd = xbmc.Keyboard()

    def get(self):
        self.doModal()
        #self.kbd.doModal()
        #if (self.kbd.isConfirmed()):
        #   text = self.kbd.getText()
        #   self.close()
        #   return text
        #xbmc.sleep(5000)
        self.close()
        if not self.cancelled:     
            retval=""
            for objn in range(9):
                if self.chkstate[objn]:#self.chk[objn].getSelected() :
                    retval+=("" if retval=="" else ",")+str(objn)
            return  retval
            
        else:
            return ""
#    def onControl(self,control):
#        if control == self.okbutton:
#            self.close()
#        elif control == self.cancelbutton:
#            self.cancelled=True
#            self.close()
    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:#obj.getSelected():
                return True
        return False
    
    
    def onControl(self,control):
        if   control==self.okbutton: 
            if self.anythingChecked():
                self.close()
        elif control== self.cancelbutton:
            self.cancelled=True
            self.close()
        try:
            #print control
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index=control.getLabel()
                #print 'index',index
                if index.isnumeric():
                    #print 'index2',index
                    #self.chk[int(index)-1].setSelected(not self.chk[int(index)-1].getSelected())
                    self.chkstate[int(index)-1]= not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])
                    #print 'ddone'
                    
        except: pass
#    def onClick(self, controlId):
#        print 'CLICKED',controlId
    def onAction(self, action):
        if action == 10:#ACTION_PREVIOUS_MENU:
            self.cancelled=True
            self.close()
        
      
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None, noredir=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)

    if noredir:
        opener = urllib2.build_opener(NoRedirection,cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    else:
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

class UnCaptchaReCaptcha:

    def _collect_api_info(self):
        html = getUrl("http://www.google.com/recaptcha/api.js")
        a    = re.search(r'po.src = \'(.*?)\';', html).group(1)
        vers = a.split("/")[5]

        print ("API version: %s" % vers)

        language = a.split("__")[1].split(".")[0]

        print ("API language: %s" % language)

        html = getUrl("https://apis.google.com/js/api.js")
        b    = re.search(r'"h":"(.*?)","', html).group(1)
        jsh  = b.decode('unicode-escape')

        print ("API jsh-string: %s" % jsh)

        return vers, language, jsh


    def _prepare_time_and_rpc(self):
        #getUrl("http://www.google.com/recaptcha/api2/demo")

        millis = int(round(time.time() * 1000))

        print ("Time: %s" % millis)

        rand = random.randint(1, 99999999)
        a    = "0.%s" % str(rand * 2147483647)
        rpc  = int(100000000 * float(a))

        print ("Rpc-token: %s" % rpc)

        return millis, rpc
        
    def processCaptcha(self, key,lang,gcookieJar):
        
        headers=[("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"),
                 ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                 ("Referer", "https://www.google.com/recaptcha/api2/demo/"),
                 ("Accept-Language", lang)];

        botguardstring      = "!A"
        vers, language, jsh = self._collect_api_info()
        millis, rpc         = self._prepare_time_and_rpc()
        
        parent="www.google.com/recaptcha/api2/demo/"
        html =getUrl("https://www.google.com/recaptcha/api2/anchor?"+
                            urllib.urlencode({'k'       : key,
                                 'hl'      : language,
                                 'v'       : vers,
                                 'co' : "aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbTo0NDM.",
                                 'size'     : "large", "cb"  : "8shiuzd0nyrv"}),headers=headers)

        token1 = re.search(r'id="recaptcha-token" value="(.*?)">', html)
        
        
        frameurl="https://www.google.com/recaptcha/api2/frame?"+urllib.urlencode({'c'      : token1.group(1),
                                     'hl'     : language,
                                     'v'      : vers,
                                     'bg'     : botguardstring,
                                     'k'      : key})
        html = getUrl(frameurl).decode("unicode-escape")
        
        #html = getUrl("https://www.google.com/recaptcha/api2/reload?k="+key,
        #                         post=urllib.urlencode({'c'      : token1.group(1),
        #                            'hl'     : language,
        #                             'v'      : vers,
        #                             'bg'     : botguardstring,
        #                             'reason'     : "t"}),headers=headers).decode("unicode-escape")
        
       
        #self.log_debug("Token #3: %s" % token3.group(1))
        
        
        
        #captcha_response =getUrl("https://www.google.com/recaptcha/api2/payload?"+
                                              #urllib.urlencode({'c':token3.group(1), 'k':key}),headers=headers)
                                              
        
        
        
        
#        self.log_debug("Token #1: %s" % token1.group(1))


        
        #html=getUrl("http://www.google.com/recaptcha/api/fallback?k=" + key,headers=headers);
        token=""
        roundnum=0
        first=True
        while True:

            message=""
            millis_captcha_loading= int(round(time.time() * 1000))

            
            token2 = re.search(r'"finput","(.*?)",', html)
            #self.log_debug("Token #2: %s" % token2.group(1))

            token3 = re.search(r'"rresp","(.*?)",', html)
            cval=token3.group(1)
            captcha_imgurl="https://www.google.com/recaptcha/api2/payload?"+urllib.urlencode({'c':token3.group(1), 'k':key})
            #response = base64.b64encode('{"response":"%s"}' % captcha_response)
        
            first=True
            if not first:
                payload = re.findall("\"(/recaptcha/api2/payload[^\"]+)",html);
                roundnum+=1
                message =re.findall("<label .*?class=\"fbc-imageselect-message-text\">(.*?)</label>",html);
                if len(message)==0:
                    message =re.findall("<div .*?class=\"fbc-imageselect-message-error\">(.*?)</div>",html)
                if len(message)==0:
                    token = re.findall("\"this\\.select\\(\\)\">(.*?)</textarea>",html)[0];
                    if not token=="":
                        line1 = "Captcha Sucessfull"
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('LSPro',line1, 3000, None))
                    else:
                        line1 = "Captcha failed"
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('LSPro',line1, 3000, None))
                    break
                else:
                    message=message[0]
                    payload=payload[0]


                imgurl=re.findall("name=\"c\"\\s+value=\\s*\"([^\"]+)",html)[0]
                cval=re.findall('name="c" value="(.*?)"',html)[0]
                captcha_imgurl = "https://www.google.com"+payload.replace('&amp;','&')
            
            headers=[("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"),
                 ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                 ("Referer", frameurl),
                 ("Accept-Language", lang)];
               


            html=getUrl(captcha_imgurl,headers=headers,cookieJar=gcookieJar);
            
            #print message
            message=message.replace('<strong>','')
            message=message.replace('</strong>','')
            #captcha_response=raw_input('-->')
            
            oSolver = cInputWindow(captcha = captcha_imgurl,msg = message,roundnum=roundnum)
            captcha_response = oSolver.get()
            #print 'captcha_response',captcha_response
            if captcha_response=="":
                break
            responses=""
            
            if 1==2:
                for rr in captcha_response.split(','):
                    responses += "&response=" + rr;
            else:
                    responses = base64.b64encode('{"response":"%s"}' % captcha_response)
                    responses=responses.replace('=','.')
                    ##responses="eyJyZXNwb25zZSI6IjAsMSwzLDYifQ.."
           
            timeToSolve     = int(round(time.time() * 1000)) - millis_captcha_loading
            timeToSolveMore = timeToSolve#timeToSolve + int(float("0." + str(random.randint(1, 99999999))) * 500)

            html = getUrl("https://www.google.com/recaptcha/api2/userverify?k="+key,
                                    post=urllib.urlencode({'c'       : cval,
                                          'response': responses,
                                          'v'      : vers,
                                          't'       : timeToSolve,
                                          'bg'     : botguardstring,
                                          'ct'      : timeToSolveMore}),headers=headers)
            if first and '["bgdata"' not in html:
               token3 = re.search(r'"uvresp","(.*?)",', html)
               return token3.group(1)
        return token

def getg():
    return None
    cookieJar = cookielib.LWPCookieJar()
    try:
        cookieJar.load("./gsite.jwl")
    except:
        pass
        
def performCaptcha(sitename,cj,returnpage=True,captcharegex='data-sitekey="(.*?)"',lang="en",headers=None):

    gcookieJar = getg()
    sitepage=getUrl(sitename,cookieJar=cj,headers=headers)
    sitekey=re.findall(captcharegex,sitepage)
    token=""
    if len(sitekey)>=1:
        #getUrl('https://www.google.com/',cookieJar=gcookieJar)
        c=UnCaptchaReCaptcha()
        token=c.processCaptcha(sitekey[0],lang,gcookieJar)
        if returnpage:
            #gcookieJar.save('./gsite.jwl');
            headers=[("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"),
             ("Referer", sitename)];
            sitepage=getUrl(sitename,cookieJar=cj,post=urllib.urlencode({"g-recaptcha-response":token}),headers=headers)
            
    if returnpage:
        return sitepage
    else:
        return token


##performCaptcha("http://www.livetv.tn/",cookieJar);


