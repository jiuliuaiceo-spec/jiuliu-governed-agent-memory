"""Clean-room, dependency-free reference implementation."""
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any

REQUIRED = ("task_id", "event_id", "conversation_id", "connector_run_id")
LAYERS = ("cognition", "planning", "execution", "memory", "supervision")

def digest(value: Any) -> str:
    return sha256(repr(value).encode()).hexdigest()

class GovernanceError(ValueError): pass
class CandidateState(str, Enum):
    CREATED="created"; PENDING_REVIEW="pending_review"; SOURCE_VERIFIED="source_verified"
    APPROVED="approved"; PUBLISHED="published"; OBSERVED="observed"; ROLLED_BACK="rolled_back"

@dataclass(frozen=True)
class Context:
    task_id: str; event_id: str; conversation_id: str; connector_run_id: str
    policy_hash: str; goal_hash: str
    def validate(self):
        if any(not getattr(self, x) for x in REQUIRED): raise GovernanceError("missing_context")

@dataclass
class Candidate:
    content: str; context: Context; state: CandidateState=CandidateState.CREATED

class KnowledgeAdapter:
    def search(self, query: str, scope: str) -> dict: return {"hits": [], "sources": [], "read_only": True}
    def retain(self, *args, **kwargs): raise GovernanceError("knowledge_write_denied")

class MemoryAdapter:
    def __init__(self, available=True): self.available=available; self.rows=[]
    def recall(self, query, context):
        context.validate()
        if not self.available: return {"status":"memory_unavailable", "degraded":True, "results":[]}
        return {"status":"ok", "degraded":False, "results":list(self.rows)}
    def retain(self, content, context):
        context.validate()
        if not self.available: return {"status":"memory_unavailable", "degraded":True}
        self.rows.append({"content":content, "context":context}); return {"status":"ok", "readback":True}
    def consolidate(self, context): context.validate(); return {"status":"ok" if self.available else "memory_unavailable", "degraded":not self.available}

class Connector:
    def __init__(self, memory=None, knowledge=None): self.memory=memory or MemoryAdapter(); self.knowledge=knowledge or KnowledgeAdapter(); self.audit=[]
    def recall(self, query, context): return self.memory.recall(query, context)
    def candidate(self, content, context):
        context.validate(); c=Candidate(content, context); self.audit.append({"event":"candidate_created","state":c.state.value,"context":context}); return c
    def publish(self, candidate, context):
        context.validate()
        if candidate.context.policy_hash != context.policy_hash or candidate.context.goal_hash != context.goal_hash: raise GovernanceError("governance_hash_mismatch")
        if candidate.state is not CandidateState.APPROVED: raise GovernanceError("candidate_not_approved")
        candidate.state=CandidateState.PUBLISHED; return candidate
    def trace(self, context, statuses=None):
        context.validate(); return {"context":context, "layers":{x:(statuses or {}).get(x,"recorded") for x in LAYERS}}
