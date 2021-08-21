"""
библиотеки: pip install streamlit numpy
запуск приложения: STREAMLIT_SERVER_PORT=80 streamlit run app.py --server.maxUploadSize=1028
"""

import streamlit as st
import pandas as pd
import subprocess as sp
import shlex
import json
 
st.set_page_config(layout="wide")
uploaded_files = st.file_uploader('Choose your video', type="MP4")
 
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
