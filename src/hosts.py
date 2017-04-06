
import re
import cm_sketch as cms
import heapq

class hosts:

    # setup regex to be used by this feature
    regex = {}
    regex['host'] = re.compile(r'^(\S*)\s+')

    def __init__(self, k, d, w):
        # setup variables specific to the instance
        self.k = k # top 10
        self.d = d # parameters for count-min sketch
        self.w = w # parameters for count-min sketch
        self.sk = cms.cm_sketch(d=d,w=w,k=k)
        
    def process_line(self, line, output):
        
        # get data
        line = line.strip()
        _host = re.search(self.regex['host'],line).group(0).rstrip()
        
        self.sk.update(_host,1)
            
    def print_results(self, output):
        
        # print out final results 
        _temp = []
        while self.sk.heap: 
            count,host = heapq.heappop(self.sk.heap)
            _temp.append([host,count])
        
        i = len(_temp)-1
        while i >= 0:
            host,count = _temp[i]
            output.write(host +' ' + str(count) + '\n') 
            i-=1