import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from datetime import date, timedelta
import streamlit as st
import streamlit.components.v1 as components
import base64
from io import BytesIO



def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Summary.xlsx">Export to Excel</a>' # decode b'abc' => abc


def data_collater(df):
    data = pd.DataFrame([df.iloc[8,2], df.iloc[8,7], df.iloc[10,2], df.iloc[10,7],  df.iloc[12,2].date(), df.iloc[12,7], 
                     df.iloc[14,2], df.iloc[14,7],
                     df.iloc[23,9], df.iloc[23,10], df.iloc[31,9], df.iloc[31,10], df.iloc[39,9], df.iloc[39,10], df.iloc[47,9], df.iloc[47,10],
                     df.iloc[54,11], df.iloc[85,5], df.iloc[95,1]],
             index=['Name', 'Surname', 'Employee Code', 'Designation', 'Joining Date', 'Department',
                    'Primary Supervisor', 'Secondary Supervisor',
                    'Employee KRA 1', 'Supervisor KRA 1','Employee KRA 2', 'Supervisor KRA 2','Employee KRA 3', 'Supervisor KRA 3','Employee KRA 4', 'Supervisor KRA 4',
                    "Supervisor's Final Rating", "Supervisor's General Comments", "Supervisor's Recommendation"])
    return data


st.write("""
    # FG PARS Data Collater
    """)
    

multiple_files = st.file_uploader(
    "Multiple File Uploader",
    accept_multiple_files=True
)

file_count = list(multiple_files)

if len(file_count)>0:
	st.write(str(len(file_count)) +" files uploaded sucessfully.")
	df = pd.DataFrame(index=['Name', 'Surname', 'Employee Code', 'Designation', 'Joining Date', 'Department',
                    'Primary Supervisor', 'Secondary Supervisor',
                    'Employee KRA 1', 'Supervisor KRA 1','Employee KRA 2', 'Supervisor KRA 2','Employee KRA 3', 'Supervisor KRA 3','Employee KRA 4', 'Supervisor KRA 4',
                    "Supervisor's Final Rating", "Supervisor's General Comments", "Supervisor's Recommendation"])
	df.index.name='Summary'


	for i in range(len(file_count)):
		summ = pd.read_excel(multiple_files[i])
		summ = data_collater(summ)
		summ.index.name = 'Summary'
		summ.columns = [summ.iloc[0,0]]
		df = df.merge(summ, on='Summary')

	st.write(df.T)
	st.markdown(get_table_download_link(df.T), unsafe_allow_html=True)
else:
	st.write('No files uploaded')





