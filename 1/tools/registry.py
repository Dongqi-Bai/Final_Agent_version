

TOOL_REGISTRY = {}

def tool(name, description, args_model):
    def deco(fn):
        TOOL_REGISTRY[name] = {
            "function":fn,
            "args_model":args_model,
            "schema":{
                "type":"function",
                "name": name,
                "description":description,
                "parameters":args_model.model_json_schema(),
            }
        }
        return fn
    return deco

        