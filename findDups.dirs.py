#!/usr/bin/env -S python3 -u
import os
import sys
import pprint
import hashlib


ShowInterval = 131072
ShowInterval = 4096
whichList    = 5
minSize      = 2048

def get_md5(file, size = False):
    global md5sumCnt
    global showInterval
    try:
        with open(file, 'rb') as file_to_check:
            # read contents of the file
            if size:
                data = file_to_check.read(size)
            else:
                data = file_to_check.read()
                md5sumCnt += 1
                if md5sumCnt % showInterval == 0:
                    print('md5sum:', md5sumCnt,  file)
            # pipe contents of the file through
            md5 = hashlib.md5(data).hexdigest()
    except:
        print('md5sum failed for:', file)
        md5 = False
    return md5

if   whichList == 0:
    topsList = [['/backups/jim3/'], ['/backups/jim4/']]
elif whichList == 1:
    topsList = [['/backups/jim3/']]
elif whichList == 2:
    topsList = [['/backups/jim3/hourly.6/home/jim/bin/', '/backups/jim3/hourly.6/home/jim/bin/']]
elif whichList == 3:
    topsList = [['/backups/jim3/daily.5/home/jim/audio/', '/backups/jim3/daily.6/home/jim/audio/']]
elif whichList == 4:
    topsList = [['/mnt/t1/jim3backup/daily.0/audio/CDs/flac/Folk/Various/Once/',
                 '/mnt/t1/jim3backup/daily.1/audio/CDs/flac/Folk/Various/Once/',
                 '/mnt/t1/jim3backup/daily.2/audio/CDs/flac/Folk/Various/Once/',
                 '/mnt/t1/jim3backup/daily.5/audio/CDs/flac/Folk/Various/Once/',
                 '/mnt/t1/jim3backup/daily.6/audio/CDs/flac/Folk/Various/Once/']]
elif whichList == 5:
    topsList = [['/backups/jim4/daily.0/home/jim/bin/',
                 '/backups/jim4/daily.1/home/jim/bin/', 
                 '/backups/jim4/daily.2/home/jim/bin/',
                 '/backups/jim4/daily.3/home/jim/bin/', 
                 '/backups/jim4/daily.4/home/jim/bin/',
                 '/backups/jim4/daily.5/home/jim/bin/', 
                 '/backups/jim4/daily.6/home/jim/bin/',
                 '/backups/jim4/hourly.0/home/jim/bin/', 
                 '/backups/jim4/hourly.1/home/jim/bin/',
                 '/backups/jim4/hourly.2/home/jim/bin/', 
                 '/backups/jim4/hourly.3/home/jim/bin/',
                 '/backups/jim4/hourly.4/home/jim/bin/', 
                 '/backups/jim4/hourly.5/home/jim/bin/',
                 '/backups/jim4/hourly.6/home/jim/bin/', 
                 '/backups/jim4/monthly.0/home/jim/bin/',
                 '/backups/jim4/monthly.10/home/jim/bin/', 
                 '/backups/jim4/monthly.11/home/jim/bin/',
                 '/backups/jim4/monthly.12/home/jim/bin/', 
                 '/backups/jim4/monthly.13/home/jim/bin/',
                 '/backups/jim4/monthly.14/home/jim/bin/', 
                 '/backups/jim4/monthly.15/home/jim/bin/',
                 '/backups/jim4/monthly.16/home/jim/bin/', 
                 '/backups/jim4/monthly.17/home/jim/bin/',
                 '/backups/jim4/monthly.18/home/jim/bin/', 
                 '/backups/jim4/monthly.19/home/jim/bin/',
                 '/backups/jim4/monthly.1/home/jim/bin/', 
                 '/backups/jim4/monthly.20/home/jim/bin/',
                 '/backups/jim4/monthly.21/home/jim/bin/', 
                 '/backups/jim4/monthly.22/home/jim/bin/',
                 '/backups/jim4/monthly.23/home/jim/bin/', 
                 '/backups/jim4/monthly.24/home/jim/bin/',
                 '/backups/jim4/monthly.2/home/jim/bin/', 
                 '/backups/jim4/monthly.3/home/jim/bin/',
                 '/backups/jim4/monthly.4/home/jim/bin/', 
                 '/backups/jim4/monthly.5/home/jim/bin/',
                 '/backups/jim4/monthly.6/home/jim/bin/', 
                 '/backups/jim4/monthly.7/home/jim/bin/',
                 '/backups/jim4/monthly.8/home/jim/bin/', 
                 '/backups/jim4/monthly.9/home/jim/bin/',
                 '/backups/jim4/weekly.0/home/jim/bin/', 
                 '/backups/jim4/weekly.1/home/jim/bin/',
                 '/backups/jim4/weekly.2/home/jim/bin/', 
                 '/backups/jim4/weekly.3/home/jim/bin/',
                 '/backups/jim4/weekly.4/home/jim/bin/', 
                 '/backups/jim4/weekly.5/home/jim/bin/']]
