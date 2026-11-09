import sys
import sqlite3
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver


class S(TypedDict):
    messages: Annotated[list, add_messages]
    turns: int


def node(state: S):
    n = state.get("turns", 0) + 1
    note = f"turn {n}, {len(state['messages'])} messages before this reply"
    return {"messages": [("assistant", note)], "turns": n}


builder = StateGraph(S)
builder.add_node("node", node)
builder.add_edge(START, "node")
builder.add_edge("node", END)

conn = sqlite3.connect("tutor_threads.db", check_same_thread=False)
graph = builder.compile(checkpointer=SqliteSaver(conn))

mode = sys.argv[1] if len(sys.argv) > 1 else "write"
thread = sys.argv[2] if len(sys.argv) > 2 else "s1"
cfg = {"configurable": {"thread_id": thread}}


if mode == "write":
    out = graph.invoke({"messages": [("user", "hello")]}, cfg)
    print("turns:", out["turns"], "| messages:", len(out["messages"]))
elif mode == "read":
    snap = graph.get_state(cfg)
    print(
        "turns:",
        snap.values.get("turns", 0),
        "| messages:",
        len(snap.values.get("messages", [])),
    )
