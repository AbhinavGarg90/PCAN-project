import numpy as np
np.random.seed(0)
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

def hex_to_float(data_string):
    output_list = []
    output_list.append(ord(data_string[0])-1)
    output_list.append(int(str(hex(ord(data_string[2]))) + str(hex(ord(data_string[3])))[2:], base=16)*10**-4)
    output_list.append(int(str(hex(ord(data_string[4]))) + str(hex(ord(data_string[5])))[2:], base=16))
    return output_list

final_array = np.empty(shape=(12,12))
loops_between_updates = 1
number_of_colums = 12
number_of_rows = 12
number_of_cells = 144
max_voltage = 20 #if voltage exceeds this number it would cause the program to crash
strcode_for_voltage = "400"


path = "input file.txt"
file = open(path)
text_file = file.read()
list_file = text_file.splitlines()

fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(np.zeros(shape=(12,12)), cmap="magma_r")
plt.show(block=False)




for x in list_file:

    if x.startswith(strcode_for_voltage) == True:     #filters out non 400 inputs
        pass
    else:
        continue
    
    # handling error for input coming as b" instead of b'
    try:    
        data_string = x[x.index("b'")+2:-2]
    except: 
        data_string = x[x.index('b"')+2:-2]
    data_string = data_string.encode('ASCII').decode("unicode_escape")
    
    #converts input from hex to float
    voltage_array = hex_to_float(data_string)
    
    # converts list of 144 cells to columns and rows
    column = 0
    while voltage_array[0] > number_of_colums-1:
        voltage_array[0] -= number_of_colums
        column += 1
    
    # to prevent possible indexing error
    try:
        final_array[column][voltage_array[0]] = voltage_array[1]
    except:
        print(f'column:{column}, row:{voltage_array[0]}')
    
    # annotated text and colour formats: rounds float values to two decimal places, 
    # 20 is used as max value for normalisation, larger than 20 may cause errors
    ann = ax.text(

        x=voltage_array[0],y=column,s=str(round(voltage_array[1],2)), fontsize = 'x-small',
         horizontalalignment = "center", backgroundcolor=matplotlib.colors.to_hex([1,1-voltage_array[1]/max_voltage,0]), color = "black"
       
         )

    # how many iteration between each chart update
    if loops_between_updates%144 == 0:
        im.set_array(final_array) 
        fig.canvas.draw()

        # refresh rate
        plt.pause(0.1)

        # clears frame after each interation
        for index,child in enumerate(ax.get_children()):
            #prevents error applying to "artist" object
            if isinstance(child, matplotlib.text.Text) and isinstance(child.get_position()[0], int): #prevents error caused by trying to apply function to matplotlib.axes object
                child.remove()
     
        
    loops_between_updates += 1


file.close()
