

descriptions = [
    {
        "type": "function",
        "function": {
            "name": "get_local_time",
            "description": "Returns the current local time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        "returns": "The current local time."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_info",
            "description": "Get flight information between two locations",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "The departure airport, e.g. DUS",
                    },
                    "destination": {
                        "type": "string",
                        "description": "The destination airport, e.g. HAM",
                    },
                },
                "required": ["origin", "destination"],
            },
            "returns": "The flight information between the two locations."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cheapest_flight",
            "description": "Get cheapest flight between two locations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "The departure airport, e.g. DUS",
                    },
                    "destination": {
                        "type": "string",
                        "description": "The destination airport, e.g. HAM",
                    },
                    "depart_date": {
                        "type": "string",
                        "description": "The departure date in the format YYYY-MM-DD",
                    },
                },
                "required": ["origin", "destination"],
            },
            "returns": "The flight information between the two locations."
        }
    },
]
