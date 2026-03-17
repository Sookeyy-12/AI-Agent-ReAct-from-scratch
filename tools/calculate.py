def tool(operation):
    return eval(operation)

definition = {
    "name": "calculate",
    "description": "Calculates the result of a mathematical operation.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "description": "The mathematical operation to perform.",
            },
        },
        "required": ["operation"],
    },
}