"""两类结论核对：放行与未放行在判定、落库呈现、列表措辞、脚注上都必须如实。

无任何第三方依赖，可直接运行：python3 test_verdicts.py
也可用 pytest 收集：pytest test_verdicts.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from presentation import present
from rules import judge

# 与 app.py 启动种子一致的两条文书
PASS_DOC = {"steps": [{"name": "清炒", "temp_c": 120, "minutes": 12}]}  # 甘草种子
HUANGQIN_DOC = {"steps": [{"name": "清炒", "temp_c": 40, "minutes": 12}]}  # 黄芩种子：温度过低


def test_pass_verdict_stays_pass_end_to_end():
    # 判定 -> 落库字段 -> 列表措辞/列表色/脚注，全程保持放行
    verdict, reason = judge(PASS_DOC)
    assert verdict == "放行"
    stored = {"herb": "甘草", "doc": PASS_DOC, "verdict": verdict, "reason": reason}
    assert stored["verdict"] == "放行"
    row = present(stored)
    assert row["verdict"] == "放行"
    assert row["tone"] == "pass"
    assert row["footnote"] == "清炒工序符合炮制要求"
    assert "bypass" not in row


def test_huangqin_seed_stays_unreleased():
    # 黄芩未放行种子不可被误改：判定、呈现全程仍是未放行
    verdict, reason = judge(HUANGQIN_DOC)
    assert verdict == "未放行"
    assert reason == "清炒温度不在范围内"
    row = present({"herb": "黄芩", "doc": HUANGQIN_DOC, "verdict": verdict, "reason": reason})
    assert row["verdict"] == "未放行"
    assert row["tone"] == "fail"
    assert row["footnote"] == "清炒温度不在范围内"
    assert "bypass" not in row


def test_judge_both_conclusions_and_edges():
    # 放行类：边界上下限都放行
    assert judge({"steps": [{"name": "清炒", "temp_c": 80, "minutes": 5}]})[0] == "放行"
    assert judge({"steps": [{"name": "清炒", "temp_c": 150, "minutes": 30}]})[0] == "放行"
    # 未放行类：缺工序、温度过高、时长过长
    assert judge({"steps": []})[0] == "未放行"
    assert judge({"steps": [{"name": "清炒", "temp_c": 200, "minutes": 12}]})[0] == "未放行"
    assert judge({"steps": [{"name": "清炒", "temp_c": 120, "minutes": 40}]})[0] == "未放行"


def test_polish_bypass_dismantled_everywhere():
    # 三处粉饰已拆：旁路模块不复存在，应用源码不再引用任何粉饰入口
    assert not (pathlib.Path(__file__).parent / "pass_polish.py").exists()
    src = (pathlib.Path(__file__).parent / "app.py").read_text(encoding="utf-8")
    for token in ("pass_polish", "polish_after_store", "map_list_copy", "map_detail_copy"):
        assert token not in src


if __name__ == "__main__":
    checks = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for check in checks:
        check()
        print(f"ok {check.__name__}")
    print(f"{len(checks)} 项核对全部通过")
