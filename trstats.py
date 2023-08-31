import sys
import subprocess
import time
import ipaddress
from statistics import mean,median
import matplotlib.pyplot as plt

#running tracecommand+++++++++++++++++++++++++++++++++++++++++++++++++++
def runTraceRouteOnce(command):
	command1=command
	proc=subprocess.Popen(command1,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	o,e=proc.communicate()
	traceoutput=o.decode('ascii')
	# print(traceoutput)
	combinedtraceoutput=[]
	temp=""
	for i in range(0,len(traceoutput)):
   	 
    	if traceoutput[i]=="\n":
        	combinedtraceoutput.append(temp)
        	temp=""
    	else:
        	temp=temp+traceoutput[i]
	combinedtraceoutput=combinedtraceoutput[1:]
	return combinedtraceoutput
    
def runTraceRoute(numofruns,rundelay,maxhops,target):
	command=["traceroute","-m",str(maxhops),"-I",target]
	finaloutput=[]
	for i in range(0,numofruns):
    	finaloutput.append(runTraceRouteOnce(command))
    	time.sleep(rundelay)
	return finaloutput
#running tracecommand+++++++++++++++++++++++++++++++++++++++++++++++++++




#helpers function============================================================
def printarr(arr):
	for i in range(0,len(arr)):
    	print(arr[i])
    	print()
def removeWhiteSpace(inputdata):
	output=[]
	for i in range(0,len(inputdata)):
    	output.append([])
    	for j in range(0,len(inputdata[i])):
        	output[i].append(inputdata[i][j].split())
	return output
def removeMilliSeconds(inputdata):
	output=[]
	for i in range(0,len(inputdata)):
    	output.append([])
    	for j in range(0,len(inputdata[i])):
        	output[i].append([m for l,m in enumerate(inputdata[i][j]) if m!='ms'])
	return output
def interChangeListAccordingToHopNumber(inputdata):
	output=[]
	m=len(inputdata)
	n=len(inputdata[0])
	for i in range(0,n):
    	output.append([])
    	for j in range(0,m):
        	output[i].append(inputdata[j][i])    
	return output
def containsStar(inputlist):
	for i in range(0,len(inputlist)):
    	if inputlist[i]=="*":
        	return True
	return False
def removeStars(inputdata):
	output=[]
	for i in range(0,len(inputdata)):
    	output.append([])
    	for j in range(0,len(inputdata[i])):
        	if not containsStar(inputdata[i][j]):
            	output[i].append(inputdata[i][j])
	return output
def createDictData(inputdata):
	output=[]
	for i in range(0,len(inputdata)):
    	temp={}
    	temp['hop']=i+1
    	temp['hosts']=[]
    	temp['latency']=[]
    	for j in range(0,len(inputdata[i])):
        	for k in range(1,len(inputdata[i][j])):
            	try:
                	if '(' in inputdata[i][j][k]:
                    	ipaddress.ip_address(inputdata[i][j][k].replace('(','').replace(')',''))  	 
                    	temp['hosts'].append([inputdata[i][j].pop(k-1),inputdata[i][j].pop(k-1)])
               	 
            	except:
                	pass    
    	output.append(temp)
	for i in range(0,len(inputdata)):
    	for j in range(0,len(inputdata[i])):
        	for k in range(1,len(inputdata[i][j])):
            	output[i]['latency'].append(float(inputdata[i][j][k]))
	return output
#helpers function=============================================================

def cleanTheData(inputdata):
	finaloutput=[]
	output1=removeWhiteSpace(inputdata)#removes spaces from string and converts data to list
	# print(output1)
	output2=removeMilliSeconds(output1)#removes millisecond string from all lists
	# printarr(output2)
	output3=interChangeListAccordingToHopNumber(output2)#changes data from each run of traceroute to hop format
	# printarr(output3)
	output4=removeStars(output3)#removes star output hops from data
	# printarr(output4)
	output5=createDictData(output4)#change data from list format to dictionary format  along with that serialize the data
	# printarr(output5)
	return output5
def calculateMinMaxAverageMedian(inputdata):
	output=[]
	for i in range(0,len(inputdata)):
    	temp={}
    	temp['hop']=inputdata[i]['hop']
    	temp['hosts']=inputdata[i]['hosts'].copy()
    	if len(inputdata[i]['latency'])>1:
        	temp['min']=min(inputdata[i]['latency'])
        	temp['max']=max(inputdata[i]['latency'])
        	temp['avg']=mean(inputdata[i]['latency'])
        	temp['med']=median(inputdata[i]['latency'])
    	else:
        	temp['min']=0
        	temp['max']=0
        	temp['avg']=0
        	temp['med']=0
    	output.append(temp)
	return output
def boxPlotFormatData(inputdata):
	labels=[]
	boxplotdata=[]
	for i in range(0,len(inputdata)):
    	labels.append('hop '+str(inputdata[i]['hop']))
    	boxplotdata.append(inputdata[i]['latency'])
	return boxplotdata,labels
def processDataTopythonDict(inputdata):
	output1=cleanTheData(inputdata)
	printarr(output1)
	output2=calculateMinMaxAverageMedian(output1)
	printarr(output2)
   
	return output1,output2

def plotTheDataToPdf(inputdata,pdfname):
	BoxPlotData,Labels=boxPlotFormatData(inputdata)
	plt.xticks(rotation=90)
	listofcolors=["#ACB2FC","#F7A99C","#7FE5CA","#D5B0FC","#FFD0AC","#8BE9F9","#FFB2C8","#DAF3BF","#FFCBFF","#FEE5A8"]
	bp=plt.boxplot(BoxPlotData,patch_artist=True,labels=Labels)
	for i in range(0,len(BoxPlotData)):
    	bp['boxes'][i].set_color(listofcolors[i%len(listofcolors)])
	plt.savefig(pdfname,format="pdf",bbox_inches="tight")    
    

def main():
	print("the arguments passsed:=",sys.argv)
	print("running")
	output="/home/vishal/Desktop/temp.json"
	graph="/home/vishal/Desktop/graph.pdf"
	tracerouteoutput=runTraceRoute(numofruns=10,rundelay=1,maxhops=20,target="www.google.com")
	plotdata,dictdata=processDataTopythonDict(tracerouteoutput)#convert data to python dict so as to easily convert to json
	plotTheDataToPdf(plotdata,pdfname="myfirstpdf.pdf")
    

main()


