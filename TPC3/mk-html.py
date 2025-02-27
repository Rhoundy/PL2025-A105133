import re, sys

def title_to_header(match):
    print(match)
    level = len(match.group(1))
    content = match.group(2).strip()
    return f"<h{level}>{content}</h{level}>"

def list_to_html(match):
    list_block = match.group(1).strip()
    items = re.findall(r'^\d+\.\s+(.+)', list_block, flags=re.MULTILINE)
    
    html_list = "<ol>\n"
    for item in items:
        html_list += f"  <li>{item}</li>\n"
    html_list += "</ol>"
    
    return html_list

def image_to_html(match):
    alt_text = match.group(1).strip()
    img_url = match.group(2).strip()
    return f'<img src="{img_url}" alt="{alt_text}"/>'

def link_to_html(match):
    text = match.group(1).strip()
    url = match.group(2).strip()
    return f'<a href="{url}">{text}</a>'


def markdown_to_html(file):
    with open(file, "r", encoding="utf-8") as f:
        markdown_text = f.read()
        print(f'Before: {markdown_text}')

    markdown_text = re.sub(r'(#{1,3})\s+(.+)$', title_to_header, markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(r'(^\d+\. +(.+)(?:\n\d+\. +(.+))*)', list_to_html, markdown_text, flags=re.MULTILINE)

    markdown_text = re.sub(r'(?:^|[^*])\*([^*]+)\*(?:[^*]|$)', r'<i>\1</i>', markdown_text)

    markdown_text = re.sub(r'(?:^|[^*])\*\*([^*]+)\*\*(?:[^*]|$)', r'<b>\1</b>', markdown_text)

    markdown_text = re.sub(r'!\[(.+)\]\((.+)\)',image_to_html, markdown_text)

    markdown_text = re.sub(r'\[(.+)\]\((.+)\)',link_to_html, markdown_text)

    return markdown_text

if __name__ == '__main__':
    file = sys.argv[1]
    print(f'After: {markdown_to_html(file)}')
    