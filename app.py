import streamlit as st
from together import Together

client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

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


st.title("چت، خلاصه‌ساز حقوقی، صدور و تحلیل آراء قضایی با Jamal_law")


tab1, tab2, tab3, tab4 = st.tabs(["چت مکالمه‌ای", "خلاصه‌ساز متون حقوقی", "صدور رای قضایی", "تحلیل آراء قضایی"])


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


with tab2:
    st.subheader("خلاصه‌ساز متون حقوقی")
    legal_text = st.text_area("متن حقوقی خود را اینجا وارد کنید:", height=200, key="legal_text_input")
    
    if st.button("استخراج نکات حقوقی", key="legal_summarize_button"):
        if legal_text:
            with st.spinner("در حال استخراج نکات حقوقی..."):
                try:
                    legal_summary_prompt = f"""
                    متن حقوقی زیر را تحلیل کن و فقط نکات دقیق حقوقی (مانند مواد قانونی مرتبط، مسئولیت‌های قانونی، تخلفات یا حقوق طرفین) را به صورت فهرست‌وار استخراج کن. جزئیات غیرضروری یا غیرحقوقی (مثل توضیحات عمومی یا احساسی) را حذف کن:\n\n{legal_text}
                    """
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                        messages=[{"role": "user", "content": legal_summary_prompt}],
                        max_tokens=500,
                        temperature=0.5,
                        top_p=0.9,
                        stream=False
                    )
                    legal_summary = response.choices[0].message.content
                    st.write("### نکات حقوقی کلیدی:")
                    st.markdown(legal_summary)
                except Exception as e:
                    st.error("❌ مشکلی در استخراج نکات حقوقی وجود دارد.")
                    st.exception(e)
        else:
            st.warning("لطفاً متنی وارد کنید.")

with tab3:
    st.subheader("صدور رای قضایی")
    legal_incident = st.text_area("رخداد حقوقی را توضیح دهید:", height=150, key="legal_incident")
    legal_references = st.text_area("مواد قانونی مرتبط (اختیاری):", height=100, key="legal_references")
    
    if st.button("صدور رای", key="judgment_button"):
        if legal_incident:
            with st.spinner("در حال صدور رای..."):
                try:
                    if legal_references:
                        judgment_prompt = f"بر اساس رخداد حقوقی زیر و مواد قانونی ذکرشده، یک رای قضایی بنویس که شامل یافته‌های事実، استناد به قوانین، و تصمیم نهایی باشد:\n\nرخداد: {legal_incident}\nمواد قانونی: {legal_references}"
                    else:
                        judgment_prompt = f"بر اساس رخداد حقوقی زیر، یک رای قضایی بنویس که شامل یافته‌های事実، استناد به قوانین مرتبط (خودت حدس بزن)، و تصمیم نهایی باشد:\n\nرخداد: {legal_incident}"
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                        messages=[{"role": "user", "content": judgment_prompt}],
                        max_tokens=1000,
                        temperature=0.5,
                        top_p=0.9,
                        stream=False
                    )
                    judgment = response.choices[0].message.content
                    st.write("### رای قضایی:")
                    st.write(judgment)
                except Exception as e:
                    st.error("❌ مشکلی در صدور رای وجود دارد.")
                    st.exception(e)
        else:
            st.warning("لطفاً رخداد حقوقی را وارد کنید.")

with tab4:
    st.subheader("تحلیل آراء قضایی")
    judgment_text = st.text_area("رای قضایی یا متن حقوقی را وارد کنید:", height=200, key="judgment_text")
    analysis_method = st.selectbox("روش تحلیل:", [
        "پوزیتیویسم حقوقی", 
        "حقوق طبیعی", 
        "رئالیسم حقوقی", 
        "تفسیر نص‌گرایانه", 
        "تفسیر منطقی", 
        "رویکرد غایت‌گرا",
        "تحلیل اقتصادی حقوق"
    ], key="analysis_method")

    method_descriptions = {
        "پوزیتیویسم حقوقی": "پوزیتیویسم حقوقی معتقد است که قانون همان چیزی است که در نص قانونی نوشته شده و باید بدون توجه به اخلاق یا عدالت خارج از قانون اجرا شود. تحلیل باید صرفاً بر اساس نص قانون باشد.",
        "حقوق طبیعی": "حقوق طبیعی بر این باور است که قوانین باید با اصول عدالت و اخلاق ذاتی هم‌راستا باشند. تحلیل باید بررسی کند که آیا رای با مفاهیم عدالت فراتر از نص قانون سازگار است یا خیر.",
        "رئالیسم حقوقی": "رئالیسم حقوقی تأکید دارد که قانون در عمل تحت تأثیر عوامل واقعی مثل رفتار قاضی، شرایط اجتماعی یا سیاسی است. تحلیل باید عوامل خارج از نص را در نظر بگیرد.",
        "تفسیر نص‌گرایانه": "تفسیر نص‌گرایانه فقط به معنای ظاهری و تحت‌اللفظی متن قانون توجه می‌کند و از تفسیر فراتر از نص خودداری می‌کند.",
        "تفسیر منطقی": "تفسیر منطقی به استدلال منطقی پشت قانون و انسجام درونی آن توجه دارد و ممکن است فراتر از معنای ظاهری نص برود.",
        "رویکرد غایت‌گرا": "رویکرد غایت‌گرا به نیت و هدف قانون‌گذار پشت قانون نگاه می‌کند و تحلیل بر اساس مقصود قانون انجام می‌شود.",
        "تحلیل اقتصادی حقوق": "تحلیل اقتصادی حقوق به کارایی اقتصادی قوانین و تصمیمات قضایی توجه دارد. تحلیل باید هزینه‌ها، فایده‌ها و تأثیرات اقتصادی رای را بررسی کند."
    }
    
    if st.button("تحلیل کن", key="analyze_button"):
        if judgment_text:
            with st.spinner("در حال تحلیل..."):
                try:
                    analysis_prompt = f"""
                    متن حقوقی یا رای قضایی زیر را بر اساس روش '{analysis_method}' تحلیل کن. ابتدا توضیح مختصر زیر را در نظر بگیر و تحلیلت را بر اساس آن انجام بده:\n
                    توضیح روش: {method_descriptions[analysis_method]}\n
                    حالا متن زیر را تحلیل کن و خروجی را به صورت ساختارمند (با سرفصل‌های 'روش‌شناسی' و 'تحلیل') ارائه کن:\n\n{judgment_text}
                    """
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                        messages=[{"role": "user", "content": analysis_prompt}],
                        max_tokens=1000,
                        temperature=0.6,
                        top_p=0.9,
                        stream=False
                    )
                    analysis = response.choices[0].message.content
                    st.write("### تحلیل رای قضایی:")
                    st.markdown(analysis)
                except Exception as e:
                    st.error("❌ مشکلی در تحلیل وجود دارد.")
                    st.exception(e)
        else:
            st.warning("لطفاً متنی وارد کنید.")
