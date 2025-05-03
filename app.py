import streamlit as st
import requests
from together import Together

client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# تنظیمات استایل فارسی
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

st.title("🧠 چت + 🌐 جستجو در وب")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ورودی کاربر
user_input = st.text_input("سوال خود را وارد کنید:")

if st.button("ارسال"):
    if not user_input.strip():
        st.warning("لطفاً سوالی وارد کنید.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("ابتدا در حال جستجو در وب..."):
            # جستجو در DuckDuckGo
            url = f"https://api.duckduckgo.com/?q={user_input}&format=json"
            try:
                res = requests.get(url)
                data = res.json()

                summaries = []
                if "RelatedTopics" in data:
                    for topic in data["RelatedTopics"]:
                        if "Text" in topic:
                            summaries.append(topic["Text"])
                        elif "Topics" in topic:
                            for subtopic in topic["Topics"]:
                                if "Text" in subtopic:
                                    summaries.append(subtopic["Text"])

                # انتخاب نهایتاً 5 نتیجه خلاصه شده
                search_context = "\n".join(summaries[:5]) if summaries else "نتیجه‌ای از جستجو پیدا نشد."

            except Exception as e:
                st.error("خطا در جستجو از وب.")
                st.exception(e)
                search_context = "جستجو در وب ناموفق بود."

        # ساخت پیام برای مدل
        system_prompt = "شما یک دستیار حقوقی هستید که ابتدا نتایج جستجو در وب را بررسی کرده‌اید و سپس پاسخ می‌دهید."
        prompt_to_model = f"""### نتایج جستجو:
{search_context}

### سوال:
{user_input}

### پاسخ دقیق و حقوقی بده:"""

        with st.spinner("در حال تولید پاسخ توسط مدل..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_to_model},
                    ],
                    max_tokens=512,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>", "<|eom_id|>"],
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

                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("مشکل در دریافت پاسخ از مدل.")
                st.exception(e)

# نمایش چت قبلی
st.markdown("---")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
