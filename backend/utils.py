def extract_function_calls(response):
    function_calls: list[dict] = []
    for candidate in response.candidates:  # Iterate through candidates
        for part in candidate.content.parts:     # Iterate through parts
            if part.function_call:  # Check if 'function_call' exists
                function_call = part.function_call
                function_call_dict = {function_call.name: {}}
                for key, value in function_call.args.items():
                    function_call_dict[function_call.name][key] = value
                function_calls.append(function_call_dict)
    return function_calls
