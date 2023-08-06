from mb_std import Result, hr


def waves_balance(node: str, address: str, timeout=10, proxy=None) -> Result[int]:
    url = f"{_add_slash(node)}addresses/balance/{address}"
    res = hr(url, timeout=timeout, proxy=proxy)
    try:
        if res.is_error():
            return res.to_error()
        if "balance" in res.json:
            return res.to_ok(res.json["balance"])
        return res.to_error("unknown_response")
    except Exception as e:
        return res.to_error(f"exception: {str(e)}")


def asset_balance(node: str, address: str, asset_id: str, timeout=10, proxy=None):
    url = f"{_add_slash(node)}assets/balance/{address}/{asset_id}"
    res = hr(url, timeout=timeout, proxy=proxy)
    try:
        if res.is_error():
            return res.to_error()
        if "balance" in res.json:
            return res.to_ok(res.json["balance"])
        return res.to_error("unknown_response")
    except Exception as e:
        return res.to_error(f"exception: {str(e)}")


def _add_slash(node: str) -> str:
    if node.endswith("/"):
        return node
    return node + "/"
