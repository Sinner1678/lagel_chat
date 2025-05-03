import streamlit as st
import requests

# تنظیم استایل فارسی
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
    </style>
""", unsafe_allow_html=True)

st.title("🌐 جستجو در وب با Serper")

if "search_results" not in st.session_state:
    st.session_state.search_results = []

# ورودی کاربر
query = st.text_input("سوال خود را وارد کنید:")

if st.button("جستجو"):
    if not query.strip():
        st.warning("لطفاً سوالی وارد کنید.")
    else:
        with st.spinner("در حال جستجو در وب..."):
            try:
                headers = {
                    "X-API-KEY": st.secrets["SERPER_API_KEY"],
                    "Content-Type": "application/json"
                }
                json_data = {
                    "q": query
                }

                response = requests.post("https://google.serper.dev/search", headers=headers, json=json_data)
                data = response.json()

                results = []
                if "organic" in data:
                    for item in data["organic"][:5]:  # فقط ۵ نتیجه اول
                        title = item.get("title", "")
                        snippet = item.get("snippet", "")
                        link = item.get("link", "")
                        results.append(f"🔹 **{title}**\n\n{snippet}\n[مشاهده لینک]({link})\n")

                st.session_state.search_results = results

            except Exception as e:
                st.error("خطا در جستجو.")
                st.exception(e)

# نمایش نتایج
st.markdown("---")
st.subheader("نتایج جستجو:")
for res in st.session_state.search_results:
    st.markdown(res, unsafe_allow_html=True)
