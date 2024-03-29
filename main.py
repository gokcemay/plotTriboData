import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
import numpy
import sigfig #For significant figures
from matplotlib.lines import Line2D




#change plot style to something fancy
plt.style.use("fivethirtyeight")

# Global varaibles

All_title = []
SSCoF = pd.DataFrame()
SSDCoF = pd.DataFrame()
av_f_CoF_A= pd.DataFrame()




#Function to add values to the bar plot
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]*0.5, y[i], ha='center', va='center',
                 bbox=dict(facecolor='white', alpha=.5))

# Function to select the directory
def select_directory(entry):
    directory_entry.delete(0,"end")
    directory = tk.filedialog.askdirectory()
    entry.insert(0, directory)

# Function to plot the files
def plot_files(directory):
    global l_data
    global max_distance
    global av_f_CoF_A
    global All_title
    global figCoFs
    global av_f_CoF
    figCoFs = plt.figure()

    # Get all the txt files in the directory
    txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    l_data = pd.DataFrame()
    data_s = pd.DataFrame() # DAta frame for steady state
    Av_CoF = []
    Std_CoF = []
    values = []
    # Plot each txt file
    max_distance = None # Set max distance as None before loop
    min_distance = None # Set max distance as None before loop

    for i, txt_file in enumerate(txt_files):
        # Read the data from the txt file
        data = pd.read_csv(os.path.join(directory, txt_file), encoding='utf-16-le', sep='\t', lineterminator='\r')


        # Remove the commas from the Distance [m] column.
        data["Distance [m]"] = data["Distance [m]"].str.replace(",", ".")
        distance = data["Distance [m]"].astype(float)
        if max_distance is None or len(distance) > len(max_distance): max_distance = distance    # if length of distance is greater set it as max distance so plot wont give error
        if min_distance is None or len(distance) > len(min_distance): min_distance = distance    # if length of distance is greater set it as max distance so plot wont give error

        # Remove the commas from the µ column.
        data[" µ"] = data[" µ"].str.replace(",", ".")
        CoF = data[" µ"].astype(float)
        CoF = abs(CoF)

        # Find the maximum value of CoF every 20 samples.
        f_CoF = CoF.rolling(20).max()
        Av_CoF.append(f_CoF.mean()) # Find the mean value of CoF
        Std_CoF.append(f_CoF.std()) # Find the std  of CoF
        values.append(txt_file[8:18])
        #print(f_CoF.info)
        l_data=pd.concat([l_data, f_CoF], axis=1)

        #ADD-----------------------------------
        # Export all CoF SS values for all samples with folder name as file name
        # Then another script will plot boxplots for each sample and combine them



# Plot column 2 versus absolute column 4
        #plt.subplot(2,2,len(txt_files) + 1).set_title(txt_file)
        plt.plot(distance, f_CoF, label=txt_file)




    plt.legend()
    # Show the plot
    d_title= directory[-3:] # Title of the plot last 2
    d_title= d_title.replace('/', '')
    plt.savefig('D:/Results/'+d_title+"average",bbox_inches='tight')
    plt.show()

# Average f_CoF values
    av_f_CoF = numpy.mean(l_data, axis=1)
    result = av_f_CoF.info
    print(result)
    title = directory[-3:]
    All_title += [title]
    print(values)
    av_f_CoF = av_f_CoF.rolling(500).max()
    plt.plot(max_distance, av_f_CoF, label=directory)
    plt.title(d_title)
    plt.savefig('D:/Results/'+d_title+"avCoF",bbox_inches='tight')
    plt.ylim([0, 0.38])
    plt.show()

    Av_CoF_f=[round(elem, 5) for elem in Av_CoF ] # round to 5 digits
    plt.bar(values, Av_CoF,yerr=Std_CoF, color ='blue', width = 0.4)
    addlabels(values, Av_CoF_f)
    plt.xlabel("Samples")
    plt.ylabel("CoF")
    plt.title("CoF values")
    plt.savefig('D:/Results/'+d_title+"Bar.png",bbox_inches='tight')
    plt.show()

