#! /usr/bin/env python

#
#    x2c - XML to CSV Conversion
#    Copyright (C) 2022  Martin Valter
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import xml.etree.ElementTree as et
import pandas as pd
import sys, argparse

class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))

def convert():
    args = sys.argv[1:]

    inputfile = ''
    outputfile = ''
    cols = []
    rows = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile')
    parser.add_argument('-i', '--infile')
    parser.add_argument('-c', '--columns', action=SplitArgs)    
    args = parser.parse_args()

    cols = args.columns
    outfile = args.outfile
    infile = args.infile

    xmlparse = et.parse(infile)
    root = xmlparse.getroot()

    for element in root:
        tmp_d = {}
        for c in cols:
            try:
                tmp_v = element.find(str(c)).text
                tmp_d[c] = tmp_v
            except:
                print('No such tag as %s.' % c)
                print('Please make sure the supplied column names match the XML tags.')
                exit(1)
        rows.append(tmp_d)
    
    f = pd.DataFrame(rows, columns=cols)    
    f.to_csv(outfile)