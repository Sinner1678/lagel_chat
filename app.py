import streamlit as st
import together

# تنظیم کلید API
together.api_key = st.secrets["TOGETHER_API_KEY"]

# تنظیم عنوان اپلیکیشن
st.title("Chat with LLaMA 3.3 - Together AI")

# دریافت ورودی از کاربر
user_input = st.text_area("سؤال خود را وارد کنید:")

# ارسال درخواست به مدل و نمایش پاسخ
if st.button("ارسال"):
    if user_input:
        with st.spinner("در حال پردازش..."):
            try:
                response = together.Complete.create(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                    prompt=user_input,
                    max_tokens=256,  # کاهش تعداد توکن‌ها
                    temperature=0.7
                )
                # نمایش پاسخ مدل
                st.write(response['output'])

            except Exception as e:
                st.error(f"❌ خطایی رخ داد: {e}")
    else:
        st.warning("لطفاً یک ورودی وارد کنید.")
