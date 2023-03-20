import streamlit as st
import streamlit.components.v1 as com
with open("design.css") as source:
    design=source.read()

com.html(f"""
<html>
    <div>
    <style>
    {design}
    </style>
    <h1 class="heading">
    Resume Parser
    </h1>
    </div>
    </html>
""", height=500)