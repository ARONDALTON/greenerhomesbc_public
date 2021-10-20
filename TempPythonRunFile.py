# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# Hi Mike, this is a markdown cell
# 
# you need to install the Jupyter from microsoft extension in Visual Studio Code (easiest) from the left panel - plugins  
# 

# %%
1+2+3+4


# %%
# TODO: import needed modules

from lxml import etree
import math as m
import numpy as np
import pandas as pd
import attr
import collections 
import pathlib as pl
import re
from datetime import datetime
# for colored text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# %% [markdown]
# File Directories can be easily copied with the following procedure:
# 1) open windows files manager and go to directory
# 2) on the directory press and hold the shift key and left click the mouse and select - "Copy as path"
# 3) key press "control v" below

# %%
# TODO: input QC dir
inputDir=input("Input Dir Path to Be Checked")
inputDir=pl.Path(inputDir)
# print(inputDir)
inputDir


# %%
import pytz
tz = pytz.timezone('US/PACIFIC')
ts=inputDir.stat().st_atime

ts=datetime.fromtimestamp(ts)#.strftime('%Y-%m-%d %H:%M:%S')
ts=ts.astimezone(tz)
# datetime.astimezone()
inputDir.exists(),ts.strftime('%Y-%m-%d %H:%M:%S'),inputDir.stat().st_size


# %%
# TODO: check dir for h2k files
def get_files(extensions):
    all_files = {}
    for ext in extensions:
        
        all_files[ext]=[{"fileName":f.name,'file':f} for f in (inputDir.glob(ext))]
        # all_files.extend(pl.Path('.').glob(ext))
    return all_files

files = get_files(('*.h2k', '*.jpg', '*.pdf'))

# files



# TODO: warn of extra h2k files
check=len (files['*.h2k'])
print(f"H2K files:")
[print(f"      {i['fileName']}") for i in files['*.h2k']]
if check>1:
    print (f" {bcolors.WARNING}****************** Error number of h2k files: {check} *****************************{bcolors.ENDC}")

# TODO: warn of missing required photos
check=len (files['*.jpg'])
print(f"jpg files:")
[print(f"      {i['fileName']}") for i in files['*.jpg']]
minimum=15
if check<minimum:
    print (f" {bcolors.WARNING}****************** Error number of jpg files: {check}, the min is {minimum} *****************************{bcolors.ENDC}")

# TODO: warn of missing ERS output files
check=len (files['*.pdf'])
print(f"PDF files:")
[print(f"      {i['fileName']}") for i in files['*.pdf']]
if check!=4:
    print (f" {bcolors.WARNING}****************** Error number of pdf files: {check} *****************************{bcolors.ENDC}")

# TODO: check files in  directory names for extra spaces and for capitals an jpg extentions...



# %%



# %%
# TODO: read h2k xml file
# https://lxml.de/tutorial.html
from lxml import etree
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

# https://stackoverflow.com/questions/42896807/how-to-parse-xml-from-local-file-or-url-with-lxml
# https://lxml.de/parsing.html
if inputDir.is_file():
  tree = etree.parse(str(inputDir))
else:
  tree = etree.parse(str(files['*.h2k'][0]['file']))

tree


# %%



# %%
p=r"/".join([r'./','Codes','Window','Standard','Code'])
# p=r"/".join([r'./','Codes','Window','Standard'])

p=".//ProgramInformation"
print (p)
t=tree.xpath(p)
t=t[0]
tl=t.getchildren()
# [ (i.attrib,j.attrib, z.tag,z.attrib, y.text)  for i in tl for j in i.getchildren() for z in j.getchildren() for y in z.getchildren()]
# [(i.getparent().getparent().tag,i.getparent().tag,i.getparent().getparent().tag) for i in tree.xpath(p)]
# [(i.getparent().tag,i.attrib, i.tag, i.text) for i in tree.xpath(p)]
l=[i.tag for  j in tl for i in list(j.getiterator())]

weather=p+"/".join(['/Weather', 'Region','English'])
fileInfo=p+"/".join(['/File'])
weather=tree.xpath(p+"/".join(['/Weather', 'Region','English']))[0].text,tree.xpath(p+"/".join(['/Weather', 'Location','English']))[0].text
print(f"Weather Info:{weather}")
fileInfo=tree.xpath(p+"/".join(['/File']))[0].attrib,tree.xpath(p+"/".join(['/File', 'Identification']))[0].text
print(f"File Info:{fileInfo}")
tags=[i.tag for i in tree.xpath(p+"/".join(['/File']))[0]]
tree.xpath(p+'/File')
# [j for i in tree.xpath(p+'/File/'+tags[0]) for j in i]


# TODO: display basic File data


for f in tree.xpath(p+'/File'): 
  # for j in i]
  print (f"Program Info :")
  for t in f:
    if t.tag=='Ownership':
      print(f"   {t.tag}: {t.find('English').text}")
    else:
      print(f"   {t.tag}: {t.text}")


# TODO: display basic customer data

for f in tree.xpath(p+'/Client'): 
  print (f"Client Info :")
  for t in f:
    print(f"   {t.tag}: {t.text}")
    if t.tag=='Name':
      # print("Name")
      [print(f"    {i.tag}: {i.text} ") for i in t.getchildren()]
      # print(f"   {t.tag}: First :{t.find('First').text}, Last : {t.find('Last').text} ")
    if t.tag=='Telephone':
      # ensure 9 numbers
      if len(re.findall('[0-9]',t.text) )!= 10:
        print(f"   {bcolors.WARNING}****************** Phone number is incorrect:  *****************************{bcolors.ENDC}")
      # print(f"   {t.tag}: {t.text}")
    
    if t.tag=='StreetAddress':
      # print(f"   {t.tag}: First :{t.find('First').text}, Last : {t.find('Last').text} ")
      print("Street Address")
      [print(f"    {i.tag}: {i.text} ") for i in t.getchildren()]
    if t.tag=='MailingAddress':
      # print(f"   {t.tag}: First :{t.find('First').text}, Last : {t.find('Last').text} ")
      print("Mailing Address")
      [print(f"    {i.tag}: {i.text} ") for i in t.getchildren()]
    
      


# client=p+"/".join(['/File', 'Region','English'])
# [i.text for i in tree.xpath('.//Weather') for j in i.]
# subTags=[i.tag for i in tree.xpath(p)[0]]
# tree.xpath(p+'/'+subTags[0])
#  [i.tag for i in tree.xpath(p+subTags)[0][0]]

# [i for i in subTags]
# l


# %%




# %%
# TODO: check total ceiling area vs total floor/foundation areas

# TODO: check total wall perimeters to total header perimeters
 


# %%



# %%
# TODO: check all reqired files are uploaded


# %%



