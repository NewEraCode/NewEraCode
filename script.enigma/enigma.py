import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers
from metahandler import metacontainers
import time,datetime


############################################################################################################################################################

grab = metahandlers.MetaData(preparezip = False)
engimapath = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
net = Net()

############################################################################################################################################################

#Metahandler
def GRABMETA(name,types,year=None):
        type = types
        if year=='': year=None
        EnableMeta = local.getSetting('Enable-Meta')
        #
        if year==None:
                try: year=re.search('\s*\((\d\d\d\d)\)',name).group(1)
                except: year=None
        if year is not None: name=name.replace(' ('+year+')','').replace('('+year+')','')
        #
        if EnableMeta == 'true':
                if 'Movie' in type:
                        ### grab.get_meta(media_type, name, imdb_id='', tmdb_id='', year='', overlay=6)
                        meta = grab.get_meta('movie',name,'',None,year,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',year,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        else: infoLabels=[]
        return infoLabels

def get_html(page_url):

        html = net.http_GET(page_url).content

        import HTMLParser
        h = HTMLParser.HTMLParser()
        html = h.unescape(html)
        return html.encode('utf-8')

def _FixText(t):
        if ("&amp;"  in t): t=t.replace('&amp;'  ,'&')#&amp;#x27;
        if ("&nbsp;" in t): t=t.replace('&nbsp;' ," ")
        if ('&#' in t) and (';' in t):
                t=t.replace("&#8211;",";").replace("&#8216;","'").replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"').replace('&#215;' ,'x').replace('&#x27;' ,"'").replace('&#xF4;' ,"o").replace('&#xb7;' ,"-").replace('&#xFB;' ,"u").replace('&#xE0;' ,"a").replace('&#xE9;' ,"e").replace('&#xE2;' ,"a").replace('&#0421;',"")
                if ('&#' in t) and (';' in t):
                        try:            matches=re.compile('&#(.+?);').findall(t)
                        except: matches=''
                        if (matches is not ''):
                                for match in matches:
                                        if (match is not '') and (match is not ' ') and ("&#"+match+";" in t): t=t.replace("&#"+match+";" ,"")
        for i in xrange(127,256): t=t.replace(chr(i),"")
        try: t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
        except: t=t
        return t
                       
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

#############################################################################################################################################################################
   
def smart_unicode(s):
        """credit : sfaxman"""
        if not s:
                return ''
        try:
                if not isinstance(s, basestring):
                        if hasattr(s, '__unicode__'):
                                s = unicode(s)
                        else:
                                s = unicode(str(s), 'UTF-8')
                elif not isinstance(s, unicode):
                        s = unicode(s, 'UTF-8')
        except:
                if not isinstance(s, basestring):
                        if hasattr(s, '__unicode__'):
                                s = unicode(s)
                        else:
                                s = unicode(str(s), 'ISO-8859-1')
                elif not isinstance(s, unicode):
                        s = unicode(s, 'ISO-8859-1')
        return s

                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
