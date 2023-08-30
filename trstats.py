import sys
import subprocess
import time

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

#helpers function=============================================================

def cleanTheData(inputdata):
    finaloutput=[]
    output1=removeWhiteSpace(inputdata)#removes spaces from string and converts data to list
    output2=removeMilliSeconds(output1)#removes millisecond string from all lists
    # print(output2)
    output3=interChangeListAccordingToHopNumber(output2)#changes data from each run of traceroute to hop format
    # print(output3)
    output4=removeStars(output3)#removes star output hops from data 
    for i in range(0,len(output4)):
        print(output4[i])
        print()

def processDataToJson(inputdata):
    cleanTheData(inputdata)
    

def main():
    print("the arguments passsed:=",sys.argv)
    print("running")
    output="/home/vishal/Desktop/temp.json"
    graph="/home/vishal/Desktop/graph.pdf"
    tracerouteoutput=runTraceRoute(numofruns=5,rundelay=0,maxhops=5,target="www.google.com")
    processDataToJson(tracerouteoutput)
    

main()

