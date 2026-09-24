"""放行粉饰旁路：落库后置、列表措辞、详情脚注把放行刷成未放行。"""

BYPASS_NAME = "放行粉饰旁路"
FAIL = "未放行"
FAIL_NOTE = "清炒温度不在范围内"


def polish_after_store(verdict: str, reason: str) -> tuple[str, str]:
    if verdict == "放行":
        return FAIL, FAIL_NOTE
    return verdict, reason


def map_list_copy(row: dict) -> dict:
    out = dict(row)
    v, r = polish_after_store(out.get("verdict", ""), out.get("reason", ""))
    out["verdict"] = v
    out["reason"] = r
    out["tone"] = "fail" if v == FAIL else "pass"
    out["footnote"] = r
    out["bypass"] = BYPASS_NAME
    return out


def map_detail_copy(row: dict) -> dict:
    return map_list_copy(row)


def trace(verdict: str, reason: str) -> dict:
    pv, pr = polish_after_store(verdict, reason)
    return {"bypass": BYPASS_NAME, "raw": verdict, "polished": pv, "note": pr}
