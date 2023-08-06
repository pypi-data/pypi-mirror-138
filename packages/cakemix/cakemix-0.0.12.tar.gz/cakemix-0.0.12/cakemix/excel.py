import xlrd
from pylab import *

def readExcel(file_name, sheet_name):
    ''' it reads excel files. It uses xlrd.
    
    USAGE: from cakemix.excel import readExcel
    data=readExcel('C:/Users/TLB/Documents/file.xlsx','Sheet2')
    
    Last updated: 8/3/2019
    '''
    workbook=xlrd.open_workbook(file_name)

    sheet1=workbook.sheet_by_name(sheet_name)

    data=[]

    for i in range(sheet1.nrows):
        data.append(sheet1.row_values(i))
    
    return data


def get_column(data,col):
    
    ''' it extracts the specific column from a data. It is used with readExcel function.
    USAGE: 
    from cakemix.excel import get_column
    col1=get_column(data2,5)
    
    '''
    result=[]
    for row in data:
        result.append(row[col])
    return result
	
def col2Num(col):
	'''It converts the Excel column name to number
	USAGE:
	num = col2Num("bz")
	'''
	
	dict={"letter":["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA",'AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ'],"num":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]}
	
	num=dict["num"][dict["letter"].index(col.upper())]
	
	return num


def plotData(data):
    ''' placeholder, dont use yet'''
    yield_data=[]

    process=get_column(data,2)[4:20]

    yield_data=get_column(data,6)[4:20]



    plot(yield_data,'ro-')
    ylim(0.7, 1.1)
    show()
	
	
def plotBarData(data1,data2,ylabel,title):
	# cakemix.plotBarData(['Python','C+',"java","Perl","scala","lisp"],[10,8,6,4,5,1],'Usage','programming language')
	import numpy as np
	import matplotlib .pyplot as plt

	#data1=['Python','C+',"java","Perl","scala","lisp"]

	#data2=[10,8,6,4,2,1]

	plt.bar(data1,data2,alpha=0.5)
	#plt.ylabel('Usage')
	plt.ylabel(ylabel)
	#plt.title('programming language usage')
	plt.title(title)
	plt.show()

def plotLineData(data1,xlabel,ylabel,title):
	# cakemix.plotLineData([1, 2, 4, 8, 16, 32, 64, 128, 256],'model','xlabel','variance')
	from matplotlib import pyplot as plt
	data = [i for i, _ in enumerate(data1)]
	plt.plot(data, data1,     'g-',  label='variance') 
	plt.xlabel(xlabel)
	plt.ylabel(ylabel) 	
	plt.title(title) 
	plt.show()

def plotScatterData(data1,data2,labels,xlabel,ylabel,title):
	# cakemix.plotScatterData([70,65,72, 63, 71, 64, 60, 64, 67],[175,170,205,120,220,130,105,145,190],['a','b','c','d','e','f','g','h','i'],'# of Friends','daily minutes spent on the site','Daily Minutes vs Number of Friends')
	from matplotlib import pyplot as plt

	friends = [70,65,72, 63, 71, 64, 60, 64, 67]
	minutes = [175,170,205,120,220,130,105,145,190]

	labels = ['a','b','c','d','e','f','g','h','i']

	plt.scatter(data1,data2)
	for label, data1_count, data2_count in zip(labels, data1, data2):
		plt.annotate(label,xy=(data1_count,data2_count),xytext = (5,-5),textcoords='offset points')

	plt.title('Daily Minutes vs Number of Friends')
	plt.xlabel('# of Friends')
	plt.ylabel('daily minutes spent on the site')
	
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
	
def plotHistData(data,label,title):
    ''' Placelholder. not yet useful. need to modify '''
    import matplotlib.pyplot as plt
    plt.hist(data,10, histtype='bar', align='mid',color='c',label=label,edgecolor='black')
    plt.legend()
    plt.title(title)
    plt.show()

	