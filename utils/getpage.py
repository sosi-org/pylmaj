#!/usr/bin/env python

#based on pygoogle: Kiran Bandla

try:
    import json
except ImportError,e:
    import simplejson as json
except ImportError,e:
    print e
    exit()

import sys
import urllib
import logging
#import argparse



URL = 'http://ajax.googleapis.com/ajax/services/search/web?'

SAFE_ACTIVE     = "active"
SAFE_MODERATE   = "moderate"
SAFE_OFF        = "off"

SAFE_LEVELS=["off", "moderate", "active"]

ALLOW_DUMPLICATE = True

DUPLICATE_FILTER_OFF  = 0
DUPLICATE_FILTER_ON  = 1

RSZ_SMALL = "small"
RSZ_LARGE = "large"



         


#def __setup_logging(self, level):
#        logger = logging.getLogger('pygoogle')
#        logger.setLevel(level)
#        handler = logging.StreamHandler(sys.stdout)
#        handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
#        logger.addHandler(handler)
#        self.logger = logger


#npages=2


def search_layer1_dont_use(_query, _rsz, _safe, _filtr, _hl, _npages):
        results = []
        for page in range(0,_npages):
            rsz = 8
            if _rsz == RSZ_SMALL: #?
                rsz = 4
            args = {'q' : _query,
                    'v' : '1.0',
                    'start' : page*rsz,
                    'rsz': _rsz,
                    'safe' : _safe, 
                    'filter' : _filtr,    
                    'hl'    : _hl
                    }

            q = urllib.urlencode(args)

            search_results = urllib.urlopen(URL+q)
            data = json.loads(search_results.read())

            if not data.has_key('responseStatus'):
                print('response does not have a responseStatus key')
                continue
            if data.get('responseStatus') != 200:
                print('responseStatus is not 200')
                print('responseDetails : %s'%(data.get('responseDetails', None)))
                continue

            if 1: #print_results:
                if data.has_key('responseData') and data['responseData'].has_key('results'):
                    for result in  data['responseData']['results']:
                        if result:
                            print '[%s]'%(urllib.unquote(result['titleNoFormatting']))
                            print result['content'].strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
                            print urllib.unquote(result['unescapedUrl'])+'\n'                

            results.append(data)

        return results

def search_layer1v2(_query, _safe, _filtr, _hl, _start, _rsz_small=False):
    results =[]
    #for page in range(0,_npages):
    if _rsz_small:
        _rsz = RSZ_SMALL
        #rsz = 4
    else:
        _rsz = RSZ_LARGE
        #rsz = 8

    #if _rsz == RSZ_SMALL: #?
    #    #rsz = 4
    #    pass
    #else:
    #    #rsz = 8
    #    pass

    args = {'q' : _query,
            'v' : '1.0',
            'start' : _start,           #from 0
            'rsz': _rsz,
            'safe' : _safe, 
            'filter' : _filtr,    
            'hl'    : _hl
            }

    q = urllib.urlencode(args)

    search_results = urllib.urlopen(URL+q)
    data = json.loads(search_results.read())

    if not data.has_key('responseStatus'):
        print('response does not have a responseStatus key')
        #continue
        return []
    if data.get('responseStatus') != 200:
        print('responseStatus is not 200')
        print('responseDetails : %s'%(data.get('responseDetails', None)))
        #continue
        return []

    if 0: #print_results:
        if data.has_key('responseData') and data['responseData'].has_key('results'):
            for result in  data['responseData']['results']:
                if result:
                    print '[%s]'%(urllib.unquote(result['titleNoFormatting']))
                    print result['content'].strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
                    print urllib.unquote(result['unescapedUrl'])+'\n'                

    results.append(data)

    return results


def search(query):

    	#(_query, _rsz, _safe, _filtr, _hl) = (query,RSZ_LARGE, SAFE_LEVELS[0], DUPLICATE_FILTER_OFF if ALLOW_DUMPLICATE else DUPLICATE_FILTER_ON, 'en'  )
        (_query, _safe, _filtr, _hl) = (query,SAFE_LEVELS[0], DUPLICATE_FILTER_OFF if ALLOW_DUMPLICATE else DUPLICATE_FILTER_ON, 'en'  )
        """Returns a dict of Title/URLs"""
        results = {}
        #search_results = search_layer1 (_query, _rsz, _safe, _filtr, _hl, 2) #2 pages!!
        search_results = search_layer1v2 (_query, _safe, _filtr, _hl,0,)

        if not search_results:
            print('No results returned')
            return results
        #print repr(search_results)
        #print type(search_results) #-> list
        print type(search_results[0]) 
        print type(search_results[0]) 
        print search_results[0]
        print type(search_results[0]) 
        print type(search_results[0]) 
        #each entry of the list is a dict: list of dict. See below
        #zz=search_results
        for data in search_results:
            if data.has_key('responseData') and data['responseData'].has_key('results'):
                for result in data['responseData']['results']:
                    if result and result.has_key('titleNoFormatting'):
                        title = urllib.unquote(result['titleNoFormatting'])
                        results[title] = urllib.unquote(result['unescapedUrl'])
            else:
                print('no responseData key found in response')
                print(data)
        return results


