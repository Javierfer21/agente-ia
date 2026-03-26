import markdown
import weasyprint


_CSS = """
@page {
    size: A4;
    margin: 2.5cm 2.2cm 2.5cm 2.2cm;
    @bottom-center {
        content: "Cloud Architecture Advisory — Informe confidencial";
        font-size: 8pt;
        color: #94a3b8;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 8pt;
        color: #94a3b8;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1e293b;
}

h1 {
    font-size: 22pt;
    font-weight: 700;
    color: #1d3557;
    border-bottom: 2.5px solid #1d3557;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 20px;
}

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #1d3557;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
}

h3 {
    font-size: 11.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 18px;
    margin-bottom: 8px;
}

h4 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 14px;
    margin-bottom: 6px;
}

p {
    margin: 0 0 10px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

th {
    background-color: #1d3557;
    color: white;
    padding: 9px 13px;
    text-align: left;
    font-weight: 600;
    font-size: 9pt;
}

td {
    padding: 7px 13px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

ul, ol {
    margin: 6px 0 10px 0;
    padding-left: 22px;
}

li {
    margin: 4px 0;
    line-height: 1.55;
}

code {
    background-color: #f1f5f9;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 9pt;
    font-family: 'Courier New', Courier, monospace;
    color: #0f172a;
}

pre {
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 12px 14px;
    font-size: 8.5pt;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap;
    word-break: break-word;
    margin: 12px 0;
}

blockquote {
    border-left: 3px solid #1d3557;
    margin: 12px 0;
    padding: 6px 16px;
    color: #475569;
    background-color: #f8fafc;
}

hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 22px 0;
}

strong {
    font-weight: 600;
    color: #0f172a;
}

em {
    color: #475569;
}

a {
    color: #1d3557;
    text-decoration: underline;
}
"""


def markdown_a_pdf(texto_markdown: str) -> bytes:
    """Convierte un texto en formato Markdown a bytes de un documento PDF."""
    html_body = markdown.markdown(
        texto_markdown,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )

    html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>{_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    return weasyprint.HTML(string=html_completo).write_pdf()
