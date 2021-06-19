from random import Random

str = ''
chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
length = len(chars) - 1
random = Random()

#生成16字的英數亂碼
for i in range(16):
    str+=chars[random.randint(0,length)]
print(str)


'''
import random, string

def GenPassword(length):
    #隨機出數字的個數
    numOfNum = random.randint(1,length-1)
    numOfLetter = length - numOfNum
    #選中numOfNum個數字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    #選中numOfLetter個字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    #打亂這個組合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    #生成密碼
    genPwd = ''.join([i for i in slcChar])
    return genPwd

    if __name__ == '__main__':
        print GenPassword(6) 

'''