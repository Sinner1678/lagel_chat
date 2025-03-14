import streamlit as st
from together import Together

# تنظیم کلید API
client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# تنظیم عنوان اپلیکیشن
st.title("Chat with LLaMA 3.3 - Together AI")

# دریافت ورودی از کاربر
user_input = st.text_area("سؤال خود را وارد کنید:")

# ارسال درخواست به مدل و نمایش پاسخ به‌صورت زنده (Streaming)
if st.button("ارسال"):
    if user_input:
        with st.spinner("در حال پردازش..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=None,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>", "<|eom_id|>"],
                    stream=True
                )

                # نمایش خروجی به‌صورت تدریجی
                output_placeholder = st.empty()
                full_response = ""

                for token in response:
                    if hasattr(token, 'choices') and token.choices:
                        delta_content = token.choices[0].delta.content
                        if delta_content:
                            full_response += delta_content
                            output_placeholder.write(full_response)

            except Exception as e:
                st.error("❌ مشکلی در دریافت پاسخ وجود دارد.")
                st.exception(e)  # نمایش جزئیات خطا
    else:
        st.warning("لطفاً یک ورودی وارد کنید.")
