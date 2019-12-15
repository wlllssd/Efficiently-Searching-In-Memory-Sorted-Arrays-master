#!/usr/bin/env python

from os import path
from os import popen
from subprocess import call
from pandas import read_csv, set_option
import pandas as pd
import sys
import subprocess
from subprocess import DEVNULL
import matplotlib.pyplot as plt

n = 1
tsv = 'experiments.tsv'
if len(sys.argv) > 1:
	tsv = sys.argv[1]

run_param = ['Run','DatasetSize','Distribution','Parameter','#threads','SearchAlgorithm','RecordSizeBytes']
# SearchAlgorithm = ['bs','tip','tip4','tip16','tip64','tip256','tip1024']
SearchAlgorithm = ['tip2', 'tip4', 'tip8', 'tip16','tip32', 'tip64','tip128', 
					'tip256', 'tip1024', 'tip2048', 'tip4096', 'tip8192', 'tip16384']

df = read_csv("outfile", engine='python', sep = "\s+|\t+|\s+\t+|\t+\s+")

df2 = df.groupby(run_param, sort=False)['TimeNS'].mean()

config = read_csv(tsv,engine='python', sep = "\t")
DatasetSize = [config['DatasetSize'][len(SearchAlgorithm)*i] for i in range(n)]


res = []
for i in range(n):
	temp = []
	for j in range(len(SearchAlgorithm)):
		temp.append(df2[len(SearchAlgorithm)*i+j][0])
	res.append(temp)


for i in range(n):
	df_temp = pd.DataFrame(res[i],index=SearchAlgorithm,columns=['TimeNS'])
	
	df_temp.TimeNS.plot(kind='barh',title="DatasetSize:{}".format(DatasetSize[i]))
	name = "output/Size_{}".format(DatasetSize[i])
	name2 = name + "_info.csv"
	name = name + ".png"
	fig = plt.gcf()
	fig.savefig(name)
	plt.clf()
	# plt.show()
	
	df_temp.to_csv(name2,sep = '	',float_format='%.0f')
	print(df_temp)