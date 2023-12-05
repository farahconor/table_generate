from astropy.table import Table
import pandas as pd
import numpy as np
import tempfile
import os
import shutil
import re
from datetime import date
import configparser
import pathlib
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

class table_generate:
    def __init__(self,index,paper,table,input_file,batch_number): #intializes the table with all the properties from the config file
        self.index = index

        self.title = paper['title']
        self.authors = paper['authors']

        self.alternate_output_name = table['alternate_output_name']
        self.table_name = table['table_name']
        self.RA_column = table['ra_column']
        self.DEC_column = table['dec_column']
        self.main_column = table['main_column']

        self.file_loc = os.path.join(application_path,'data',input_file)
        self.input_file=input_file

        self.raw_name = input_file[:-4]
        if self.alternate_output_name != 'False':
            self.raw_name = self.alternate_output_name

        os.makedirs(os.path.join(application_path,'table_generate_output',str(date.today())+'_batch'+str(batch_number),self.raw_name)) #creates the output folder
        self.output_path = os.path.join(application_path,'table_generate_output',str(date.today())+'_batch'+str(batch_number),self.raw_name)
    
    def make_mrt(self):
        df = pd.read_csv(self.file_loc)
        unitmap = df.to_dict(orient='records')[0] #create a map for the units of each column
        descriptionmap = df.to_dict(orient='records')[1] #create a map for the description of each column
        df = df.drop([0]) #drops the units row
        df = df.drop([1]) #drops the description row

        tempcsv = tempfile.NamedTemporaryFile() #writes a temporary csv file to be read by astropy, this fixes an issue where directly feeding astropy a pandas df doesn't correctly assign datatypes
        df.to_csv(tempcsv,index=False)
        csv = Table.read(tempcsv,format='csv',units=unitmap,descriptions=descriptionmap) #read the csv into an astropy table

        csv.write(os.path.join(self.output_path,'tab'+str(self.index)+'.txt'), overwrite=True, format='mrt') #uses astropy to write and mrt lacking metadata

        mrt_replaceables = { #used to replace empty metadata in the mrt
            'Title:': 'Title: ' + self.title,
            'Authors:': 'Authors: '+ self.authors,
            'Table:': 'Table: '+ self.table_name,
            'table.dat': self.raw_name+'.dat',
        }

        with open(os.path.join(self.output_path,'tab'+str(self.index)+'.txt'), 'r+') as file: #replaces empty MRT metadata
            read_content=file.read()
            #read_content=re.sub("[\[].*?[\]] ", "", read_content) #gets rid of limits, wish this was just an option when exporting
            for key in mrt_replaceables:
                read_content=read_content.replace(key, mrt_replaceables[key])
            file.seek(0)
            file.write(read_content)
        
    def make_html(self):
        pd.read_csv(self.file_loc,header=[0,1],skiprows=[2]).to_html(os.path.join(self.output_path,self.raw_name+'.html'),index=False) #makes the html table via pandas
    
    def make_conesearch(self):
        shutil.copy(os.path.join(application_path,'search.php'), self.output_path)
        shutil.copy(self.file_loc, self.output_path)

        consearch_replaceables = { #used to fill in info for conesearch script
            'file_name_replace': '"' + self.input_file + '"',
            'RA_index_replace': self.RA_column,
            'DEC_index_replace': self.DEC_column,
            'main_index_replace': self.main_column
        }

        with open(os.path.join(self.output_path,'search.php'), 'r+') as file: #fills in necessary info for conesearch script
            read_content=file.read()
            for key in consearch_replaceables:
                read_content=read_content.replace(key, consearch_replaceables[key])
            file.seek(0)
            file.write(read_content)

    def make_all(self):
        self.make_mrt()
        self.make_html()
        if self.RA_column:
            self.make_conesearch()

from tkinter.filedialog import askopenfilename

print("Please choose a configuration file")
config_filename = askopenfilename(filetypes=[('Configuration settings', '*.ini')],initialdir=os.path.join(application_path,'config'))
config_filename = os.path.split(config_filename)[-1]

config = configparser.ConfigParser() 
config.read(os.path.join(application_path,'config',config_filename)) #gets the configuration from the ini file

paper_config = dict(config.items('paper')) #grabs the paper configs

batch_number=1
while os.path.exists(os.path.join(application_path,'table_generate_output',str(date.today())+'_batch'+str(batch_number))): #tess for a folder based on date and number of batches existing for today
    batch_number+=1
os.makedirs(os.path.join(application_path,'table_generate_output',str(date.today())+'_batch'+str(batch_number))) #generates the folder based on the dynamic date and batch number

for i, section in enumerate(config.sections()[1:]): #runs through each table in the config and generates the outputs
    table_config = dict(config.items(section))
    table = table_generate(i+1,paper_config,table_config,section,batch_number)
    table.make_all()
