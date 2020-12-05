#!/usr/bin/env python3
import os
import sys
import pprint
import hashlib

topsList = ['/backups/jim3/', '/backups/jim4/']
#topsList = ['/backups/jim3/']
#topsList = [['a', 'bb', 'ccc'], ['dddd', 'eeeee']]
topsList = [['/backups/jim3/hourly.6/home/jim/bin/', '/backups/jim3/hourly.6/home/jim/bin/']]
topsList = [['/backups/jim3/daily.5/home/jim/audio/', '/backups/jim3/daily.6/home/jim/audio/']]
topsList = [['/mnt/t1/jim3backup/daily.0/audio/CDs/flac/Folk/Various/Once/',
             '/mnt/t1/jim3backup/daily.1/audio/CDs/flac/Folk/Various/Once/',
             '/mnt/t1/jim3backup/daily.2/audio/CDs/flac/Folk/Various/Once/',
             '/mnt/t1/jim3backup/daily.5/audio/CDs/flac/Folk/Various/Once/',
             '/mnt/t1/jim3backup/daily.6/audio/CDs/flac/Folk/Various/Once/']]
             
pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)
debugCnt = 0
debugMax = 10
for topList in topsList:
    print('Processing topList:', topList)
    sizes = {}
    inodes = {}
    for top in topList:
        print('..Processing top:', top)
        for root, dirs, files in os.walk(top):
            for name in files:
                debugCnt += 1
                filename = os.path.join(root, name)
                statinfo = os.stat(filename, follow_symlinks = False)
                size = statinfo.st_size
                inode = statinfo.st_ino
                dev = statinfo.st_dev
                hardlinks = statinfo.st_nlink
                if name[:1] == '0':
                    continue
                if os.path.isfile(filename):
                    #print(debugCnt, ': ', size, dev, inode, filename)
                    if size not in sizes:
                        sizes[size] = {}
                    if inode not in sizes[size]:
                        sizes[size][inode] = {}
                        sizes[size][inode]['links'] = hardlinks
                        sizes[size][inode]['names'] = []
                    sizes[size][inode]['names'].append(filename)
                else:
                    print('Not a file:', filename)
    
    for size in sizes:
        #print(size)
        for inode in sizes[size]:
            #print(inode, len(sizes[size][inode]['names']))
            if len(sizes[size][inode]['names']) == 1:
                size[size][inode]['md5sum'] = False
            else:
                file = sizes[size][inode]['names'][0]
                with open(file, 'rb') as file_to_check:
                    # read contents of the file
                    data = file_to_check.read()    
                    # pipe contents of the file through
                    md5 = hashlib.md5(data).hexdigest()
                sizes[size][inode]['md5sum'] = md5
    
    pp.pprint(sizes)
    for size in sizes:
        maxV = -1
        maxK = None
        for inode in sizes[size]:
            if sizes[size][inode]['links'] > maxV:
                maxV = sizes[size][inode]['links']
                maxK = inode
        basefile = sizes[size][maxK]['names'][0]
        #print(size, maxK, maxV, basefile)
        for inode in sizes[size]:
            if inode == maxK:
                continue
            if sizes[size][maxK]['md5sum'] == sizes[size][inode]['md5sum']:
                for name in sizes[size][inode]['names']:
                    print('ln ', basefile, ' ', name)
                    #os.link(basefile, name)
                