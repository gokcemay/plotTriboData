import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog
import matplotlib.pyplot as plt

#change plot style to something fancy
plt.style.use("fivethirtyeight")

class CSVSelector:
    def __init__(self, root):
        self.root = root
        self.filename1 = None
        self.filename2 = None

        self.label1 = tk.Label(root, text="Select CSV file 1:")
        self.label1.pack()

        self.filechooser1 = tk.Button(root, text="Select file 1", command=self.select_file1)
        self.filechooser1.pack()

        self.label2 = tk.Label(root, text="Select CSV file 2:")
        self.label2.pack()

        self.filechooser2 = tk.Button(root, text="Select file 2", command=self.select_file2)
        self.filechooser2.pack()

        self.button = tk.Button(root, text="Submit", command=self.submit)
        self.button.pack()

    def select_file1(self):
        self.filename1 = tk.filedialog.askopenfilename(title="Select CSV file 1", filetypes=[("CSV files", "*.csv")])

    def select_file2(self):
        self.filename2 = tk.filedialog.askopenfilename(title="Select CSV file 2", filetypes=[("CSV files", "*.csv")])

    def submit(self):
        if self.filename1 is not None and self.filename2 is not None:
            # Read the data from the CSV files
            df1 = pd.read_csv(self.filename1, header=0, delimiter=',')
            df2 = pd.read_csv(self.filename2, header=0, delimiter=',')

            # Transpose the data (Rows to columns)
            df_transposed1 = df1.transpose()
            df_transposed2 = df2.transpose()

            # Make first row column names
            df_transposed1.columns = df_transposed1.iloc[0]
            df_transposed2.columns = df_transposed2.iloc[0]

            # Remove first row
            df_transposed1 = df_transposed1.tail(-1)
            df_transposed2 = df_transposed2.tail(-1)

            # Make Row Names Column
            df_transposed1=df_transposed1.rename_axis("Samples").reset_index()
            df_transposed2=df_transposed2.rename_axis("Samples").reset_index()

            #Print dataframes
            print(df_transposed1)
            print('\n')
            print(df_transposed2)

            # Create a two-column plot
            fig, axs = plt.subplots(1, 2)

            # set ylimit before errorbar https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html#matplotlib.pyplot.errorbar

            axs[0].set_ylim(0.20,0.35)
            axs[1].set_ylim(0.20,0.35)

            # Plot the error plot in the left column
            ax1 = axs[0].errorbar(df_transposed1['Samples'], df_transposed1['CoF'], df_transposed1['SD'],ls='none',capsize=10, marker='^', markersize=10, markerfacecolor='red', label=self.filename1)


            ax2 = axs[1].errorbar(df_transposed2['Samples'], df_transposed2['CoF'], df_transposed2['SD'],ls='none',capsize=10, marker='^', markersize=10, markerfacecolor='blue', label=self.filename2)


            # Add a legend to the right column
            axs[0].legend([ax1[0]], labels=['CoF'])
            axs[1].legend([ax2[0]], labels=['CoF'])

            # Set the title and labels of the plot
            fig.suptitle('Error Plot of CoF')
            axs[0].set_xlabel('Samples')
            axs[1].set_xlabel('Samples')

            # Show the plot
            plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    csv_selector = CSVSelector(root)
    root.mainloop()
