import streamlit as st
import requests
from together import Together

# کلیدها از secrets
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# کلاینت Together
client = Together(api_key=TOGETHER_API_KEY)

# استایل راست‌چین فارسی
st.markdown("""
    <style>
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Vazirmatn', sans-serif;
    }
    .stTextInput > div > div > input {
        direction: rtl;
        text-align: right;
    }
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    .stTextArea > div > div > textarea {
        direction: rtl;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.title("چت با Jamal_law + جستجو در وب")

# چت‌بات
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش تاریخچه چت
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ورودی کاربر
user_input = st.text_input("سؤال خود را وارد کنید:", key="user_input")

if st.button("ارسال", key="chat_button"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("در حال جستجو در وب..."):
            # انجام سرچ با Serper.dev
            def search_web(query):
                url = "https://google.serper.dev/search"
                headers = {"X-API-KEY": SERPER_API_KEY}
                payload = {"q": query}
                res = requests.post(url, json=payload, headers=headers)
                results = res.json()
                snippets = []
                if "organic" in results:
                    for r in results["organic"][:5]:
                        if "snippet" in r:
                            snippets.append(r["snippet"])
                return "\n\n".join(snippets)

            search_results = search_web(user_input)
            context = f"""این اطلاعات از نتایج جستجوی وب استخراج شده‌اند:\n{search_results}\n\nحال به پرسش زیر پاسخ بده:\n{user_input}"""

        with st.spinner("در حال تولید پاسخ..."):
            try:
                # ایجاد پاسخ با مدل
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3-70B-Instruct",
                    messages=[
                        {"role": "system", "content": "تو یک دستیار حقوقی هستی که با توجه به اطلاعات وب و تخصص حقوقی پاسخ می‌دهی."},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7,
                    top_p=0.7,
                    max_tokens=1024,
                    stream=True
                )
                output_placeholder = st.empty()
                full_response = ""
                for token in response:
                    if hasattr(token, 'choices') and token.choices:
                        delta_content = token.choices[0].delta.content
                        if delta_content:
                            full_response += delta_content
                            output_placeholder.write(full_response)
                # ذخیره چت
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.rerun()
            except Exception as e:
                st.error("❌ مشکلی در تولید پاسخ وجود دارد.")
                st.exception(e)
    else:
        st.warning("لطفاً یک ورودی وارد کنید.")
