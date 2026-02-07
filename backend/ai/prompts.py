SUMMARIZE_CODEBASE = """You are a code analysis expert. Analyze the following codebase structure and provide a clear, concise summary.

Repository: {repo_name}
Total Files: {file_count}
Languages: {languages}

File Structure:
{file_structure}

Classes and Functions:
{code_elements}

Provide:
1. A 2-3 sentence overview of what this codebase does
2. The main components/modules
3. Key architectural patterns observed
4. Entry points (if identifiable)

Be concise and technical."""


ANSWER_QUESTION = """You are a code assistant helping developers understand a codebase.

Repository: {repo_name}

Codebase Structure:
{context}

User Question: {question}

Instructions:
1. Answer the question based on the codebase information provided
2. Reference specific files, functions, or classes when relevant
3. If you need to show code locations, format them as: [file:line_start-line_end]
4. Be concise but thorough
5. If the answer cannot be determined from the context, say so clearly

Response:"""


EXPLAIN_CODE = """You are a code explainer helping developers understand specific code elements.

File: {file_path}
Element: {element_name} ({element_type})
Lines: {start_line} to {end_line}

Code:
```{language}
{code}
```

Surrounding Context:
{context}

Explain:
1. What this code does (in plain English)
2. Its purpose in the larger system
3. Key logic or algorithms used
4. Any notable patterns or potential issues

Keep the explanation clear and practical."""


FIND_RELATED = """Given the following code element:

Element: {element_name}
Type: {element_type}
File: {file_path}

And these related elements from the codebase:
{related_elements}

Identify and explain:
1. Direct dependencies (what this element uses)
2. Dependents (what uses this element)
3. Related functionality (similar or complementary code)

Format as a structured list."""
