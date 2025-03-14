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
                    max_tokens=512,
                    temperature=0.7
                )
                # نمایش جزئیات کامل پاسخ برای اشکال‌یابی
                st.json(response)

                # بررسی صحت خروجی
                if 'output' in response:
                    st.write(response['output'])
                else:
                    st.error("❌ مشکلی در دریافت پاسخ وجود دارد. ساختار پاسخ:")
                    st.json(response)

            except Exception as e:
                st.error(f"❌ خطایی رخ داد: {e}")
    else:
        st.warning("لطفاً یک ورودی وارد کنید.")
