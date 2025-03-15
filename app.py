import streamlit as st
from together import Together

# تنظیم کلید API
client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# تنظیم عنوان اپلیکیشن
st.title("چت مکالمه‌ای با Jamal_law")

# مقداردهی اولیه تاریخچه در session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش تاریخچه چت
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# دریافت ورودی از کاربر
user_input = st.text_input("سؤال خود را وارد کنید:", key="user_input")

# ارسال درخواست به مدل و نمایش پاسخ
if st.button("ارسال"):
    if user_input:
        # اضافه کردن پیام کاربر به تاریخچه
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("در حال پردازش..."):
            try:
                # ارسال کل تاریخچه به مدل
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

                # جمع‌آوری و نمایش پاسخ به‌صورت تدریجی
                output_placeholder = st.empty()
                full_response = ""

                for token in response:
                    if hasattr(token, 'choices') and token.choices:
                        delta_content = token.choices[0].delta.content
                        if delta_content:
                            full_response += delta_content
                            output_placeholder.write(full_response)

                # اضافه کردن پاسخ مدل به تاریخچه
                st.session_state.messages.append({"role": "assistant", "content": full_response})

                # به‌روزرسانی صفحه برای نمایش تاریخچه جدید
                st.rerun()

            except Exception as e:
                st.error("❌ مشکلی در دریافت پاسخ وجود دارد.")
                st.exception(e)
    else:
        st.warning("لطفاً یک ورودی وارد کنید.")
