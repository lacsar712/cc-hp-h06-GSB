"""列表与详情的展示拼装：如实反映落库结论，不改写 verdict/reason。"""

PASS = "放行"


def present(row: dict) -> dict:
    """在落库字段之上补展示字段（列表色 tone、脚注 footnote），库字段原样保留。"""
    out = dict(row)
    out["tone"] = "pass" if out.get("verdict") == PASS else "fail"
    out["footnote"] = out.get("reason", "")
    return out
