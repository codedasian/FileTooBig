#!python3
# File Too Big
# Version : 1.0
# By Codedasian
# Information: This is to be used to split large log files and find a value.

import os
import configparser
import shutil


def findvalue(source):
    found = False
    biline = 0
    bcline = 0

    with open(source, 'r') as log:
        for line in log:
            if batchinstance in line:
                biline += 1
            elif batchclass in line:
                bcline += 1

    print('Found %s occurrences of %s in file' % (bcline, batchclass))
    print('Found %s occurrences of %s in file' % (biline, batchinstance))

    if bcline or biline < 0:
        found = True

    return found


def filesplit(source):

    # Reference Code
    # https://stackoverflow.com/questions/22751000/split-large-text-filearound-50gb-into-multiple-files
    # User: Jyo the Whiff

    numberoflines = int(config['LINES']['numberof'])
    linecount = 0
    filecount = 1

    filereader = open(source, 'r')

    try:
        line = filereader.readline()
        filename = files[f].replace('.log', ('_' + str('%03d' % filecount))) + '.txt'
        filewriter = open('split/%s' % filename, 'a')

        while line != '':
            if linecount == 0:
                filename = files[f].replace('.log', ('_' + str('%03d' % filecount))) + '.txt'
                filewriter = open('split/%s' % filename, 'a')
                filecount += 1
            filewriter.write(line)
            linecount += 1
            if linecount == numberoflines:
                linecount = 0
                filewriter.close()
            line = filereader.readline()
        filewriter.close()

    except Exception as e:
        print(e)
    finally:
        filereader.close()


def foundfiles(source):
    for path, sub, files in os.walk(source):
        for f in range(len(files)):
            textfile = logfile = '%s/%s' % (path, files[f])
            if textfile.endswith('.txt'):
                with open(textfile) as txt:
                    for line in txt:
                        if batchinstance in line:
                            print(textfile)
                            txt.close()
                            shutil.move(textfile, 'found')
                            print('Found %s in %s file.' % (batchinstance, textfile))
                            break
                        if batchclass in line:
                            txt.close()
                            shutil.move(textfile, 'found')
                            print('Found %s in %s file.' % (batchclass, textfile))
                            break


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    os.makedirs('found', exist_ok=True)
    os.makedirs('input', exist_ok=True)
    os.makedirs('split', exist_ok=True)
    os.makedirs('processed',exist_ok=True)

    inputpath = 'input'
    batchinstance = config['BATCH']['instance']
    batchclass = config['BATCH']['class']


    for path, sub, files in os.walk(inputpath):
        for f in range(len(files)):
            logfile = '%s/%s' % (path, files[f])

            if findvalue(logfile):
                filesplit(logfile)
                print('')
                foundfiles('split')

            shutil.move(logfile,'processed')

    # print('')
    # input('Files Ready To Be Use With Notepad or Notepad++.')