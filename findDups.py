#!/usr/bin/env python3
import os
import sys
import pprint
import hashlib
import filecmp
import argparse
import datetime

# want unbuffered stdout for use with "tee"
buffered = os.getenv('PYTHONUNBUFFERED')
if buffered is None:
    myenv = os.environ.copy()
    myenv['PYTHONUNBUFFERED'] = 'Please'
    os.execve(sys.argv[0], sys.argv, myenv)
    
MAXSIZE = 1024 ** 5
optsP = argparse.ArgumentParser(description = 'Options')
optsP.add_argument('-s', '--show-interval', default=131072,  type=int, action='store', help='progress output interval')
optsP.add_argument('-m', '--minimum-size',  default=1048576, type=int, action='store', help='minimum file size to process')
optsP.add_argument('-M', '--maximum-size',  default=MAXSIZE, type=int, action='store', help='maximum file size to process')
optsP.add_argument('-n', '--dry-run',                                  action='store_true', help='make no changes')
optsP.add_argument('directories',           nargs='+',                                      help='list of directories to scan')

opts = optsP.parse_args()
print(opts)

ShowInterval = opts.show_interval
minSize      = opts.minimum_size
maxSize      = opts.maximum_size
dryRun       = opts.dry_run
topsList     = []
topsList.append(opts.directories)

now = str(datetime.datetime.now().replace(microsecond = 0))
optFmt = '{:20s}, ShowInterval: {:d}  minSize: {:d}  maxSize: {:d}  dryRun: {:s}  directories: {:s}'
print(optFmt.format( \
                     now, ShowInterval, minSize, maxSize, str(dryRun), str(topsList)))

#pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)
pp = pprint.PrettyPrinter(indent=4)

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
    goodNameCnt  = 0
    nonFileCnt   = 0
    linkCnt      = 0
    linkedSize   = 0
    showInterval = ShowInterval
    directories  = []
    walkFmt      = '{:20s}: {:9d}: size:{:12d}  dev:{:5d}  inode:{:10d}  {:s}'
    for top in topList:
        print('..Processing top:', top)
        for root, dirs, files in os.walk(top):
            dirNo = len(directories)
            directories.append(root)
            for name in files:
                nameCnt += 1
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
                    now = str(datetime.datetime.now().replace(microsecond = 0))
                    try:
                        print(walkFmt.format( \
                                              now, debugCnt, size, dev, inode, filename))
                    except:
                        print(walkFmt.format( \
                                              now, debugCnt, size, dev, inode,ize, dev, inode, '=== unprintable ==='))
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
                    goodNameCnt += 1
                else:
                    #print('Not a file:', filename)
                    nonFileCnt += 1
    print('\nSizes:\t\t', sizeCnt, '\nInodes:\t\t', inodeCnt, '\nTotal Names:\t', nameCnt,
          '\nMatching Names:\t', goodNameCnt, '\nNonFiles:\t', nonFileCnt)
    only1 = 0
    for size in sizes:
        if len(sizes[size]) == 1:
            only1 += 1
    print('SingleInode:\t', only1)
    
    #pp.pprint(sizes)
    #pp.pprint(directories)
    scanFmt = '{:20s}: {:9d}: scan    {:s}'
    linkFmt = '{:20s}: {:9d}: {:s}({:s}, {:s})'
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
                    now = str(datetime.datetime.now().replace(microsecond = 0))
                    try:
                        print(scanFmt.format(now, scanCnt, fn1))
                    except:
                        print(scanFmt.format(now, scanCnt, ' scan:',  '=== unprintable ==='))

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
                        now = str(datetime.datetime.now().replace(microsecond = 0))
                        if dryRun is False:
                            print(linkFmt.format(now, linkCnt, 'os.link', basefile, tgtfile))
                            os.unlink(tgtfile)
                            os.link(basefile, tgtfile)
                        else:
                            try:
                                print(linkFmt.format(now, linkCnt, 'zz.link', basefile, tgtfile))
                            except:
                                print(linkFmt.format(now, linkCnt, 'ZZ.link', str(sizes[size][base]), str(sizes[size][target])))
                        linkCnt += 1
                    sizes[size][base]['names']  += sizes[size][target]['names']
                    sizes[size][target]['names'][0] = sizes[size][target]['names'][0]
                    sizes[size][base]['links']  += sizes[size][target]['links']
                    sizes[size][target]['links'] = 0
    #pp.pprint(sizes)
    print('\nfile compares:\t', compareCnt)
    print('\nlink calls:\t', linkCnt)
    print('bytes linked: {:12d}  {:12.3f}K {:12.3f}M {:12.3f}G'.format( \
          linkedSize, linkedSize/1024, linkedSize/1024/1024, linkedSize/1024/1024/1024))
