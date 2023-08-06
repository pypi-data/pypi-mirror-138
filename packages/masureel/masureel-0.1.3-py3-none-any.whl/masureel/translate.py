import csv
import codecs

def translate_file(filename):
  Dict = []
  with open('data/Dict.csv') as f:
      aList = csv.reader(f, delimiter='|')
      for row in aList:
        Dict.append(row)

  with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as fdata:
    filedata = fdata.read()

  for i in range(len(Dict)):
    filedata = filedata.replace(Dict[i][0], Dict[i][1])

  with open(f'translated_{filename}', 'w', encoding='utf-8') as file:
    file.write(filedata)