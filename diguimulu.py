import os  
'''
递归遍历目录
''' 
def getfilelist(filepath, tabnum=1):  
    simplepath = os.path.split(filepath)[1]  
    returnstr = simplepath+"目录<>"+"\n"  
    returndirstr = ""  
    returnfilestr = ""  
    filelist = os.listdir(filepath)  
    for num in range(len(filelist)):  
        filename=filelist[num]  
        if os.path.isdir(filepath+"/"+filename):  
            returndirstr += "\t"*tabnum+getfilelist(filepath+"/"+filename, tabnum+1)  
        else:  
            returnfilestr += "\t"*tabnum+filename+"\n"  
    returnstr += returnfilestr+returndirstr  
    return returnstr+"\t"*tabnum+"</>\n"  
    
    
print(getfilelist('D:\软件'))