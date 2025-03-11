import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytesIO
import openpyxl # type: ignore

st.set_page_config(page_title = "Data Sweeper", layout = 'wide')

#custom css
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

#title and description
st.title("Data Sweeper sterling by Syed Maaz Hassan")
st.write("Transform your files between CSV and Excel formats which built-in data cleaning and visualizing Creating the project for quarter 3!")

#upload file
uploaded_files = st.file_uploader("Upload you files (accepts CSV and Excel):", type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
            continue

        #file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")


            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled with mean successfully!")

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns) 
        df = df[columns]


        #data visualizations
        st.subheader("Data Visualizations")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_charts(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CVS","Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            )

st.success("All files processed successfully!")



