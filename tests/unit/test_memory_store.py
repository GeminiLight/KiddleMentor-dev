import json
from pathlib import Path
import tempfile
import shutil
import unittest
from gen_mentor.core.memory.memory_store import MemoryStore, LearnerMemoryStore

class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.workspace = self.test_dir / "workspace"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_memory_store_basic(self):
        store = MemoryStore(self.workspace)
        store.write_long_term("Test fact")
        self.assertEqual(store.read_long_term(), "Test fact")
        self.assertTrue((self.workspace / "memory" / "user_facts.md").exists())
        
        store.append_history("learner", "Hello")
        history = store.read_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "learner")
        self.assertEqual(history[0]["content"], "Hello")
        self.assertTrue((self.workspace / "memory" / "chat_history.json").exists())

    def test_learner_memory_store(self):
        learner_id = "test_learner"
        store = LearnerMemoryStore(self.workspace, learner_id=learner_id)
        learner_dir = self.workspace / "memory" / learner_id
        
        # Test Profile
        profile = {"name": "Test User", "interests": ["coding"]}
        store.write_profile(profile)
        self.assertEqual(store.read_profile(), profile)
        self.assertTrue((learner_dir / "profile.json").exists())
        
        # Test Objectives
        objectives = {"goals": ["Learn Python"]}
        store.write_objectives(objectives)
        self.assertEqual(store.read_objectives(), objectives)
        self.assertTrue((learner_dir / "objectives.json").exists())
        
        # Test Mastery
        mastery_entry = {"topic": "Unit Testing", "status": "started"}
        store.append_mastery_entry(mastery_entry)
        mastery = store.read_mastery()
        self.assertEqual(len(mastery["entries"]), 1)
        self.assertEqual(mastery["entries"][0]["topic"], "Unit Testing")
        self.assertTrue((learner_dir / "mastery.json").exists())
        
        # Test Evaluations (Merged into mastery)
        evaluation = {"overall_score": 85, "performance_level": "good"}
        store.update_evaluations(evaluation)
        mastery = store.read_mastery()
        self.assertEqual(mastery["last_evaluation"]["overall_score"], 85)
        self.assertEqual(len(mastery["evaluations_history"]), 1)
        
        # Test Learning Path
        learning_path = {"modules": [{"id": "m1", "title": "Intro"}]}
        store.write_learning_path(learning_path)
        self.assertEqual(store.read_learning_path(), learning_path)
        self.assertTrue((learner_dir / "learning_path.json").exists())
        
        # Test Context
        context = store.get_learner_context()
        self.assertIn("Test User", context)
        self.assertIn("Learn Python", context)
        self.assertIn("Unit Testing", context)
        self.assertIn("Learning Mastery & Performance", context)

if __name__ == "__main__":
    unittest.main()
