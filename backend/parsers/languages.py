LANGUAGE_CONFIGS = {
    "python": {
        "extension": ".py",
        "function_query": """
            (function_definition
                name: (identifier) @function.name
                parameters: (parameters) @function.params
                return_type: (type)? @function.return_type
            ) @function.def
        """,
        "class_query": """
            (class_definition
                name: (identifier) @class.name
                body: (block) @class.body
            ) @class.def
        """,
        "import_query": """
            [
                (import_statement
                    name: (dotted_name) @import.name
                )
                (import_from_statement
                    module_name: (dotted_name) @import.module
                )
            ]
        """,
        "call_query": """
            (call
                function: [
                    (identifier) @call.name
                    (attribute
                        attribute: (identifier) @call.name
                    )
                ]
            )
        """,
    },
    "javascript": {
        "extension": ".js",
        "function_query": """
            [
                (function_declaration
                    name: (identifier) @function.name
                    parameters: (formal_parameters) @function.params
                ) @function.def
                (arrow_function
                    parameters: (formal_parameters) @function.params
                ) @function.def
                (method_definition
                    name: (property_identifier) @function.name
                    parameters: (formal_parameters) @function.params
                ) @function.def
            ]
        """,
        "class_query": """
            (class_declaration
                name: (identifier) @class.name
                body: (class_body) @class.body
            ) @class.def
        """,
        "import_query": """
            [
                (import_statement
                    source: (string) @import.source
                )
                (import_clause
                    (identifier) @import.name
                )
            ]
        """,
        "call_query": """
            (call_expression
                function: [
                    (identifier) @call.name
                    (member_expression
                        property: (property_identifier) @call.name
                    )
                ]
            )
        """,
    },
    "typescript": {
        "extension": ".ts",
        "function_query": """
            [
                (function_declaration
                    name: (identifier) @function.name
                    parameters: (formal_parameters) @function.params
                    return_type: (type_annotation)? @function.return_type
                ) @function.def
                (arrow_function
                    parameters: (formal_parameters) @function.params
                    return_type: (type_annotation)? @function.return_type
                ) @function.def
                (method_definition
                    name: (property_identifier) @function.name
                    parameters: (formal_parameters) @function.params
                    return_type: (type_annotation)? @function.return_type
                ) @function.def
            ]
        """,
        "class_query": """
            (class_declaration
                name: (type_identifier) @class.name
                body: (class_body) @class.body
            ) @class.def
        """,
        "import_query": """
            (import_statement
                source: (string) @import.source
            )
        """,
        "call_query": """
            (call_expression
                function: [
                    (identifier) @call.name
                    (member_expression
                        property: (property_identifier) @call.name
                    )
                ]
            )
        """,
    },
}


def get_language_config(language: str) -> dict:
    return LANGUAGE_CONFIGS.get(language, {})


def get_supported_languages() -> list[str]:
    return list(LANGUAGE_CONFIGS.keys())
