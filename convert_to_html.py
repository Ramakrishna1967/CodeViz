import re
import os
import json

def convert_md_to_html(md_file, html_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pre-process mermaid blocks to be raw text so marked doesn't mess them up too much, 
    # OR we can just use a custom renderer.
    # The custom renderer in the JS below handles 'mermaid' language blocks.
    # So we don't strictly need to regex replace here if marked detects the language correctly.
    # BUT marked might escape the content inside.
    # Let's try the pure JS approach with custom renderer first, it's cleaner.

    # We need to ensure the mermaid diagrams are rendered div class="mermaid".
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeViz AI - Deep Dive</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max_width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9fafb;
        }}
        .container {{
            background: white;
            padding: 4rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        h1, h2, h3 {{ border-bottom: 1px solid #eaeaea; padding-bottom: 0.5rem; margin-top: 2rem; }}
        h1 {{ margin-top: 0; }}
        code {{ background-color: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.9em; font-family: 'Menlo', 'Monaco', 'Courier New', monospace; }}
        pre {{ background-color: #f3f4f6; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
        pre code {{ background-color: transparent; padding: 0; }}
        .mermaid {{ display: flex; justify-content: center; margin: 2rem 0; background: white; }}
        blockquote {{ border-left: 4px solid #3b82f6; margin: 1rem 0; padding: 0.5rem 1rem; color: #555; background-color: #eff6ff; border-radius: 4px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f3f4f6; }}
        img {{ max-width: 100%; }}
        .alert {{ padding: 1rem; border-radius: 4px; margin-bottom: 1rem; border: 1px solid transparent; }}
        .alert-info {{ color: #0c5460; background-color: #d1ecf1; border-color: #bee5eb; }}
        .alert-warning {{ color: #856404; background-color: #fff3cd; border-color: #ffeeba; }}
        .alert-important {{ color: #155724; background-color: #d4edda; border-color: #c3e6cb; }}
    </style>
</head>
<body>
    <div class="container" id="content"></div>

    <script>
        const markdownContent = {json.dumps(content)};

        // Configure marked
        const renderer = new marked.Renderer();
        
        // Override code block rendering
        renderer.code = function(code, language, escaped) {{
            if (language === 'mermaid') {{
                return '<div class="mermaid">' + code + '</div>';
            }}
            return '<pre><code class="language-' + language + '">' + code + '</code></pre>';
        }};

        // Parse markdown
        document.getElementById('content').innerHTML = marked.parse(markdownContent, {{ renderer: renderer }});

        // Initialize mermaid
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{ htmlLabels: true }}
        }});
    </script>
</body>
</html>
    """

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Successfully created {html_file}")

if __name__ == "__main__":
    convert_md_to_html("PROJECT_DEEP_DIVE.md", "PROJECT_DEEP_DIVE.html")
