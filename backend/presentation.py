"""读模型拼装：列表与详情如实展示落库结论，不做任何改写。"""

PASS = "放行"


def present(row: dict) -> dict:
    """把落库的一行记录拼成列表/详情响应。

    tone 与 footnote 完全由库存的 verdict/reason 推导：
    放行 -> tone "pass"，其余 -> tone "fail"，脚注即判定理由原文。
    """
    out = dict(row)
    out["tone"] = "pass" if out.get("verdict") == PASS else "fail"
    out["footnote"] = out.get("reason", "")
    return out
