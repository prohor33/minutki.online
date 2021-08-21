"""
библиотеки: pip install streamlit numpy
запуск приложения: STREAMLIT_SERVER_PORT=80 streamlit run app.py --server.maxUploadSize=1028
"""

import streamlit as st
import pandas as pd
import subprocess as sp
import shlex
import json
import os
import base64
 
st.set_page_config(layout="wide")
uploaded_files = st.file_uploader(label='Выберите файл для загрузки', type="MP4")
 
if uploaded_files is not None:
    video_bytes = uploaded_files.read()
    st.video(video_bytes)
    with st.spinner('Пожалуйста подождите, идет анализ данных...'):
        normal = sp.run(
            shlex.split("python runner.py"),
            stdout=sp.PIPE, stderr=sp.PIPE,
            check=True,
            text=True
        )
        output = normal.stdout
        obj = json.loads(output)
        print(os.path.abspath("."))
        print(os.listdir("."))
        files = os.listdir("./report")
       
        if files:
            with open(os.path.join("./report", files[0]), "rb") as fp:
                bytes = fp.read()
                b64 = base64.b64encode(bytes).decode()
                href = f'<a href="data:base64,{b64}" download="{files[0]}">Скачать отчет в формате Word</a>'
                st.markdown(href, unsafe_allow_html=True)


        left, right = st.columns(2)
        with left:
            st.markdown("<h2 style='text-align: center;'>Текст</h2>", unsafe_allow_html=True)
            st.write(obj["text"])
        with right:
            st.markdown("<h2 style='text-align: center;'>Поручения</h2>", unsafe_allow_html=True)
            st.markdown("---")
        for record in obj["cards"]:
            with right:
                st.write(record["assignment"]["text"])
                st.caption(f"Ответственный: {record['responsible']['text']}")
                st.caption(f"Срок: {record['date']['text']}")
                st.markdown("---")
