#!/usr/bin/python3

def func():
    count = 0
    while count < 5:
        print (count, " is  less than 5")
        count = count + 1
        try:
            break
        except Exception as e:
            print ('nei',e)
    else:
        print (count, " is not less than 5")
        return
       
    try:
        1/0      
    except Exception as e:
        print ('wai',e)
       
       
func()