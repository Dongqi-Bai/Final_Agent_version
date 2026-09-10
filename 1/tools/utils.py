from tools.registry import TOOL_REGISTRY


def run_tool(name, arguments_json):
    entry = TOOL_REGISTRY.get(name)
    if entry is None:
        out = f"未知工具：{name}"
        err = False
    try:
        args = entry["args_model"].model_validate_json(arguments_json)
        out = entry["function"](**args.model_dump())
        err = False
    except Exception as e:
        out = f"工具执行出错：{e}"
        err = True
    return out, err
    


def get_schema():
    return [e["schema"] for e in TOOL_REGISTRY.values()]
    
    
