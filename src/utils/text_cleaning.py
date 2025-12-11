import re

def clear_text(text: str):
    
    text = re.split(r'\breferences\b|\bbibliography\b', text, flags=re.IGNORECASE)[0]
    text = re.sub(r'\$.*?\$|\[.*?\]', '', text)

    return (
        text.replace("\u200b", "")
            .replace("\t", " ")
            .replace("  ", " ")
            .strip()
    )
