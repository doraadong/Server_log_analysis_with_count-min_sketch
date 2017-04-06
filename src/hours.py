
import re
from datetime import datetime,timedelta
from collections import deque 
import heapq

class hours:

    # setup regex to be used by this feature
    regex = {}
    regex['datetime'] = re.compile(r'(\d{2}\/\w+\/\d{4}:\d{2}:\d{2}:\d{2})')
    regex['time_zone'] = re.compile(r'(\-\d{4})')
    
    # setup data structures to store counts
    dq = deque() # store a counter [count, start_time, UTC_OFFSET]
    heap = [] # store a counter [count, start_time, UTC_OFFSET]
    
    def __init__(self, window_size, k):
        # setup variables specific to the instance
        self.window_size = 3600 # 60min = 3600s
        self.k = 10 # top 10
        
    def process_line(self, line, output):
        
        # get data
        line = line.strip()
        _raw = re.search(self.regex['datetime'],line).group(0) 
        _timezone = re.search(self.regex['time_zone'],line).group(0) 
        
        _temp = datetime.strptime(_raw +_timezone, '%d/%b/%Y:%H:%M:%S%z')
        
        # convert to UTC time 
        UTC_OFFSET = datetime.utcoffset(_temp) 
        current = _temp - UTC_OFFSET 
        
        while len(self.dq) >= 1 and self.dq[-1][1] < current:
            counter = [0,self.dq[-1][1]+timedelta(seconds=1),UTC_OFFSET] 
            self.dq.append(counter)
            if len(self.dq) > self.window_size:
                head = self.dq.popleft()
                heapq.heappush(self.heap, head)
                if len(self.heap) > k:
                    heapq.heappop(self.heap) 
                    
        if len(self.dq) == 0:
            self.dq.append([0,current,UTC_OFFSET])
        for entry in self.dq:
            entry[0]+=1
            
    def print_results(self, output):
        
        # if deque is not empty, pop all and put them in heap
        while self.dq:
            tail = self.dq.pop()
            heapq.heappush(self.heap, tail)
            if len(self.heap) > self.k:
                heapq.heappop(self.heap)  
          
        # print out final results 
        _temp = []
        while self.heap: 
            count,date,offset = heapq.heappop(self.heap)
            _temp.append([count,date,offset])
        
        i = len(_temp)-1
        while i >= 0:
            count,date,offset = _temp[i]
            localtime = (date + offset).strftime('%d/%b/%Y:%H:%M:%S%z')
            _datetime = re.search(self.regex['datetime'],localtime).group(0) 
            _timezone = re.search(self.regex['time_zone'],localtime).group(0) 
            output.write(_datetime +' '+ _timezone +',' +str(count) + '\n') 
            i-=1