# import required files and modules
from urllib import response
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re

def comp(deva):
#generating url
  def generate_url(part1,part2,search_for,ch):
    url=part1
    list1=list(search_for)
    #print(list1)
    l=len(list1)
    for i in range(0,l):
      if list1[i]==' ':
        list1[i]=ch
      url=url+list1[i]
    url=url+part2
    return url

  search_for=deva
  #amazon_url=generate_url('https://www.amazon.in/s?k=','&ref=nb_sb_noss_1',search_for,'+')
  spd_url=generate_url('https://www.snapdeal.com/search?keyword=','&sort=rlvncy',search_for,'%20')
  fl_url=generate_url('https://www.flipkart.com/search?q=','&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off',search_for,'%20')

  headers = {
      "Host": "www.snapdeal.com",
      "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate, br",
      "Connection": "keep-alive",
  }
  headers1 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
  headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
  r1 = requests.get(spd_url, headers=headers1)
  r2=requests.get(fl_url,headers=headers2)
  content2=r2.content
  content = r1.content
  #print("spd stat: ",r1.status_code)
  #print("flipkart stat: ",r2.status_code)
  if r1.status_code!=200 or r2.status_code!=200:
   print('Sorry cannot fetch data for this product right now!!')
   exit()
  soup2=BeautifulSoup(content2,'html.parser')
  soup1=BeautifulSoup(content,'html.parser')
  lin=[]
  sl=[]
  data={
      "Sold By": [],
      "Product Info": [],
      "Price": [],
      "Link To Site": []
  }

  #scraping spd
  cnt=0
  for t in soup1.find_all('p',attrs={'class':'product-title'},text=True):
        data["Sold By"].append('Snapdeal')
        data["Product Info"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break
  if len(data["Sold By"])==0 :
    for t in soup1.find_all('p',attrs={'class':'product-title'},text=True):
        data["Sold By"].append('Snapdeal')
        data["Product Info"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break

  cnt=0
  for t in soup1.find_all('span',attrs={'class':'lfloat product-price'},text=True):
        data["Price"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break
  cnt=0
  for t in soup1.find_all('a < div',attrs={'class':'dp-widget-link noUdLine hashAdded','href':re.compile("^https://www.snapdeal.com/")},href=True):
        sl.append(t.get('href'))
        data["Link To Site"].append(t.get('href'))
        cnt+=1
        if cnt==5:
          print(sl)
          break

  print(data)
  #scraping flipkart
  cnt=0
  for t in soup2.find_all('div',attrs={'class':'_4rR01T'},text=True):
        data["Sold By"].append('Flipkart')
        data["Product Info"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break
  
  if len(data["Sold By"])<=5:
    for t in soup2.find_all('a',attrs={'class':'s1Q9rs'},title=True):
        data["Sold By"].append('Flipkart')
        data["Product Info"].append(str(t.get_text()))
        cnt+=1
        if cnt==5:
          break

  if len(data["Sold By"])<=5:
    for t in soup2.find_all('div',attrs={'class':'_2WkVRV'},text=True):
        data["Sold By"].append('Flipkart')
        data["Product Info"].append(str(t.get_text()))
        cnt+=1
        if cnt==5:
          break
    cnt=0
    for t in soup2.find_all('a',attrs={'class':'IRpwTa'},title=True):
        data["Product Info"][5+cnt]+=' '+str(t.get_text())
        cnt+=1
        if cnt==5:
          break
        
  cnt=0
  for t in soup2.find_all('div',attrs={'class':'_30jeq3 _1_WHN1'},text=True):
        data["Price"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break
  
  if len(data["Price"])<=5:
    for t in soup2.find_all('div',attrs={'class':'_30jeq3'},text=True):
        data["Price"].append(t.get_text())
        cnt+=1
        if cnt==5:
          break
   
  cnt=0
  #for t in soup2.find_all('a',attrs={'class':'_1fQZEK','href':re.compile("^https://www.flipkart.com/")},href=True):
  for t in soup2.find_all('a',attrs={'class':'_1fQZEK'},href=True):
        #data["Link To Site"].append(t.get('href'))
        lin.append(t.get('href'))
        data["Link To Site"]=lin
        cnt+=1
        if cnt==5:
            #print(data["Link To Site"])
            break
  print(len(data["Link To Site"]))
  
  if len(data["Link To Site"])<=5:
    for t in soup2.find_all('a',attrs={'class':'IRpwTa','href':re.compile("^https://www.flipkart.com/")},href=True):
        data["Link To Site"].append(t.get('href'))
        lin.append(t.get('href'))
        cnt+=1
        if cnt==5:
          break
  if len(data["Link To Site"])<=5:
    for t in soup2.find_all('a',attrs={'class':'s1Q9rs','href':re.compile("^https://www.flipkart.com/")},href=True):
        data["Link To Site"].append(t.get('href'))
        lin.append(t.get('href'))
        cnt+=1
        if cnt==5:
          break
    
  #df=pd.DataFrame(data)
  df = pd.DataFrame.from_dict(data, orient='index')
  df = df.transpose()
  print("df value is:",df)
  for index,rows in df.iterrows():
    if rows["Sold By"]=='Flipkart':
         i=index-5
         rows["Link To Site"]=lin[i]

  for index,rows in df.iterrows():
    if rows["Sold By"]=='Snapdeal':
      rows["Link To Site"]='https://www.snapdeal.com/search?keyword='+rows["Product Info"].replace(" ","%20")+'&sort=rlvncy'
    else:
         #try:
            rows["Link To Site"]='https://www.flipkart.com'+rows["Link To Site"]
            #rows["Link To Site"]=rows["Link To Site"]
         #except:   
            #rows["Link To Site"]='https://www.flipkart.com'+lin[pl]
            #pl+=1
  '''
  #print(df)
  #df.to_csv("output.csv",index=False)
  #x=df.values.tolist()
  #print(x)
  # Creating an empty list
  res=[]
  
  # Iterating through the columns of
  # dataframe
  for column in df.columns:
      
      # Storing the rows of a column
      # into a temporary list
      li = df[column].tolist()
      
      # appending the temporary list
      res.append(li)
      
  # Printing the final list
  print(res)
  '''
  x=df.to_dict('records')
  #print(x)
  #response.close()
  return x
'''
vt=True
while vt:
    try:
      print(comp('laptop'))
      vt=False
    except:
      vt=True 
'''
#items=comp('laptop')
#print(items)