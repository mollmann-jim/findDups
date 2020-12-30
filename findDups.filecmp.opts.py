#!/usr/bin/env -S python3 -u
import os
import sys
import pprint
import hashlib
import filecmp
import argparse

MAXSIZE = 1024 ** 5
optsP = argparse.ArgumentParser(description = 'Options')
optsP.add_argument('-s', '--show-interval', default=131072,  type=int, action='store', help='progress output interval')
optsP.add_argument('-m', '--minimum-size',  default=1048576, type=int, action='store', help='minimum file size to process')
optsP.add_argument('-M', '--maximum-size',  default=MAXSIZE, type=int, action='store', help='maximum file size to process')
optsP.add_argument('-d', '--directories',   default=[],      nargs='+',                help='list of directories to scan')
optsP.add_argument('-n', '--dry-run',       default=True,              action='store', help='make no changes')
opts = optsP.parse_args()
print(opts)

ShowInterval = opts.show_interval
minSize      = opts.minimum_size
maxSize      = opts.maximum_size
dryRun       = opts.dry_run
topsList     = []
topsList.append(opts.directories)

print(ShowInterval, minSize, maxSize, topsList, dryRun)

pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)

for topList in topsList:
    print('Processing topList:', topList)
    sizes        = {}
    inodes       = {}
    debugCnt     = 0
    compareCnt   = 0
    scanCnt      = 0
    sizeCnt      = 0
    inodeCnt     = 0
    nameCnt      = 0
    nonFileCnt   = 0
    linkCnt      = 0
    linkedSize   = 0
    showInterval = ShowInterval
    directories         = []
    for top in topList:
        print('..Processing top:', top)
        for root, dirs, files in os.walk(top):
            dirNo = len(directories)
            directories.append(root)
            for name in files:
                filename = os.path.join(root, name)
                statinfo = os.stat(filename, follow_symlinks = False)
                size = statinfo.st_size
                inode = statinfo.st_ino
                dev = statinfo.st_dev
                hardlinks = statinfo.st_nlink
                if size < minSize:
                    # skip the little files
                    continue
                if size > maxSize:
                    # skip the giant files
                    continue
                debugCnt += 1
                if debugCnt % showInterval == 0:
                    try:
                        print(debugCnt, ': ', size, dev, inode, filename)
                    except:
                        print(debugCnt, ': ', size, dev, inode, '=== unprintable ===')
                if os.path.isfile(filename):
                    if size not in sizes:
                        sizes[size] = {}
                        sizeCnt += 1
                    if inode not in sizes[size]:
                        sizes[size][inode] = {}
                        sizes[size][inode]['links'] = hardlinks
                        sizes[size][inode]['names'] = []
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
    
    #pp.pprint(sizes)
    #pp.pprint(directories)
    
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
                    #print(size, inode1, sizes[size][inode1])
                    try:
                        print('scan:', scanCnt, fn1)
                    except:
                        print('scan:', scanCnt, '=== unprintable ===')

                if sizes[size][inode1]['links'] == 0 or sizes[size][inode2]['links'] == 0:
                    # already linked one of them
                    continue                                                               
                compareCnt += 1
                basefile = os.path.join(directories[sizes[size][inode1]['dirNo'][0]],
                                        sizes[size][inode1]['names'][0])
                tgtfile  = os.path.join(directories[sizes[size][inode2]['dirNo'][0]],
                                        sizes[size][inode2]['names'][0])
                if filecmp.cmp(basefile, tgtfile, shallow = False):
                    if sizes[size][inode1]['links'] >= sizes[size][inode2]['links']:
                        base  = inode1
                        target = inode2
                    else:
                        base  = inode2
                        target = inode1
                    if len(sizes[size][base]['names']) < 1:
                        continue
                    basefile = os.path.join(directories[sizes[size][base]['dirNo'][0]],
                                            sizes[size][base]['names'][0])
                    linkedSize += size
                    for name, dirNo in zip(sizes[size][target]['names'],
                                           sizes[size][target]['dirNo']) :
                        tgtfile = os.path.join(directories[dirNo], name)
                        try:
                            print('ZZln ', basefile, ' ', tgtfile)
                            print('dryRun:', dryRun)
                        except:
                            print('ZZln ', sizes[size][base], sizes[size][target], '=== unprintable ===')
                        if dryRun is not True:
                            print('os.link(', basefile, tgtfile)
                            os.unlink(tgtfile)
                            os.link(basefile, tgtfile)
                        linkCnt += 1
                    sizes[size][base]['names']  += sizes[size][target]['names']
                    sizes[size][target]['names'][0] = sizes[size][target]['names'][0]
                    sizes[size][base]['links']  += sizes[size][target]['links']
                    sizes[size][target]['links'] = 0
    #pp.pprint(sizes)
    print('\nfile compares:\t', compareCnt)
    print('\nlink calls:\t', linkCnt)
    print('\nbytes linked:\t', linkedSize,'\t', linkedSize/1024, 'K\t',
          linkedSize/1024/1024, 'M\t', linkedSize/1024/1024/1024, 'G')
