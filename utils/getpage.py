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


DUPLICATE_FILTER_FF  = 0
DUPLICATE_FILTER_ON   = 1

RSZ_SMALL = "small"
RSZ_LARGE = "large"



         


#def __setup_logging(self, level):
#        logger = logging.getLogger('pygoogle')
#        logger.setLevel(level)
#        handler = logging.StreamHandler(sys.stdout)
#        handler.setFormatter(logging.Formatter('%(module)s %(levelname)s %(funcName)s| %(message)s'))
#        logger.addHandler(handler)
#        self.logger = logger


npages=2

def search_layer1(_query, _rsz, _safe, _filtr, _hl):
        results = []
        for page in range(0,npages):
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


def search(query):
    	(_query, _rsz, _safe, _filtr, _hl) = (query,RSZ_LARGE, SAFE_OFF, DUPLICATE_FILTER_ON, 'en'  )
        """Returns a dict of Title/URLs"""
        results = {}
        search_results = search_layer1 (_query, _rsz, _safe, _filtr, _hl)
        if not search_results:
            print('No results returned')
            return results
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

print search("hello")
