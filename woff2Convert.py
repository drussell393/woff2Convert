#!/usr/bin/env python
# Simple command-line conversion for woff2 to TTF using Google's woff2
# Author: Dave Russell (drussell393)

import os
import sys
import getopt
import yaml
import urllib2

def main(argv):
    with open('config.yaml', 'r') as config:
        config = yaml.load(config)

    fontFamily = config['defaultFamily']
    outputDir = config['defaultOutputDir']
    charset = config['defaultCharset']

    # Get our arguments (we should be passing this a family name and an optional outfile name)
    try:
        opts, args = getopt.getopt(argv, "hf:o:c:", ["help", "family=", "outdir=", "charset="])
    except getopt.GetoptError:
        print('usage: woff2Convert.py [--help] [--outdir="/path/to/outputDirectory"] [--family="Noticia Text"] [--charset="latin"]')
        sys.exit(2)

    for opt, arg in opts:
        if (opt in ('-h', '--help')):
            print('usage: woff2Convert.py [--help] [--outdir="/path/to/outputDirectory"] [--family="Noticia Text"] [--charset="latin"]')
            sys.exit()
        elif (opt in ('-f', '--family')):
            fontFamily = arg
        elif (opt in ('-o', '--outdir')):
            outputDir = arg
        elif (opt in ('-c', '--charset')):
            charset = arg

    if (fontFamily is not None):
        if (outputDir is not None):
            woff2url = getWoffFile(fontFamily, charset)
            modifiedFamily = fontFamily.replace(' ', '-') + '_' + charset
            woffFile = modifiedFamily + '-' + charset + '.woff2'
            os.system('wget ' + woff2url + ' -O ' + woffFile)
            os.system(config['woff2Path'] + '/woff2_decompress ' + woffFile)
            if (os.path.isdir(outputDir) == False):
                os.system('mkdir ' + outputDir)
            os.system('mv ' + modifiedFamily + '.ttf ' + outputDir)
            if (config['keepFile'] == False):
                os.system('rm -f ' + woffFile)
        else:
            print('Please specify a default output directory in config.yaml or by passing the "-o" option through the command.')
            sys.exit(2)
    else:
        print('Please specify a family either in the command by using the "-f" option, or in the config.yaml file')
        sys.exit(2)

def getWoffFile(fontFamily, charset):
    url = "https://fonts.googleapis.com/css?family=" + fontFamily.replace(' ', '+')
    request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 7520.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.110 Safari/537.36'})
    try:
        connection = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if (e.code == 404) or (e.code == 400):
            print('This font family doesn\'t exist on Google Fonts.')
            sys.exit(2)
        else:
            print('There was an issue obtaining the Google Font. The web server replied with response code: ' + str(e.code))
            sys.exit(2)
    content = connection.read()

    # Get our file to download
    try:
        fontFaceBlock = content.split('/* ' + charset + ' */')[1]
    except IndexError:
        print('That character set  doesn\'t exist in this family, bud. Try again.')
        sys.exit(2)

    woff2url = fontFaceBlock.split('url(')[1].split(')')[0]
    return woff2url

if __name__ == "__main__":
    main(sys.argv[1:])
