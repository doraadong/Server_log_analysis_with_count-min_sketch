
import re
from datetime import datetime,timedelta
from collections import deque 

class blocked:

    # setup regex to be used by this feature
    regex = {}
    regex['host'] = re.compile(r'^(\S*)\s+')
    regex['datetime'] = re.compile(r'(\d{2}\/\w+\/\d{4}:\d{2}:\d{2}:\d{2})')
    regex['time_zone'] = re.compile(r'(\-\d{4})')
    regex['code_and_bytes'] = re.compile(r'\s+(\d+)\s+(\d+|-)') # code: group 1; bytes: group 2
    
    # setup data structures to store blocked 
    blocked_dq = deque() # deque of [host,time]
    blocked_list = set() # set of host and entry [host,time]

    # setup data structures for counts
    count_dq = deque()  # deque of [host,time,count]
    count_map = {} # map of host and entry [host,time,count]
    
    def __init__(self,latent_seconds, blocked_minutes,threshhold):
        # setup variables specific to the instance
        self.latent_seconds = 20
        self.blocked_minutes = 5
        self.threshhold = 3 
        
    def process_line(self, line, output):
        
        # get data 
        line = line.strip()
        _time = re.search(self.regex['datetime'],line).group(0) 
        _timezone = re.search(self.regex['time_zone'],line).group(0) 
        _code = re.search(self.regex['code_and_bytes'],line).group(1) 
        _host = re.search(self.regex['host'],line).group(0).rstrip()
        
        _temp = datetime.strptime(_time+_timezone, '%d/%b/%Y:%H:%M:%S%z')
        
        # convert to UTC time 
        current = _temp - datetime.utcoffset(_temp) 
        
        # remove entries appears more than 5min ago 
        while len(self.blocked_dq) >= 1 and self.blocked_dq[0][1] < current - timedelta(minutes=self.blocked_minutes):
            _expired = self.blocked_dq.popleft()
            del self.blocked_list[_expired[0]]

        if _host in self.blocked_list:
            output.write(line + '\n')
        elif _code == '401':

            # remove entries appears more than 20s ago 
            while len(self.count_dq) >= 1 and self.count_dq[0][1] < current - timedelta(seconds=self.latent_seconds):
                _expired = self.count_dq.popleft()
                del self.count_map[_expired[0]]

            entry_old = self.count_map.get(_host,None)

            if entry_old is None:

                # if entry not exist, create one 
                entry = [_host, current, 1]
                self.count_dq.append(entry)
                self.count_map[_host] = entry
#                 print ('start counting', [_host,_time,_code])

            else:
                # if exist, increment
                entry_old[2] += 1 
#                 print ('counting', [_host,_time,_code])
                if entry_old[2] == self.threshhold:
                    self.blocked_dq.append([_host,current])
                    self.blocked_list.add(_host)
                    # no need to drop the counter, will be removed after blocking 
                    
                    
                    
    def print_results(self, output):
        pass