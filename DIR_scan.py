#encoding:utf-8
import getopt
import requests
import threading
import random
from urllib import quote
import optparse
class main(object):
    def __init__(self):
        self.path = []
        self.types = ['PHP','ASP','JSP','ASPX']
        self.result = {}
    def _getPath(self,fileType):
        fileType = fileType.upper()
        if fileType not in self.types:
            print "[*]Fucking noob,fileType Error\n"
            print "Types:\n"
            print self.types
            return False
        dPath = "./Dirs/%s.txt"
        files = [dPath % 'MDB',dPath % 'DIR',dPath % 'JSP',dPath % fileType]
        for file in files:
            f = open(file, 'r')
            for line in f.readlines():
                if line in self.path:
                    continue
                self.path.append(line.replace('\n',''))
            f.close()
        print len(self.path)
#Have one request
    def req_one(self,host):
        while len(self.path)>0:
            path = quote(random.choice(self.path))
            url = host+'/'+path
            req = requests.get(url,timeout=3)
            if req.status_code != 404:
                self.result[host+path] = req.status_code
                print '[+]%s----%s' % (url,req.status_code)
        self.path.remove(path)

    def print_res(self):
        print self.result
        for key in self.result:
            print "%s------%s" % key,self.result[key]
if __name__ == '__main__':
    host = 'http://127.0.0.1/'
#   t_num = 200
#GET options
    parser = optparse.OptionParser(usage='usage:%prog [options] arg1 arg2')
    parser.add_option('-u','--url',dest='url',type=str)
    parser.add_option('-t','--thread',dest='t_num',type=str)
    parser.add_option('-l','--language',dest='lang',type=str)
    opts,args = parser.parse_args()
    if opts.url is not None:
        host = opts.url
    else:
        print "[*]Please use -u [url] input url"
        exit()
    if opts.t_num is not None:
        t_num = int(opts.t_num)
    else:
        t_num = 200
    if 'http' not in host:
        host = 'http://'+host
    if opts.lang is not None:
        if opts.lang.upper() in ['PHP','ASP','JSP','ASPX']:
            lang = opts.lang
        else:
            print '[-]Error language'
            exit()
    else:
        print '[-]Enter language'
        exit()
    if 'http' not in host:
        host = 'http://'+host
    main = main()
    main._getPath(lang)
#Threading
    threads = []
    for i in xrange(t_num):
        threads.append(threading.Thread(target=main.req_one,args=(host,)))
    for t in threads:
        t.start()
        t.join()
        t.deamon()
    main.print_res()