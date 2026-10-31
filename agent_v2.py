import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,HumanMessage
from tools import read_logs, get_metrics

load_dotenv()

tools = [read_logs, get_metrics]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.environ["GEMINI_API_KEY"]
)
llm_with_tools = llm.bind_tools(tools)

PLANNER_PROMPT = """You are an incident response planner.
Given an alert, write a short numbered plan (2-4 steps) for investigating it
using read_logs and get_metrics. Output only the plan, no investigation yet."""

def planner(state: MessagesState):
    reply = llm.invoke([SystemMessage(content=PLANNER_PROMPT)] + state["messages"])
    nudge = HumanMessage(content="Now carry out this plan using your tools and report the root cause.")
    return {"messages": [reply, nudge]}

def call_model(state: MessagesState):
    reply = llm_with_tools.invoke(state["messages"])
    return {"messages": [reply]}

graph = StateGraph(MessagesState)
graph.add_node("planner", planner)
graph.add_node("call_model", call_model)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "planner")
graph.add_edge("planner", "call_model")
graph.add_conditional_edges("call_model", tools_condition)
graph.add_edge("tools", "call_model")
app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({
        "messages": [
            ("user", "Alert: users report errors on /data. Investigate.")
        ]
    })
    for m in result["messages"]:
        m.pretty_print()