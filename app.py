
import os
import argparse
import re 
from PIL import Image, features


# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--path", "-p", help="Resimleri içeren klasör", required=True)
parser.add_argument("--filter", "-f", help="Klasördeki resimler uygulanacak olan filteri(reqex) ifade eder", default="*")
parser.add_argument("--quality", "-q", help="Kalite 0-100 arasında değer alıyor", default=90)
parser.add_argument("--max_x", "-x", help="Resim Maksimum genişlik büyükse tekrar boyutlandırılır.", default=0)
 

# Read arguments from the command line
args = parser.parse_args()

def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))

if __name__ == "__main__":
  info_list = []
  for infile in os.listdir(args.path):
    f, e = os.path.splitext(infile)
    
    if e.lower() != ".webp" and (args.filter == "*" or re.search(args.filter,infile)):    
      try:
          infile_path = os.path.join(args.path, infile)
          outfile_path = os.path.join(args.path, f +".webp")  
          with Image.open(infile_path) as im:        
              
              if args.max_x != 0 and  im.size[0] > args.max_x:
                im.thumbnail(args.max_x) 
              
              im.save(outfile_path, format = "webp", minimize_size=True, method=6, quality= args.quality)
                        
              info_list.append({
                'image' : infile,
                'old_size' : f"{round(os.path.getsize(infile_path) / 1024, 1)} kB",
                'new_size' : f"{round(os.path.getsize(outfile_path) / 1024, 1)} kB",  
                'px' : f"{im.size}"
              })
      except OSError as e:
          print("cannot convert", infile, str(e))

  printTable(info_list, ['image','old_size','new_size','px'])
