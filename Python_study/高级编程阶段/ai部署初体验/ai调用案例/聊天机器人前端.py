import streamlit as st
from 聊天机器人后端 import get_response
from langchain.memory import ConversationBufferMemory
st.title("无敌战神大模型")

with st.sidebar:
    api_key = st.text_input("请输入Tongyi账号的api_key")
    if api_key:
        st.write("成功传入apikey~")
    st.session_state["api_key"] = api_key
    st.markdown("[获取Tongyi账号的API KEY](https://bailian.console.aliyun.com/?apiKey=1#/api-key)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory()
    st.session_state["messages"] = [{"role":"ai","content":"请问"}]

for message in st.session_state["messages"]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input("问咩啊？")

if prompt:
    if not api_key:
        st.warning("想白嫖？")
        st.stop()
    if api_key:
        try:
            with st.chat_message(name="human"):
                st.write(prompt)
            with st.spinner("running..."):
                res = get_response(api_key=api_key,prompt=prompt,memory=st.session_state["memory"])["response"]
            st.session_state["messages"].append({"role":"human","content":prompt})
            st.session_state["messages"].append({"role":"ai","content":res})
            with st.chat_message(name="ai"):
                st.write(res)
        except:
            st.warning("api有误desu")


