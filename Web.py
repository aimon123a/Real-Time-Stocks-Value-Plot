'''
Created on Feb 26, 2018

@author: HP User
'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

from lxml import html
import requests
import time
import sys
import multiprocessing
import matplotlib
import PyQt5
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
'''plt.switch_backend('agg')'''
import matplotlib.animation as animation
from matplotlib import style
xsappl = []
ysappl = []
xsMS = []
ysMS = []
xsGoog = []
ysGoog = []
xsAmaz =[]
ysAmaz = []

t_end = time.time() + 60 * 30

company = ['apple', 'mircosoft', 'google', 'amazon']
realTimeMaxMin = []
index = 0

'''style.use('fivethirtyeight')
fig = plt.figure()
axl = fig.add_subplot(1,1,1)'''


def main(argv):
    urlfront = 'https://www.nasdaq.com/symbol/'
    
    if argv not in company:
        print('argv error')
        return
    if argv == 'apple':
        urlargs = 'aapl'
    if argv == 'mircosoft':
        urlargs = 'msft'
    if argv == 'google':
        urlargs = 'goog'
    if argv == 'amazon':
        urlargs = 'amzn'
    print(argv)
    urlback = '/historical'
    url = urlfront + urlargs + urlback
    page = requests.get(url)
    tree = html.fromstring(page.content)

    stats = tree.xpath('//td/text()')

    i = 0
    j = i+6
    arr = []
    stats = [x.replace("\r\n ,","").strip() for x in stats]

    for x in stats:
        if x:
            if ',' in x:
                x = x.replace(',','')
            arr.append(x)
        
    while j <= len(arr):
        arr[i:j] = [','.join(arr[i:j])]
        i = i + 1
        j = j + 1
    
    for x in arr:
        print(x)
    csvf = argv + '.csv'
    properties = 'Date, Open, High,Low, Close, Volumn'
    with open(csvf,'w')as file2:
        file2.write(argv)
        file2.write('\n')
        file2.write(properties)
        file2.write('\n')
        for line in arr:
            file2.write(line)
            file2.write('\n')



def currentStockValue(url, company):
    global index
    currentValue = 0
    indexCompany = index
    growth = 'increased '
    initialValue = 0
    fiveChanges = 0
    started = 0
    x = 1
    
    if company == "Apple":
        comColor = bcolors.HEADER
        xs = xsappl
        ys = ysappl
    elif company == "Google":
        comColor = bcolors.OKGREEN
        xs = xsGoog
        ys = ysGoog
    elif company == "Mircosoft":
        comColor = bcolors.OKBLUE
        xs = xsMS
        ys = ysMS
    else:
        comColor = bcolors.WARNING
        xs = xsAmaz
        ys = ysAmaz
    while time.time () < t_end:
        
        time.sleep(1.5)
        page1 = requests.get(url)
        tree1 = html.fromstring(page1.content)
        stats1 = tree1.xpath('//div[@class = "qwidget-dollar"]/text()')
        if(started == 0):
            currentValue = float(stats1[0].replace("$","")) 
            print(comColor,company,bcolors.ENDC, 'current value: ',stats1)
            xs.append(x)
            x += 1
            ys.append(currentValue)
        diff = float(stats1[0].replace("$","")) - currentValue 
        started += 1
        
        if currentValue != float(stats1[0].replace("$","")):   
            currentValue = float(stats1[0].replace("$","")) 
            if diff > 0:
                #print("\n")
                xs.append(x)
                x+=1
                ys.append(currentValue)      
                print(comColor,company,bcolors.ENDC, 'current value: ',stats1, bcolors.OKGREEN + 
                      " +", "%.3f" % round(diff,2), bcolors.ENDC)  
            elif diff < 0:
                #print("\n")
                xs.append(x)
                x+=1
                ys.append(currentValue) 
                print(comColor,company,bcolors.ENDC, 'current value: ',stats1, bcolors.RED,
                       "%.3f" % round(diff,2), bcolors.ENDC)
            fiveChanges += 1
            if initialValue == 0:
                initialValue = float(stats1[0].replace("$",""))
        if x%5 == 0:
            animate(xs, ys, company)
            plt.ion()
            plt.show()
        if fiveChanges == 5:
            changes = currentValue - initialValue
            if(changes >0.0):
                print(comColor,company,bcolors.ENDC,  'over the last 5 changes it has', 
                      bcolors.OKGREEN + growth," +", "%.3f" % round(changes,2),bcolors.ENDC,' dollars')
            elif(changes < 0.0):
                growth = 'decreased '
                print(comColor,company,bcolors.ENDC,  'over the last 5 chages it has', 
                      bcolors.RED + growth, "%.3f" % round(changes,2) ,bcolors.ENDC, 'dollars')
                growth = 'increased '
            else: 
                print(comColor,company,bcolors.ENDC,  'has significantly small on price change over the 5 in/decrease in price')
            fiveChanges  = 0
            initialValue = currentValue
            
            
    
            
            
if len(sys.argv) > 1:
    if sys.argv[1] == 'current':
        if __name__ == '__main__':
            
            if len(sys.argv) == 2:
                p = multiprocessing.Process(name='p', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/goog/historical', 'Google',))
                p1 = multiprocessing.Process(name='p1', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/aapl/historical', 'Apple',))
                p2 = multiprocessing.Process(name='p2', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/msft/historical', 'Mircosoft',))
                p3 = multiprocessing.Process(name='p3', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/amzn/historical', 'Amazon',))
                p.start()
                p1.start()
                p2.start()
                p3.start()
            else:
                iterator = iter(sys.argv)
                next(iterator)
                next(iterator)
                for x in iterator:
                    if x not in company:
                        print('argv error')
                        break
                    if x == 'apple':
                        p1 = multiprocessing.Process(name='p1', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/aapl/historical', 'Apple',))
                        p1.start()
                    if x == 'mircosoft':
                        p2 = multiprocessing.Process(name='p2', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/msft/historical', 'Mircosoft',))
                        p2.start()
                    if x == 'google':
                        p = multiprocessing.Process(name='p', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/goog/historical', 'Google',))
                        p.start()
                    if x == 'amazon':
                        p3 = multiprocessing.Process(name='p3', target=currentStockValue, args = ('https://www.nasdaq.com/symbol/amzn/historical', 'Amazon',))
                        p3.start()
        
        


if len(sys.argv) > 1:
    if(sys.argv[1] == 'data'):
        if len(sys.argv) == 1:
            for x in company:
                main(x)
        else :
            iterator = iter(sys.argv)
            next(iterator)
            next(iterator)
            for x in iterator:
                main(x) 


def animate(x,y,company):   
    xs=x
    ys=y
    plt.plot(xs,ys)
    plt.ylabel('stock value')
    plt.xlabel('time')
    plt.title(company)
    plt.pause(1)
    
'''ani = animation.FuncAnimation(fig, animate, interval=1000)'''




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    