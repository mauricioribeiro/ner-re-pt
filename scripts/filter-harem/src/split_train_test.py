from lxml import etree
import sys
from random import shuffle
#129 documents
#90 train
#39 test

if(len(sys.argv) > 1):
  harem_filename = sys.argv[1]
  output_name = sys.argv[2]
else:
  print "Usage: python " + sys.argv[0] + " <input file> <output file>"
  sys.exit()

tree = etree.parse(harem_filename)

dataset = tree.xpath("//DOC")
shuffle(dataset)

# split into 10 folds
n_folds = int(len(dataset)/9)
folds = [dataset[i:i + 10] for i in xrange(0, len(dataset), n_folds)]

for i in range(len(folds)):
	out_tree_str = "<?xml version='1.0' encoding='ISO-8859-1'?>\n"
	out_tree_str += "<!DOCTYPE colHAREM>\n"
	out_tree_str += "<colHAREM versao=\"Segundo_dourada_com_relacoes_14Abril2010\">\n"
	out_tree_str += "</colHAREM>"

	out_tree_train = etree.fromstring(out_tree_str)
	out_tree_test = etree.fromstring(out_tree_str)

	train = folds[:i] + folds[i+1:]
	train = [item for sublist in train for item in sublist]
	test = folds[i]

	for el in train:
		out_tree_train.append(el)

	for el in test:
		out_tree_test.append(el)

	# output to file
	f = open("../outputs/fold-"+str(i)+"/"+output_name+"_train.xml",'w')
	f.write(etree.tostring(out_tree_train, encoding="ISO-8859-1"))
	f.close()

	# output to file
	f = open("../outputs/fold-"+str(i)+"/"+output_name+"_test.xml",'w')
	f.write(etree.tostring(out_tree_test, encoding="ISO-8859-1"))
	f.close()