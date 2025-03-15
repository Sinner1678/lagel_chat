import streamlit as st
from together import Together

# تنظیم کلید API
client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# اعمال استایل RTL
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

# تنظیم عنوان اپلیکیشن
st.title("چت و خلاصه‌ساز با Jamal_law")

# تب‌بندی برای چت و خلاصه‌ساز
tab1, tab2 = st.tabs(["چت مکالمه‌ای", "خلاصه‌ساز متن"])

# بخش چت مکالمه‌ای
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.text_input("سوال خود را وارد کنید:", key="user_input")

    if st.button("ارسال", key="chat_button"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("در حال پردازش..."):
                try:
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                        messages=st.session_state.messages,
                        max_tokens=None,
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
                    st.rerun()
                except Exception as e:
                    st.error("❌ مشکلی در دریافت پاسخ وجود دارد.")
                    st.exception(e)
        else:
            st.warning("لطفاً یک ورودی وارد کنید.")

# بخش خلاصه‌ساز
with tab2:
    st.subheader("خلاصه‌سازی متن طولانی")
    long_text = st.text_area("متن طولانی خود را اینجا وارد کنید:", height=200)
    
    if st.button("خلاصه کن", key="summarize_button"):
        if long_text:
            with st.spinner("در حال خلاصه‌سازی..."):
                try:
                    summary_prompt = f"لطفاً متن زیر را خلاصه کن و نکات کلیدی آن را استخراج کن:\n\n{long_text}"
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                        messages=[{"role": "user", "content": summary_prompt}],
                        max_tokens=500,
                        temperature=0.5,
                        top_p=0.9,
                        stream=False
                    )

                    summary = response.choices[0].message.content
                    st.write("### خلاصه و نکات کلیدی:")
                    st.write(summary)
                except Exception as e:
                    st.error("❌ مشکلی در خلاصه‌سازی وجود دارد.")
                    st.exception(e)
        else:
            st.warning("لطفاً متنی وارد کنید.")
