from cv2 import detail_SeamFinder, dnn_DetectionModel
import pandas as pd
import numpy as np
import datetime


def OsciFinder(df_invest,start):
    df_1=df_invest.index[0] #move to more general point and add for loop
    df_2=df_invest.index[1]
    differnece=df_2-df_1
    try:
        sampling_rate = differnece.total_seconds()
    except AttributeError:
        sampling_rate=1 #in Seconds
    if sampling_rate<=0:
        sampling_rate=1 #in Seconds
    #sampling_rate=12
    df_invest=np.array(df_invest)
    a=0.01 #Percent 
    n_lim=10
    load=[]
    counter=0
    waves=0
    iae=0
    number_osci=0
    counter_crossing=0
    counter_limit=30
    counter_index=0
    #to ensure that there is also a check on the time line
    n=0
    max_samples=-1
    end_index=[]
    list_osci_slices=[]
    intermend_res_list=[]
    last_osci=False
    tsup_start=False

    store_between=[]
    cylces_between=[]

    #For Testing 
    iae_test=[]
    iae_test_plt=[]
    iae_lim_test=[]
    iae_comp=[]

    for i in range(1,len(df_invest)): 
        sign_old=int(np.sign(df_invest[i-1:i]))
        sign_current=int(np.sign(df_invest[i:i+1]))
        if tsup_start==True:
            n+=1
        if sign_current==sign_old:
            iae = iae + float(abs(df_invest[i:i+1]) * sampling_rate)
            counter+=1
        else:
            if counter==0: # Get over the initial value of 0
                counter=1
            omega_i=2*3.14159/(counter*sampling_rate)
            iae_lim = 2 * a / omega_i
            counter=0
            #Testing
            iae_lim_test.append(iae_lim)
            iae_lim_test.append('idx '+str(i))

            if iae>iae_lim:
                number_osci+=1
                end_index.append(i+start)
                #Test
                iae_comp.append('iae')
                iae_comp.append(iae)
                iae_comp.append('iae_lim')
                iae_comp.append(iae_lim)
                iae_comp.append('<- idx '+str(i))
            iae=float(abs(df_invest[i:i+1]) * sampling_rate)
            
            counter_crossing+=1
            intermend_res_list.append(i+start)
            counter_index+=1
            if counter_index==2:
                start_ind=intermend_res_list[-2]
                end_ind=intermend_res_list[-1]
                between=end_ind-start_ind
                max_samples=between*10
                tsup_start=True
                n=0
            
        #Test
        iae_test.append(iae)
        iae_test.append('idx '+str(i))
        iae_test_plt.append(iae)
        
        if n==max_samples:
            n=0
            tsup_start=False
            if number_osci>=n_lim:
                list_osci_slices.append('start')
                list_osci_slices.append(min(end_index))
                list_osci_slices.append(max(end_index))
                list_osci_slices.append('end')
                #Experiment
                store_between.append(max_samples)
                cylces_between.append(False)
            #Check if there are any cylces containing oscillation 
            if number_osci >= 2 and number_osci < n_lim:
                cylces_between.append(True) # MAYBE UNIQUE NUMBER --> 1 go on , 2 osci between with cylces , 3 not
            end_index=[]                 
            counter_crossing=0
            number_osci=0
            counter_index=1
            time_counter=0

    # Outside of Loop             
    list_results=[]
    counter=0 
    intermed_value=0
    for i in range(3,len(list_osci_slices)):
        if list_osci_slices[i-3] =='start' and list_osci_slices[i] =='end' and intermed_value>0:
            list_results.append(list_osci_slices[i-1])
            list_results.append('end')
            intermed_value=0
            counter=0
        if list_osci_slices[i-3] =='start' and list_osci_slices[i] =='end':
            list_results.append('start')
            list_results.append(list_osci_slices[i-2])
            list_results.append(list_osci_slices[i-1])
            list_results.append('end')
    
    res_list_connected=[]
     #check if list is empty and if so return empty list 
    if not list_results:
        return res_list_connected
    
    loop_steps=range(int(len(list_results)/4))
    loop_steps_max=max(loop_steps)
    for i in loop_steps:
        if i < loop_steps_max:
            if i == 0:
                start_1=list_results[(i*4)+1] #start
                end_1=list_results[(i*4)+2] #end
                start_2=list_results[(i*4)+5] #start 2
                end_2=list_results[(i*4)+6] #end 2
            else:
                start_1=res_list_connected[-3] #start
                end_1=res_list_connected[-2] #end
                start_2=list_results[(i*4)+5] #start 2
                end_2=list_results[(i*4)+6] #end 2
            if abs(end_1-start_2) <= store_between[i]: # MAYBE HERE CONDITION TO CHECK IF THERE ARE ANY CYCLEY IN BETWEEN 
                if i==0:
                    res_list_connected.append('start')
                    res_list_connected.append(start_1)
                    res_list_connected.append(end_2)
                    res_list_connected.append('end')
                else:
                    res_list_connected.pop(-1)
                    res_list_connected.pop(-1)

                    res_list_connected.append(end_2)
                    res_list_connected.append('end')
            else:
                res_list_connected.append('start')
                res_list_connected.append(list_results[(i*4)+1])
                res_list_connected.append(list_results[(i*4)+2])
                res_list_connected.append('end')

    return res_list_connected




    


