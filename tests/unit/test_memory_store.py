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

        # Test Learning Goals
        goal_id = store.add_goal("Learn Python")
        goals = store.read_learning_goals()
        self.assertEqual(len(goals["goals"]), 1)
        self.assertEqual(goals["goals"][0]["learning_goal"], "Learn Python")
        self.assertEqual(goals["active_goal_id"], goal_id)
        self.assertTrue((learner_dir / "learning_goal.json").exists())

        # Test get_active_goal
        active = store.get_active_goal()
        self.assertIsNotNone(active)
        self.assertEqual(active["learning_goal"], "Learn Python")
        self.assertEqual(active["goal_id"], goal_id)

        # Test get_active_goal_id
        self.assertEqual(store.get_active_goal_id(), goal_id)

        # Test adding a second goal deactivates the first
        goal_id_2 = store.add_goal("Learn Rust")
        goals = store.read_learning_goals()
        self.assertEqual(len(goals["goals"]), 2)
        self.assertEqual(goals["active_goal_id"], goal_id_2)
        self.assertEqual(goals["goals"][0]["status"], "inactive")
        self.assertEqual(goals["goals"][1]["status"], "active")

        # Test Skill Gaps
        store.write_skill_gaps_for_goal(goal_id, {
            "skill_gaps": [{"name": "Testing", "is_gap": True}]
        })
        gaps = store.read_skill_gaps()
        self.assertIn(goal_id, gaps)
        self.assertEqual(len(gaps[goal_id]["skill_gaps"]), 1)
        self.assertTrue((learner_dir / "skill_gaps.json").exists())

        # Test read_skill_gaps_for_goal
        goal_gaps = store.read_skill_gaps_for_goal(goal_id)
        self.assertEqual(len(goal_gaps["skill_gaps"]), 1)
        self.assertEqual(goal_gaps["skill_gaps"][0]["name"], "Testing")

        # Test read_skill_gaps_for_goal with nonexistent goal
        empty_gaps = store.read_skill_gaps_for_goal("nonexistent")
        self.assertEqual(empty_gaps, {})

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
        self.assertEqual(store.read_learning_path()["modules"], learning_path["modules"])
        self.assertTrue((learner_dir / "learning_path.json").exists())

        # Test goal-scoped learning path
        store.write_learning_path_for_goal(goal_id, {
            "learning_path": [{"id": "s1", "title": "Session 1"}]
        })
        goal_path = store.read_learning_path_for_goal(goal_id)
        self.assertEqual(len(goal_path["learning_path"]), 1)
        self.assertEqual(goal_path["learning_path"][0]["title"], "Session 1")

        # Test read_learning_path_for_goal with nonexistent goal
        empty_path = store.read_learning_path_for_goal("nonexistent")
        self.assertEqual(empty_path, {})

        # Test Context
        context = store.get_learner_context()
        self.assertIn("Test User", context)
        self.assertIn("Learn Rust", context)
        self.assertIn("Unit Testing", context)
        self.assertIn("Learning Mastery & Performance", context)
        self.assertIn("Learning Goals", context)
        self.assertIn("Skill Gaps", context)

if __name__ == "__main__":
    unittest.main()
