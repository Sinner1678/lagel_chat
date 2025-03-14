import streamlit as st
from huggingface_hub import InferenceClient
import os

st.title("چت با Jamal_law")
st.write("پیام خود را وارد کنید و پاسخ را به صورت زنده ببینید!")

# گرفتن API Key از متغیر محیطی
API_KEY = os.environ.get("HF_API_KEY")
client = InferenceClient(provider="together", api_key=API_KEY)

user_input = st.text_input("پیام خود را وارد کنید:", "")
if st.button("ارسال"):
    if user_input:
        messages = [{"role": "user", "content": user_input}]
        st.write("پاسخ مدل:")
        response_container = st.empty()
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages,
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7,
            stream=True
        )
        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                response_container.write(full_response)
    else:
        st.warning("لطفاً یک پیام وارد کنید!")
