"""两类结论的核对：判定、落库展示拼装都不许把放行刷成未放行，也不许反向误改。"""

import importlib
import unittest

from presentation import present
from rules import judge

# 与 app.py startup 种子一致的文书
GANCAO_SEED_DOC = {"steps": [{"name": "清炒", "temp_c": 120, "minutes": 12}]}
HUANGQIN_SEED_DOC = {"steps": [{"name": "清炒", "temp_c": 40, "minutes": 12}]}


class JudgePassTest(unittest.TestCase):
    """放行类结论核对。"""

    def test_gancao_seed_doc_is_pass(self):
        verdict, reason = judge(GANCAO_SEED_DOC)
        self.assertEqual(verdict, "放行")
        self.assertEqual(reason, "清炒工序符合炮制要求")

    def test_boundary_temps_and_minutes_pass(self):
        for temp_c, minutes in [(80, 5), (150, 30), (100, 12)]:
            verdict, _ = judge({"steps": [{"name": "清炒", "temp_c": temp_c, "minutes": minutes}]})
            self.assertEqual(verdict, "放行", f"temp_c={temp_c}, minutes={minutes}")


class JudgeFailTest(unittest.TestCase):
    """未放行类结论核对。"""

    def test_huangqin_seed_doc_stays_fail(self):
        # 黄芩种子温度过低，必须判未放行，任何改动不得把它刷成放行
        verdict, reason = judge(HUANGQIN_SEED_DOC)
        self.assertEqual(verdict, "未放行")
        self.assertEqual(reason, "清炒温度不在范围内")

    def test_temp_200_is_fail(self):
        verdict, _ = judge({"steps": [{"name": "清炒", "temp_c": 200, "minutes": 12}]})
        self.assertEqual(verdict, "未放行")

    def test_minutes_out_of_range_is_fail(self):
        verdict, reason = judge({"steps": [{"name": "清炒", "temp_c": 120, "minutes": 60}]})
        self.assertEqual(verdict, "未放行")
        self.assertEqual(reason, "清炒时长不在范围内")

    def test_missing_fry_step_is_fail(self):
        verdict, reason = judge({"steps": []})
        self.assertEqual(verdict, "未放行")
        self.assertEqual(reason, "缺少清炒工序")


class PresentTest(unittest.TestCase):
    """列表措辞与详情脚注拼装核对：落库什么就展示什么。"""

    def test_pass_row_keeps_pass_with_pass_tone(self):
        row = {"id": 1, "herb": "甘草", "verdict": "放行", "reason": "清炒工序符合炮制要求"}
        out = present(row)
        self.assertEqual(out["verdict"], "放行")
        self.assertEqual(out["reason"], "清炒工序符合炮制要求")
        self.assertEqual(out["tone"], "pass")
        self.assertEqual(out["footnote"], "清炒工序符合炮制要求")

    def test_fail_row_keeps_fail_with_fail_tone(self):
        row = {"id": 2, "herb": "黄芩", "verdict": "未放行", "reason": "清炒温度不在范围内"}
        out = present(row)
        self.assertEqual(out["verdict"], "未放行")
        self.assertEqual(out["reason"], "清炒温度不在范围内")
        self.assertEqual(out["tone"], "fail")
        self.assertEqual(out["footnote"], "清炒温度不在范围内")

    def test_present_does_not_mutate_input_row(self):
        row = {"verdict": "放行", "reason": "清炒工序符合炮制要求"}
        present(row)
        self.assertEqual(row, {"verdict": "放行", "reason": "清炒工序符合炮制要求"})


class PolishRemovedTest(unittest.TestCase):
    """粉饰旁路必须已拆除。"""

    def test_pass_polish_module_is_gone(self):
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module("pass_polish")


if __name__ == "__main__":
    unittest.main()
