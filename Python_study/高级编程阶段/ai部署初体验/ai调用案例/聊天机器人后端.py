from langchain_community.llms import Tongyi
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def get_response(memory,api_key,prompt):
    llm = Tongyi(model="qwen-max",api_key=api_key)
    chain = ConversationChain(llm=llm,memory=memory)
    response = chain.invoke(prompt)
    return response

if __name__ == '__main__':
    with open("../apikey","r") as f:
        api_key = f.read()
    memory = ConversationBufferMemory(return_messages=True)
    prompt = input("请问：")
    res = get_response(memory=memory,prompt=prompt,api_key=api_key)["response"]
    print(res)
