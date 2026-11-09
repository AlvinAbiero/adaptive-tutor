from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore


class S(TypedDict):
    messages: Annotated[list, add_messages]
    thread_msgs: int
    learner_memories: int


def node(state: S, config, *, store):
    learner = config["configurable"]["learner_id"]
    ns = (learner, "memories")
    text = state["messages"][-1].content
    store.put(ns, f"m{len(store.search(ns)) + 1}", {"text": text})
    return {
        "thread_msgs": len(state["messages"]),
        "learner_memories": len(store.search(ns)),
    }


builder = StateGraph(S)
builder.add_node("node", node)
builder.add_edge(START, "node")
builder.add_edge("node", END)

store = InMemoryStore()
graph = builder.compile(checkpointer=InMemorySaver(), store=store)


def run(learner, thread, msg):
    cfg = {"configurable": {"learner_id": learner, "thread_id": f"{learner}:{thread}"}}
    out = graph.invoke({"messages": [("user", msg)]}, cfg)
    print(
        f"{learner:10} {thread:8} thread_msgs={out['thread_msgs']} "
        f"learner_memories={out['learner_memories']}"
    )


run("learner_42", "lesson-1", "I think tuples can be changed")
run("learner_42", "lesson-2", "I like analogies")
run("learner_7", "lesson-1", "I want to build a scraper")
run("learner_42", "lesson-1", "second message, same lesson")
