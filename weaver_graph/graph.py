from typing import Callable, Dict, Any, List, Optional

END = object()


class StateGraph:
 """A lightweight directed state graph for helpdesk orchestration.

 Nodes are callables with signature: func(state: dict, *args, **kwargs) -> dict
 The returned dict is merged into the state. Routing can be accomplished by
 setting `state['classification']` to the next node name.
 """

 def __init__(self, state_type: Any = dict):
 self.state_type = state_type
 self._nodes: Dict[str, Callable] = {}
 self._edges: Dict[str, List] = {}
 self._entry: Optional[str] = None

 def add_node(self, name: str, func: Callable):
 self._nodes[name] = func

 def add_edge(
 self,
 src: str,
 dst: str,
 condition: Optional[Callable[[dict], bool]] = None,
 ):
 self._edges.setdefault(src, []).append((condition, dst))

 def set_entry_point(self, name: str):
 self._entry = name

 def add_conditional_edges(
 self,
 src: str,
 condition_fn: Callable[[dict], str],
 mapping: Optional[Dict[str, str]] = None,
 ):
 """Convenience: store a condition function that returns a routing key.

 If mapping is provided, the returned key is mapped to a target node name.
 Otherwise, the returned string is treated as the node name directly.
 """

 def wrapper(state: dict):
 target = condition_fn(state)
 if mapping is not None and isinstance(target, str):
 return mapping.get(target, None)
 return target

 self._edges.setdefault(src, []).append((wrapper, None))

 def compile(self):
 graph = _CompiledGraph(self._nodes, self._edges, self._entry)
 return graph


class _CompiledGraph:
 def __init__(
 self,
 nodes: Dict[str, Callable],
 edges: Dict[str, List],
 entry: Optional[str],
 ):
 self._nodes = nodes
 self._edges = edges
 self._entry = entry

 def run(
 self,
 state: dict,
 *runtime_args,
 max_steps: int = 100,
 **runtime_kwargs
 ) -> dict:
 """Execute the graph starting from the entry point.

 `runtime_args` and `runtime_kwargs` are forwarded to node callables
 (e.g., vector_db_client).
 """
 if self._entry is None:
 raise RuntimeError("Entry point not set on StateGraph")

 current = self._entry
 steps = 0

 while current is not None and current is not END and steps < max_steps:
 steps += 1
 node_fn = self._nodes.get(current)
 if node_fn is None:
 # No node registered for this name; stop execution
 break

 result = node_fn(state, *runtime_args, **runtime_kwargs) or {}

 # Merge conversational history intelligently
 if "conversation_history" in result:
 existing = state.get("conversation_history", [])
 state["conversation_history"] = (
 existing + result["conversation_history"]
 )
 # remove from result so normal update doesn't overwrite
 del result["conversation_history"]

 # Merge the rest of the state
 state.update(result)

 # Evaluate edges
 next_node = None
 for cond, dst in self._edges.get(current, []):
 if cond is None:
 # unconditional edge
 next_node = dst
 break
 try:
 # cond may be a callable that returns a bool or returns a
 # node name
 res = cond(state)
 except Exception:
 res = None

 if isinstance(res, str):
 # condition function returned a target node name
 next_node = res
 break
 if res is True and dst is not None:
 next_node = dst
 break

 # Fallback: use classification field if present and matches a node
 if next_node is None:
 cls = state.get("classification")
 if isinstance(cls, str) and cls in self._nodes:
 next_node = cls

 # If next_node signals END sentinel or is missing, end loop
 if next_node is None or next_node is END:
 break

 current = next_node

 return state

 def stream(
 self,
 state: dict,
 config: Optional[dict] = None,
 *runtime_args,
 max_steps: int = 100,
 **runtime_kwargs
 ):
 """Mock stream method to match LangGraph API and yield node updates."""
 if self._entry is None:
 raise RuntimeError("Entry point not set on StateGraph")

 current = self._entry
 steps = 0

 while current is not None and current is not END and steps < max_steps:
 steps += 1
 node_fn = self._nodes.get(current)
 if node_fn is None:
 break

 result = node_fn(state, *runtime_args, **runtime_kwargs) or {}

 # Merge conversational history
 if "conversation_history" in result:
 existing = state.get("conversation_history", [])
 state["conversation_history"] = (
 existing + result["conversation_history"]
 )
 del result["conversation_history"]

 state.update(result)

 # Yield update matching langgraph structure
 yield {current: result}

 # Evaluate edges
 next_node = None
 for cond, dst in self._edges.get(current, []):
 if cond is None:
 next_node = dst
 break
 try:
 res = cond(state)
 except Exception:
 res = None

 if isinstance(res, str):
 next_node = res
 break
 if res is True and dst is not None:
 next_node = dst
 break

 if next_node is None:
 cls = state.get("classification")
 if isinstance(cls, str) and cls in self._nodes:
 next_node = cls

 if next_node is None or next_node is END:
 break

 current = next_node

 invoke = run

