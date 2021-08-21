"""
библиотеки: pip install streamlit numpy
запуск приложения: STREAMLIT_SERVER_PORT=80 streamlit run app.py
"""

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
# import numpy as np
import pandas as pd
# import os
import subprocess as sp
import shlex
import json
 
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
        data = list()
        left, right = st.columns(2)
        with left:
            st.header("Текст")
            st.write(obj["text"])
        for key, value in obj["cards"].items():
            with right:
                st.header(key)
                st.write(value["text"])
                st.markdown("---")
