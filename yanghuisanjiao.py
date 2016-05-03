'''
打印出杨辉三角形
'''

a = []  
for i in range(0,10):  
    a.append([])  
    for j in range(0,19):  
        a[i].append(0)  
for i in range(10):
    for j in range(19):
        if (i+j==9 or j-i==9):
            a[i][j]=1
for i in range(1,10):
    for j in range(1,18):
        a[i][j]=a[i-1][j-1]+a[i-1][j+1]         
for i in range(10):
    print a[i]