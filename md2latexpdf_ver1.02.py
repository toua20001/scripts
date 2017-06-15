#!/usr/bin/env python3
import os, sys
import argparse
import subprocess
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ifname', type=str, nargs='*') # ifnameは何個でも良い
    parser.add_argument('--output', type=str, default='output.pdf')
    parser.add_argument('--clean', action='store_true', default=False)
    parser.add_argument('--title', type=str, default='')
    parser.add_argument('--author', type=str, default='')
    parser.add_argument('--date', type=str, default='\\today')
    args = parser.parse_args()
    return args

def call_cmd(cmd):
    print("$", cmd)
    proc = subprocess.call(cmd, shell=True)
    if not proc == 0: # error
        sys.exit("# Cancel Document creation ...")

def md2tex(fnames):
    texs = []
    for fname in fnames:
        tex = os.path.splitext(fname)[0] + ".tex"
        cmd = "pandoc %s -o %s" % (fname, tex)
        call_cmd(cmd)
        texs.append( tex )
    return texs

def ajust_img(fname):
    f = open(fname, 'r+') # 読み書きモードでopen
    lines = []
    for line in f.readlines():
        line = line.rstrip()
        if 'includegraphics' in line: #画像を指定している部分
            imgf = line.split('{')[1][:-1]
            size = Image.open(imgf).size[0]
            opt = '[width=\\hsize]' if size>430 else ''
            line = '\\includegraphics%s{%s}' % (opt, imgf)
        if 'begin{figure}' in line:
            line = '\\begin{figure}[htb]'
        if 'tightlist' in line:
            continue
        lines.append(line + '\n')
    lines.append('\n\n\n')

    f.seek(0)
    for line in lines:
        f.write(line)
    f.close()

def create_temp(texs, args):
    opt = []
    opt.append( "\\documentclass[11pt, a4j, uplatex]{jsarticle}" )
    opt.append( "\\usepackage[dvipdfmx]{graphicx}" ) # 画像
    opt.append( "\\usepackage{amsmath}" )
    opt.append( "\\usepackage{amssymb}" )
    opt.append( "\\usepackage{amsfonts}" )
    opt.append( "\\usepackage{longtable}" )
    opt.append( "\\usepackage{booktabs}" )
    opt.append( "" )
    opt.append( "\\title{%s}" % args.title )
    opt.append( "\\author{%s}" % args.author )
    opt.append( "\\date{%s}" % args.date )
    opt.append( "" )
    opt.append( "\\begin{document}" )
    opt.append( "\\maketitle" )
    for tex in texs:
        opt.append( "\\input{%s}" % tex )
    opt.append( "\\end{document}" )

    # 書き出し　
    fout = open('temp.tex', 'w')
    for p in opt:
        print(p, file=fout)
    fout.close()

def main():
    args = get_args()
    texs = md2tex(args.ifname)
    for tex in texs:
        ajust_img(tex)
    create_temp(texs, args)

    call_cmd("latexmk " + 'temp.tex')
    rm = []
    for ext in ('.aux', '.dvi', '.fdb_latexmk', '.fls', '.log', '.synctex.gz'):
        rm.append('temp' + ext)
    if args.clean:
        rm.extend(texs)
        rm.append('temp.tex')
    call_cmd('rm -v ' + ' '.join(rm))
    call_cmd('mv temp.pdf ' + args.output)

if __name__ == '__main__':
    main()
