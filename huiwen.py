#b5判断字符串是否为回文句
list1='saas adads  s aas'
new_list=[]
for l in list1:
    if l==' ':pass
    else: new_list.append(l)
print(new_list)
n=len(new_list)
if len(new_list)%2==0:
    n2=n/2
    for i in range(int(n2)):
        if new_list[i]!=new_list[-(i+1)]:        
            print('ou not huiwen')
            break
        else: n2=n2-1
    if n2==0:
        print('ou huiwen')
    
if len(new_list)%2==1:
    n2=(n+1)/2
    for i in range(int(n2)):
        if new_list[i]!=new_list[-(i+1)]:        
            print('ji not huiwen')
            break
        else: n2=n2-1
    if n2==0:
        print('ji huiwen')