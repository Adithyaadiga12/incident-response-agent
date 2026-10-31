import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph , MessagesState,START
from langgraph.prebuilt import  ToolNode , tools_condition
from tools import read_logs, get_metrics

load_dotenv()

tools = [read_logs,get_metrics]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
)

llm_with_tools = llm.bind_tools(tools)

def call_model(state:MessagesState):
    reply = llm_with_tools.invoke(state["messages"])
    return {"messages":[reply]}

SYSTEM = """You are an incident response agent.
When given an alert, investigate using your tools:
- read_logs: to see recent errors and warnings
- get_metrics: to see request, error and warning counts

Find the root cause of the problem. Then reply with:
Root cause: <one sentence>
Evidence: <what in the logs/metrics supports it>"""

graph = StateGraph(MessagesState)
graph.add_node("call_model",call_model)
graph.add_node("tools",ToolNode(tools))
graph.add_edge(START,"call_model")
graph.add_conditional_edges("call_model",tools_condition)
graph.add_edge("tools","call_model")

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"messages":
        [("system",SYSTEM),("user", "Alert: users report errors on the /data endpoint. Investigate.")]
        }) 
    print(result["messages"][-1].text)
           

