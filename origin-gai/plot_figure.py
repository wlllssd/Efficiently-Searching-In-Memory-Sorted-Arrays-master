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

n = 2
if len(sys.argv) > 1:
	n = sys.argv[1]

run_param = ['Run','DatasetSize','Distribution','Parameter','#threads','SearchAlgorithm','RecordSizeBytes']
SearchAlgorithm = ['bs','tip','tip4','tip16','tip64','tip256','tip1024']

df = read_csv("outfile", engine='python', sep = "\s+|\t+|\s+\t+|\t+\s+")

df2 = df.groupby(run_param, sort=False)['TimeNS'].mean()

config = read_csv("experiments.tsv",engine='python', sep = "\t")
DatasetSize = [config['DatasetSize'][len(SearchAlgorithm)*i] for i in range(n)]


res = []
for i in range(n):
	temp = []
	for j in range(len(SearchAlgorithm)):
		temp.append(df2[7*i+j][0])
	res.append(temp)


for i in range(n):
	df_temp = pd.DataFrame(res[i],index=SearchAlgorithm,columns=['TimeNS'])
	print(df_temp.head())
	df_temp.TimeNS.plot(kind='barh',title="DatasetSize:{}".format(DatasetSize[i]))
	name = "Size_{}.png".format(DatasetSize[i])
	fig = plt.gcf()
	fig.savefig(name)
	plt.clf()
	# plt.show()
