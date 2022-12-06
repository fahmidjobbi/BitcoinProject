
import numpy as np
def handle_uploaded_file(f):  
    with open(r"C:\Users\Fahmi\dev\Job-e\Bitcoinproject\BTC\pages\static\uploads"+ "\\" +f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
            
            
def normalise_zero_base(df):
    return df / df.iloc[0] - 1
def normalise_min_max(df):
    return (df - df.min()) / (df.max() - df.min())


def extract_window_data(df, window_len=5, zero_base=True):
    window_data = []
    for idx in range(len(df) - window_len):
        tmp = df[idx: (idx + window_len)].copy()
        if zero_base:
            tmp = normalise_zero_base(tmp)
        window_data.append(tmp.values)
    return np.array(window_data)