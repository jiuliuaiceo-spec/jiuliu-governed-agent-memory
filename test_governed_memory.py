import unittest
from governed_memory import *

class Tests(unittest.TestCase):
 def ctx(self, **kw): return Context("t","e","c","r",kw.get("policy_hash","p"),kw.get("goal_hash","g"))
 def test_context_required(self):
  with self.assertRaises(GovernanceError): Context("","e","c","r","p","g").validate()
 def test_degraded_memory(self): self.assertEqual(MemoryAdapter(False).recall("x",self.ctx())["status"],"memory_unavailable")
 def test_knowledge_read_only(self):
  with self.assertRaises(GovernanceError): KnowledgeAdapter().retain("x")
 def test_publish_requires_approval_and_same_hash(self):
  c=Connector(); cand=c.candidate("x",self.ctx())
  with self.assertRaises(GovernanceError): c.publish(cand,self.ctx())
  cand.state=CandidateState.APPROVED
  with self.assertRaises(GovernanceError): c.publish(cand,self.ctx(goal_hash="new"))
  self.assertEqual(c.publish(cand,self.ctx()).state,CandidateState.PUBLISHED)
 def test_shared_context_consolidation(self):
  c=Connector(); x=self.ctx(); self.assertTrue(c.memory.retain("x",x)["readback"]); self.assertEqual(c.memory.consolidate(x)["status"],"ok")
 def test_trace_has_five_layers(self): self.assertEqual(tuple(Connector().trace(self.ctx())["layers"]),LAYERS)
if __name__=="__main__": unittest.main()