def search_rvar(query):
        #todo: multi page, but appending them as one list. (in this function)
        (_query, _safe, _filtr, _hl) = (query,SAFE_LEVELS[0], DUPLICATE_FILTER_OFF if ALLOW_DUMPLICATE else DUPLICATE_FILTER_ON, 'en'  )
        search_results = search_layer1v2 (_query, _safe, _filtr, _hl,0,)
        if not search_results:
            print('No results returned')
            return None

        return search_results

def search_robj(query):
    s=search_rvar(query)
    if s is None:
        return None
    return ResultsObject(s)


#dict entry:

"""
ex={
    u'responseData':
    {
        u'cursor':
        {
            u'moreResultsUrl': u'http://www.google.com/search?oe=utf8&ie=utf8&source=uds&start=0&safe=off&filter=1&hl=en&q=hello', 
            u'estimatedResultCount': u'108000000', 
            u'searchResultTime': u'0.17',
            u'resultCount': u'108,000,000',
            u'pages': 
            [
                {
                    u'start': u'0',
                    u'label': 1
                },
                {
                    u'start': u'8',
                    u'label': 2
                },
                {
                    u'start': u'16',
                    u'label': 3
                },
                {
                    u'start': u'24',
                    u'label': 4
                },
                {
                    u'start': u'32',
                    u'label': 5
                },
                {
                    u'start': u'40',
                    u'label': 6
                },
                {
                    u'start': u'48',
                    u'label': 7
                },
                {
                    u'start': u'56',
                    u'label': 8
                }
            ],
            u'currentPageIndex': 0
        },

        u'results':
        [
            {
                u'GsearchResultClass': u'GwebSearch',
                u'visibleUrl': u'www.hellomagazine.com',
                u'titleNoFormatting': u'HELLO! Online: celebrity &amp; royal news, magazine, babies, weddings ...',
                u'title': u'<b>HELLO</b>! Online: celebrity &amp; royal news, magazine, babies, weddings <b>...</b>',
                u'url': u'http://www.hellomagazine.com/',
                u'cacheUrl': u'http://www.google.com/search?q=cache:QzMhUCC4zBoJ:www.hellomagazine.com',
                u'unescapedUrl': u'http://www.hellomagazine.com/',
                u'content': u'<b>HELLO</b>! Online brings you the latest celebrity &amp; royal news from the UK &amp; around \nthe world, magazine exclusives, celeb babies, weddings, pregnancies and\xa0...'
            },
            ...
            {...
            }
        ]
    }, 
    u'responseDetails': None, u'responseStatus': 200
}
"""

#0xA0


class ResultsObject:
    #keeps one page worth of results each time
    #The class methods provide ways to extrat data from this.
    def __init__(self,search_results):
        self.res = search_results
        pass
    def getEstimated_count(self):
        #return self.res['responseData']['cursor']['estimatedResultCount']
        #print type(self.res)
        #print len(self.res)
        #print "[1][1][1][1][1][1][1][1][1][1][1][1][1][1]"
        #print self.res[0]
        #assert len(self.res)==1, "len=%d"%(len(self.res),)
        if not len(self.res)==1:
            print "Warning: **** len=%d"%(len(self.res),)
        #print "[1][1][1][1][1][1][1][1][1][1][1][1][1][1]"
        a= self.res[0]['responseData']
        b=a['cursor']
        c=b['estimatedResultCount']
        return c
        pass
    def _mainList(self):
        #internal use
        return self.res[0]['responseData']['results']
    def count(self):
        return len(self._mainList())
    def _mainItem(self,idx):
        #internal use
        #return self.res[0]['responseData']['results'][idx]
        return self._mainList()[idx]
    def item_obj(self,idx):
        return ResultsItemObject(self._mainItem(idx))

class ResultsItemObject:
    def __init__(self,single_item):
        #{
        #    u'GsearchResultClass': u'GwebSearch',
        #    u'visibleUrl': u'en.wikipedia.org',
        #    u'titleNoFormatting': u'Hello - Wikipedia, the free encyclopedia',
        #    u'title': u'<b>Hello</b> - Wikipedia, the free encyclopedia',
        #    u'url': u'http://en.wikipedia.org/wiki/Hello',
        #    u'cacheUrl': u'http://www.google.com/search?q=cache:oCsA1meBGrMJ:en.wikipedia.org',
        #    u'unescapedUrl': u'http://en.wikipedia.org/wiki/Hello',
        #    u'content': u'<b>Hello</b> is a ...'
        #}, 
        self.res_dict = single_item
    def getUrl(self):
        return self.res_dict['url']
    def getContent(self): #snippet content
        return self.res_dict['content']


        
import sys
argv = sys.argv
q=argv[1]
print "looking for %s"%q
#res=search(q)
#print repr(res)
#print type(res)

ro=search_robj(q)

print ro.getEstimated_count()
#print ro.item_robj
#print ro._mainItem(2)
if ro.count()>=3:
    roi= ro.item_obj(2)
else:
    roi= ro.item_obj(0)


print roi.getUrl()
print 
print roi.getContent    ()
# example usage:
# ./getpage.py "sohail site:guardian.co.uk"

# ipython -i ./getpage.py "sosi site:guardian.co.uk"
