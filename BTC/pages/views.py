from django.shortcuts import render
from django.views.generic import TemplateView
import joblib as joblib
import openpyxl
from django.http import HttpResponse
from pages.functions import handle_uploaded_file ,normalise_zero_base,normalise_min_max,extract_window_data
from pages.forms import StudentForm
from keras import models
import numpy as np
import pandas as pd 
import os
import matplotlib.pyplot as plt
from itertools import cycle
import plotly.express as px
 
def home(request):
    context={}
    return render(request, 'index.html', context)

 
def analyze(request):
    context={}
    return render(request, 'analyze.html', context)
       
    

def about(request):
    context={}
    return render(request, 'about.html', context)




def result (request):
    if request.method == 'POST':
        student=StudentForm(request.POST,request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            a='File uploaded successfully'
            return render(request,"result.html",{'a':a})
    else:
        student=StudentForm()
        return render(request,"result.html",{'form':student})



        
def predict (request):
    target_col = ['Close']
    window_len = 5
   
    #dst_path =  str(os.path.abspath(os.getcwd()))+r"\dev\Job-e\Bitcoinproject\BTC\pages\static\uploads"+"\\"+"uploadsdatabtc.csv"
    path=r"C:\Users\Fahmi\dev\Job-e\Bitcoinproject\BTC\pages\static\uploads\databtc.csv"
    d=pd.read_csv(path)
    d=d.set_index('Date')
    d.dropna(inplace=True)
    d1=normalise_zero_base(d)
    d1=normalise_min_max(d)
    d1=extract_window_data(d, window_len = 5, zero_base = True)
    
    m=models.load_model(r'C:\Users\Fahmi\dev\Job-e\Bitcoinproject\BTC\modelbitcoin.sav')
    
    o1=m.predict(d1).squeeze()
    o1 = np.nan_to_num(o1)
    d1=np.nan_to_num(d1)
    o = d[target_col].values[:-window_len] * (o1 + 1)
    o = pd.Series(index=d.index[5:], data=o[:, 0])  
    #p=o.to_list()
    p=o.to_frame()
    p=p.reset_index()
    p.columns=['Date','Close']
    #p=p.set_index('Date')
        
    fig = px.line(d,x=d.index[5:], y=o, labels={'y':'Close price','x': 'Date'})
    fig.show()
    #fig.write_html(r"C:\Users\Fahmi\dev\Job-e\Bitcoinproject\BTC\pages\templates\predicto.html")
    
    
    return render(request,"predict.html",{'o':p})
        
        
        


'''def result(request):
    
    cls=joblib.load('newmodel.sav')
    lis=[]
    lis.append(request.GET['OverTime'])
    lis.append(request.GET['Companyculture'])
    lis.append(request.GET['Worktimingsatisfaction'])
    lis.append(request.GET['Salaryandbenefit'])
    lis.append(request.GET['Skilldevelopment'])
    lis.append(request.GET['Worksatisfaction'])
    lis.append(request.GET['YerasAtCompany'])
    lis.append(request.GET['Worklifebalance'])
    lis.append(request.GET['Careergrowth'])

    print(lis)
    
    pred=cls.predict([lis])
      #pred is the predicted value
            
            
    return render(request, 'result.html', {'result':pred})'''




def team(request):
    context={}
    return render(request, 'team.html', context)

def contacte(request):
    context={}
    return render(request, 'contacte.html', context)
