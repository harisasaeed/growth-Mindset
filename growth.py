import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title=  "Data Sweeper",layout='wide')
#css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#title
st.title("DataSweeper Sterling Integrator By Harisa Saeed")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization creating the project for quarter q3")
#file uploader
uploaded_files = st.file_uploader("Choose a files (accepts CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=(True))
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name) [-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file type. Please upload a CSV or Excel file: {file_ext}")
            continue 
        
        #file deatils
        st.write("preview the head of the Dataframe") 
        st.dataframe(df.head())
        
        #data cleaning option
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"Clean data for {file.name}"): 
            col1 , col2 = st.columns(2)
            with col1:
                    if st.button(f"Remove duplicate from the file : {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("Duplicate Remove!")
                        with col2:
                            if st.button(f"Fill Missing Values For: {file.name}"):
                                numeric_cols = df.select_dtypes(include=['number']).columns   
                                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  
                                st.write(" ✅ Missing values have been failed!")
                                
        st.subheader(" 🎯 Select Columns to keep")  
        columns = st.multiselect(f"Choose columns for {file.name}" , df.columns, default=df.columns)   
        df - df[columns]                                          
        
    #data visualization
    st.subheader("📟 Data Visualization")   
    if st.checkbox(f" Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        
    #Conversion options
    st.subheader(" conversion Options")   
    conversion_type = st.radio(f"convert {file.name} to:", ["CVS", "Excel"], key=file.name) 
    if st.button(f"Covert{file.name}"):
        buffer = BytesIO()
        if conversion_type == "CVS":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, "csv")
            mime_type = "text/csv"
            
        elif conversion_type == "Excel":
            df.to.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, "xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            
st.success("🎉 All files Processed Successfuly!")            
            
            
            
            