elif whichList == 6:
    topsList = [['/backups/jim4/daily.0/home/jim',
                 '/backups/jim4/daily.1/home/jim', 
                 '/backups/jim4/daily.2/home/jim',
                 '/backups/jim4/daily.3/home/jim', 
                 '/backups/jim4/daily.4/home/jim',
                 '/backups/jim4/daily.5/home/jim', 
                 '/backups/jim4/daily.6/home/jim',
                 '/backups/jim4/hourly.0/home/jim', 
                 '/backups/jim4/hourly.1/home/jim',
                 '/backups/jim4/hourly.2/home/jim', 
                 '/backups/jim4/hourly.3/home/jim',
                 '/backups/jim4/hourly.4/home/jim', 
                 '/backups/jim4/hourly.5/home/jim',
                 '/backups/jim4/hourly.6/home/jim', 
                 '/backups/jim4/monthly.0/home/jim',
                 '/backups/jim4/monthly.10/home/jim', 
                 '/backups/jim4/monthly.11/home/jim',
                 '/backups/jim4/monthly.12/home/jim', 
                 '/backups/jim4/monthly.13/home/jim',
                 '/backups/jim4/monthly.14/home/jim', 
                 '/backups/jim4/monthly.15/home/jim',
                 '/backups/jim4/monthly.16/home/jim', 
                 '/backups/jim4/monthly.17/home/jim',
                 '/backups/jim4/monthly.18/home/jim', 
                 '/backups/jim4/monthly.19/home/jim',
                 '/backups/jim4/monthly.1/home/jim', 
                 '/backups/jim4/monthly.20/home/jim',
                 '/backups/jim4/monthly.21/home/jim', 
                 '/backups/jim4/monthly.22/home/jim',
                 '/backups/jim4/monthly.23/home/jim', 
                 '/backups/jim4/monthly.24/home/jim',
                 '/backups/jim4/monthly.2/home/jim', 
                 '/backups/jim4/monthly.3/home/jim',
                 '/backups/jim4/monthly.4/home/jim', 
                 '/backups/jim4/monthly.5/home/jim',
                 '/backups/jim4/monthly.6/home/jim', 
                 '/backups/jim4/monthly.7/home/jim',
                 '/backups/jim4/monthly.8/home/jim', 
                 '/backups/jim4/monthly.9/home/jim',
                 '/backups/jim4/weekly.0/home/jim', 
                 '/backups/jim4/weekly.1/home/jim',
                 '/backups/jim4/weekly.2/home/jim', 
                 '/backups/jim4/weekly.3/home/jim',
                 '/backups/jim4/weekly.4/home/jim', 
                 '/backups/jim4/weekly.5/home/jim']]    
elif whichList == 7:
    topsList = [['/backups/jim4/daily.0/home/jim/audio/CDs/flac/',
                 '/backups/jim4/daily.1/home/jim/audio/CDs/flac/']]
elif whichList == 8:
    topsList = [['/home/jim/tools/findDups/test']]
else:
    print('Out of range!!!')
          
pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)

