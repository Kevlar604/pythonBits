#!/usr/bin/env python2

import os
import subprocess
import sys
import math
import tempfile

import config
config = config.Config()

l2 = math.log(2)
def log2(x):
    return math.log(x)/l2


def get_size(fname):
    if os.path.isfile(fname):
        return os.path.getsize(fname)
    else:
        return sum(get_size(os.path.join(fname, f)) for f in os.listdir(fname))
            

def piece_size_exp(size):
    min_psize_exp = 14 #16 KiB piece size
    max_psize_exp = 24 #16 MiB piece size
    target_pnum_exp = 10 #1024 pieces
    
    psize_exp = int(math.floor(log2(size)-target_pnum_exp))
    psize_exp = min(psize_exp, max_psize_exp)
    psize_exp = max(psize_exp, min_psize_exp)
    
    return psize_exp


def make_torrent(fname):
        fsize = get_size(fname)
        psize_exp = piece_size_exp(fsize)
        
        announce_url = config.get('Tracker', 'announce_url')
        
        tmp_dir = tempfile.mkdtemp()
        out_fname = os.path.splitext(os.path.split(fname)[1])[0] + ".torrent"
        out_fname = os.path.join(tmp_dir, out_fname)
        try:
            mktorrent = subprocess.Popen([r"mktorrent", "--private",
                                          "-l", str(psize_exp),
                                          "-a", announce_url,
                                          "-c", "made with Pythonbits",
                                          "-o", out_fname,
                                          fname],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError:
            print >> sys.stderr, "Error: mktorrent not found"
            exit(1)
            
        mktorrent.wait()
        if mktorrent.returncode:
            print mktorrent.stdout.read()
            
        print "Torrent file created at file://{}".format(out_fname)
        return out_fname


if __name__ == '__main__':
    fname = sys.argv[1]
    make_torrent(fname)