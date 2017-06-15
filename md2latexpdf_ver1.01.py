#!/usr/bin/env python3

import os, sys
import argparse
import subprocess
from PIL import Image

def call_cmd(cmd):
    print("$", cmd)
    proc = subprocess.call(cmd, shell=True)
    if not proc == 0:
        sys.exit("# Cancel Document creation ...")

parser = argparse.ArgumentParser()
parser.add_argument('ifname', type=str, nargs='*')
parser.add_argument('--output', type=str, default='output.pdf')
parser.add_argument('--clean' , action='store_true', default=False)
parser.add_argument('--title', type=str, default='')
parser.add_argument('--author', type=str, default='')
parser.add_argument('--date', type=str, default='\\today')
args = parser.parse_args()

# markdown to tex format
texs = []
for fname in args.ifname:
    ofname = os.path.splitext(fname)[0] + ".tex"
    cmd = "pandoc " + fname + " -o " + ofname
    call_cmd(cmd)

# ちょこちょこ小細工
    # 画像のサイズ調整
    imgs = subprocess.check_output("grep 'includegraphics' " + ofname + " | cut -d'{' -f2 ", shell=True)
    imgs = imgs.decode('utf-8').rstrip()
    for imgf in imgs.split('\n'):
        imgf = imgf[:-1] # 末尾のゴミを捨てる
        img = Image.open(imgf)
        print(imgf, img.size)
    print('-----------', img)
#    call_cmd("sed -i '' 's|includegraphics|includegraphics[width=\\\\hsize]|g' " + ofname)
    
    call_cmd("sed -i '' 's|begin{figure}|begin{figure}[htb]|g' " + ofname)
    call_cmd("sed -i '' 's|\\\\tightlist||g' " + ofname)
    texs.append(ofname)
    print()

# create template
ofname     = os.path.splitext(args.output)[0] + "_temp"
temp_fname = ofname + ".tex"
fout       = open(temp_fname, 'w')
print("\\documentclass[11pt, a4j, uplatex]{jsarticle}", file=fout)
print("\\usepackage[dvipdfmx]{graphicx}", file=fout)
print("\\usepackage{amsmath}", file=fout)
print("\\usepackage{amssymb}", file=fout)
print("\\usepackage{amsfonts}", file=fout)
print("\\title{%s}"  % args.title, file=fout)
print("\\author{%s}" % args.author, file=fout)
print("\\date{%s}"   % args.date, file=fout)
print("", file=fout)
print("\\begin{document}", file=fout)
print("\\maketitle", file=fout)
for fname in texs:
    print("\\input{%s}" % fname, file=fout)
print("\\end{document}", file=fout)
fout.close()


# latexmk
call_cmd("latexmk " + temp_fname)
# remove files
rfiles = []
for ext in ['.aux','.dvi','.fdb_latexmk','.fls','.log','.synctex.gz']:
    rfiles.append(ofname + ext)
call_cmd("rm -v " + " ".join(rfiles))

call_cmd("mv " + ofname + ".pdf " + args.output)
