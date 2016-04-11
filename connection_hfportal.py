import os
import json
import urllib
from urllib2 import urlopen, Request

def get_submissions(hw_id, state = 0):    
    try:
        if state:
            response = urlopen('https://hf.mit.bme.hu/api.php?get_submission_list=%d&status=%d' % (int(hw_id), int(state)))
        else:	
            response = urlopen('https://hf.mit.bme.hu/api.php?get_submission_list=%d' % int(hw_id))
        data = response.read()    
        return json.loads(data)
    except Exception as e:
        return []

def get_submission_file(id):    
    response = urlopen('https://hf.mit.bme.hu/api.php?get_submission_file=%d' % int(id))
    data = response.read()
    return data

'''
0 = Beadva
1 = El?feldolgoz?s alatt
2 = El?feldolgoz?s k?sz
3 = Automatikus ki?rt?kel?s alatt
4 = Automatikus ki?rt?kel?s fut
5 = K?zi ki?rt?kel?s alatt
6 = K?zi ki?rt?kel?s k?sz
7 = ?rt?kel?s lez?rva
9 = ?rt?kel?s megszak?tva
10 = El?feldolgoz?s megszak?tva
'''

def post_result(id, sender, state, result, comment):    
    values = {
        'sender': sender,
        'state' : state,
        'result' : result,
        'comment' : comment
    }
    data = urllib.urlencode(values)
    response = urlopen('https://hf.mit.bme.hu/api.php?set_result=%d' % int(id), data)
    databack = response.read()
    return databack
