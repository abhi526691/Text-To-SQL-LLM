import streamlit as st


class View():
    def __init__(self):
        pass

    def title(self, message):
        return st.title(message)

    def file_uploader(self, message, type=[]):
        return st.file_uploader(message, type=type)

    def button(self, message):
        return st.button(message)

    def text_area(self, label, message):
        return st.text_area(label=label, value=message)

    def write(self, message):
        return st.write(message)

    def header(self, message):
        return st.header(message)

    def success(self, message):
        return st.success(message)

    def warning(self, message):
        return st.warning(message)

    def error(self, message):
        return st.error(message)
