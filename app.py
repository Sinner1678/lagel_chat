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


st.title("چت  با Jamal_law")



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