# Av_CoF with Error bars

    # plt.errorbar(values,Av_CoF,Std_CoF,xerr= None,ls='none', marker ='^')
    # addlabels(values, Av_CoF_f)
    # plt.xlabel("Samples")
    # plt.ylabel("CoF")
    # plt.title("CoF values")
    # plt.savefig('D:/Results/'+d_title+"SD.png")
    # plt.show()

# Append Average Cof values Av_CoF_f_A
#    av_f_CoF_A = numpy.concatenate((av_f_CoF_A, av_f_CoF.rolling(500).max()), axis=0)
    av_f_CoF_A = pd.concat([av_f_CoF_A, pd.DataFrame(av_f_CoF.rolling(500).max())],axis=1)


def steady (vEntry):
    #-- Calculate steady state
    global SSCoF
    global SSDCoF
    if max_distance is None:
        print("Max distance none")
    else:
        print("max distance",max(max_distance),"Entry",vEntry,"/n","Max distance value",numpy.argmax(max_distance>vEntry),"Null value",av_f_CoF.isnull().values.any())
        index = numpy.argmax(max_distance>vEntry)
        SSCoF= numpy.append(SSCoF, (numpy.mean(av_f_CoF[index:])))
        SSDCoF= numpy.append(SSDCoF, (numpy.std(av_f_CoF[index:])))
        print(SSDCoF)
        print(SSCoF)
        print(All_title)





def plotAll ():
    global SSCoF
    global All_title
    global SSDCoF
            #Write results to a file
    with open('D:/Results/CoF'+str(''.join(All_title))+'.csv', 'w') as f: # Make a new csv file with all sample names
        f.write('Samples, '+str(', '.join(All_title))) # Convert elements of list to strings
        f.write('\n'+'CoF, '+str(', '.join(str(x) for x in SSCoF))) # Convert elements of dataframe to strings
        f.write('\n'+'SD, '+str(', '.join(str(x) for x in SSDCoF))) # Convert elements of dataframe to strings

    v1= [round(elem, 5) for elem in SSCoF ] # round to 5 digits
    plt.bar(All_title,SSCoF,yerr=SSDCoF,xerr= None,align='center', alpha=0.5, ecolor='black', capsize=10)
    addlabels(All_title, v1)
    plt.xlabel("Samples")
    plt.ylabel("CoF")
    plt.title("CoF values")
    plt.savefig('D:/Results/'+"All data",bbox_inches='tight')
    plt.show()


def plotCoFAll (): #plot all CoF values
    global av_f_CoF_A
    global All_title
    max_distance2 = pd.DataFrame(numpy.arange(0, 50, (50/len(av_f_CoF_A)), dtype=float)) # found the length of the dataframe av_f_CoF_A and make a new df for time
    print(All_title)
    print('Dataframe burada')
    print(av_f_CoF_A)
    #generate empty figure
    figCoFs = plt.figure()
    plt.ylim([0, 0.38])             #set ylimit
    plt.title("CoF vs Distance")    #set title

    figCoFs = plt.plot( max_distance2, av_f_CoF_A)
    plt.legend(figCoFs, All_title) # set legend from All_title for CoFs plot
    plt.savefig('D:/Results/'+"All CoF",bbox_inches='tight')

    plt.show()

# Create the GUI window
window = tk.Tk()
window.title("Plot TXT Files")
# Define geometry of the window
window.geometry("700x250")
# Create the directory selection entry
directory_entry = tk.Entry(window, bg="white", width=50, borderwidth=2)
directory_entry.pack()

# Create the browse button
browse_button = tk.Button(window, text="Browse", command=lambda: select_directory(directory_entry))
browse_button.pack()

# Create the plot button
plot_button = tk.Button(window, text="Plot", command=lambda: plot_files(directory_entry.get()))
plot_button.pack()

#Create an Entry Widget
entrySS= tk.Entry(window,font=('Century 12'),width=40)
entrySS.pack(pady= 10)
entrySS.pack()

# Create the steady button
plot_button = tk.Button(window, text="Steady plot", command=lambda: steady(int(entrySS.get())))
plot_button.pack()

# Create the Allplot button
plot_button = tk.Button(window, text="Plot ALL", command=lambda: plotAll())
plot_button.pack()

# Create all CoF versus distance plots button
pbutton = tk.Button(window, text="Plot CoF all", command=lambda: plotCoFAll ())
pbutton.pack()


# Create the main loop
window.mainloop()
