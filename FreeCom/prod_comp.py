# import required files and modules

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def detail(p1,p2):
  # set the headers and user string
  headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  }


  def link_gen(x_prod):
      response = requests.get('https://www.flipkart.com/search?q='+x_prod, headers=headers)
      #print(response)
      soup = BeautifulSoup(response.content, 'html.parser')
      t=soup.find('a',attrs={'class':'_1fQZEK'})
      link=t.get('href')
      link='https://www.flipkart.com'+link
      return link

  def product(url):
      # send a request to fetch HTML of the page
      
      response = requests.get(url, headers=headers)
      if response.status_code != 200:
        print('Sorry cannot fetch data for this product right now!!')
        exit()
      #print(response)
      # create the soup object
      soup = BeautifulSoup(response.content, 'html.parser')

      # change the encoding to utf-8
      soup.encode('utf-8')

      title = soup.find('span',attrs={'class': 'B_NuCI'}).get_text()
      price = soup.find('div',attrs={'class': '_30jeq3 _16Jk6d'}).get_text()

      th=[]
      th.append('Title')
      th.append('Price')
      for td in soup.find_all('td',attrs={'class':'_1hKmbr col col-3-12'},text=True):
          th.append(td.get_text())

      td=[]
      td.append(title)
      td.append(price)
      for t in soup.find_all('li',attrs={'class':'_21lJbe'},text=True):
          td.append(t.get_text())
      
      
      if len(th)==2:
        for i in soup.find_all('div',attrs={'class':'col col-3-12 _2H87wv'},text=True):
          th.append(i.get_text())

        for t in soup.find_all('div',attrs={'class':'col col-9-12 _2vZqPX'},text=True):
          td.append(t.get_text())

      if len(th)>len(td):
        th.pop(2)
      else:
        if len(th)<len(td):
          td.pop(2)

      
      data={"Features": th,
        "Details": td
        }

      df=pd.DataFrame(data=data)
      
      return df

  #n=int(input("Enter number of prod: "))

  list_of_df=[]

  #for i in range(0,n):
  x_prod1=p1
  url1=link_gen(x_prod1)
  list_of_df.append(product(url1))

  x_prod2=p2
  url2=link_gen(x_prod2)
  list_of_df.append(product(url2))

  feature={ }
  final={}

  list_of_feature=[]

  for df in list_of_df :
    for index,rows in df.iterrows():
      if rows["Features"] in feature:
        h=1
      else :
        list_of_feature.append(rows["Features"])
        feature[rows["Features"]]=1

  final["Features"]=list_of_feature
  heading='Details of Product '
  for i in range(0,2):
    final[heading+str(i+1)]=[]


  for f in list_of_feature:
    i=0
    for df in list_of_df :
      flag=0 
      for index,rows in df.iterrows():
        if rows["Features"]==f:
          flag=1
          final[heading+str(i+1)].append(rows["Details"])
      if flag==0:
        final[heading+str(i+1)].append('NA')
      i+=1

  final_df=pd.DataFrame(data=final)
  #final_df.to_excel("data.xls",index=False)
  print(final_df.columns)
  x=final_df.to_dict('records')
  #print(x)
  return x