for topList in topsList:
    print('Processing topList:', topList)
    sizes        = {}
    inodes       = {}
    debugCnt     = 0
    md5sumCnt    = 0
    md5smplCnt   = 0
    scanCnt      = 0
    sizeCnt      = 0
    inodeCnt     = 0
    nameCnt      = 0
    nonFileCnt   = 0
    showInterval = ShowInterval
    fileSampleSz = 4096
    directories         = []
    for top in topList:
        print('..Processing top:', top)
        for root, dirs, files in os.walk(top):
            dirNo = len(directories)
            directories.append(root)
            for name in files:
                debugCnt += 1
                filename = os.path.join(root, name)
                statinfo = os.stat(filename, follow_symlinks = False)
                size = statinfo.st_size
                inode = statinfo.st_ino
                dev = statinfo.st_dev
                hardlinks = statinfo.st_nlink
                #if name[:1] == '0':
                    #continue
                if size < minSize:
                    # skip the little files
                    continue    
                if os.path.isfile(filename):
                    if debugCnt % showInterval == 0:
                        try:
                            print(debugCnt, ': ', size, dev, inode, filename)
                        except:
                            print(debugCnt, ': ', size, dev, inode, '=== unprintable ===')
                    if size not in sizes:
                        sizes[size] = {}
                        sizeCnt += 1
                    if inode not in sizes[size]:
                        sizes[size][inode] = {}
                        sizes[size][inode]['links'] = hardlinks
                        sizes[size][inode]['names'] = []
                        #sizes[size][inode]['md5_sample'] = get_md5(filename, size = fileSampleSz)
                        sizes[size][inode]['md5_sample'] = False
                        # end test
                        sizes[size][inode]['md5sum'] = False
                        sizes[size][inode]['dirNo'] = []
                        inodeCnt += 1
                    sizes[size][inode]['names'].append(name)
                    sizes[size][inode]['dirNo'].append(dirNo)
                    nameCnt += 1
                else:
                    #print('Not a file:', filename)
                    nonFileCnt += 1
    print('\nSizes:\t\t', sizeCnt, '\nInodes:\t\t', inodeCnt, '\nNames:\t\t', nameCnt,
          '\nNonFiles:\t', nonFileCnt, '\n')
    only1 = 0
    for size in sizes:
        if len(sizes[size]) == 1:
            only1 += 1
    print('\nSingleInode:\t', only1, '\n')
    
    for size in sizes:
        if len(sizes[size]) > 1:
            for inode in sorted(sizes[size]):
                try:
                    filename  = os.path.join(directories[sizes[size][inode]['dirNo'][0]],
                                             sizes[size][inode]['names'][0])
                except:
                    print('QQQQQQQQQQQQQQ')
                    print(size, inode, sizes[size])
                    pp.pprint(sizes[size][inode])
                sizes[size][inode]['md5_sample'] = get_md5(filename, size = fileSampleSz)
                md5smplCnt += 1
                if md5smplCnt % showInterval == 0:
                    try:
                        print('md5 sample:', md5smplCnt, size, inode, filename)
                    except:
                        print('md5 sample:', md5smplCnt, size, inode, '=== unprintable ===')
    
    pp.pprint(sizes)
    pp.pprint(directories)
    
    for size in sizes:
        for inode1 in sorted(sizes[size]):
            for inode2 in sorted(sizes[size]):
                if inode2 <= inode1:
                    continue
                scanCnt += 1
                if len(sizes[size][inode1]['names']) > 0:
                    fn1 = os.path.join(directories[sizes[size][inode1]['dirNo'][0]],
                                       sizes[size][inode1]['names'][0])
                else:
                    fn1 = os.path.join(directories[sizes[size][inode1]['dirNo'][0]], '*n/a*')
                if len(sizes[size][inode2]['names']) > 0:  
                    fn2 = os.path.join(directories[sizes[size][inode2]['dirNo'][0]],
                                       sizes[size][inode2]['names'][0])
                else:
                    fn2 = os.path.join(directories[sizes[size][inode2]['dirNo'][0]], '*n/a*')
                if scanCnt % showInterval == 0:
                    print(size, inode1, sizes[size][inode1])
                    try:
                        print('scan:', scanCnt, fn1)
                    except:
                        print('scan:', scanCnt, '=== unprintable ===')
                if not (sizes[size][inode1]['md5_sample'] and sizes[size][inode2]['md5_sample']):
                    print('No sample md5 for:', fn1, ' or ', fn2)
                    continue
                if sizes[size][inode1]['md5_sample'] != sizes[size][inode2]['md5_sample']:
                    # if the first parts do not match, the rest can not match
                    continue
                if not sizes[size][inode1]['md5sum']:
                    sizes[size][inode1]['md5sum'] = get_md5(fn1)
                if not sizes[size][inode2]['md5sum']:
                    sizes[size][inode2]['md5sum'] = get_md5(fn2)
                if sizes[size][inode1]['md5sum'] == sizes[size][inode2]['md5sum']:
                    if sizes[size][inode1]['links'] == sizes[size][inode2]['links']:
                        base  = inode1
                        target = inode2
                    else:
                        base  = inode2
                        target = inode1
                    if len(sizes[size][base]['names']) < 1:
                        continue
                    basefile = os.path.join(directories[sizes[size][base]['dirNo'][0]],
                                            sizes[size][base]['names'][0])
                    for name, dirNo in zip(sizes[size][target]['names'],
                                           sizes[size][target]['dirNo']) :
                        tgtfile = os.path.join(directories[dirNo], name)
                        try:
                            print('ZZln ', basefile, ' ', tgtfile)
                        except:
                            print('ZZln ', sizes[size][base], sizes[size][target], '=== unprintable ===')
                        #os.link(basefile, tgtfile)
                    sizes[size][base]['names']  += sizes[size][target]['names']
                    sizes[size][target]['names'] = []
                    sizes[size][base]['links']  += sizes[size][target]['links']
                    sizes[size][target]['links'] = 0
    pp.pprint(sizes)
