import json
from markdown_it import MarkdownIt

class MarkdownConverter:
    @staticmethod
    def parse_inline_to_rich_text(inline_token):
        rich_text = []
        if not inline_token.children:
            if inline_token.content:
                rich_text.append({
                    "type": "text",
                    "text": {"content": inline_token.content}
                })
            return rich_text

        current_styles = {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False
        }
        current_link = None

        for child in inline_token.children:
            if child.type == "text":
                if child.content:
                    text_obj = {
                        "content": child.content
                    }
                    if current_link:
                        text_obj["link"] = {"url": current_link}
                        
                    rich_text.append({
                        "type": "text",
                        "text": text_obj,
                        "annotations": {k: v for k, v in current_styles.items() if v}
                    })
            elif child.type == "code_inline":
                text_obj = {
                    "content": child.content
                }
                if current_link:
                    text_obj["link"] = {"url": current_link}
                    
                rich_text.append({
                    "type": "text",
                    "text": text_obj,
                    "annotations": {**{k: v for k, v in current_styles.items() if v}, "code": True}
                })
            elif child.type == "strong_open":
                current_styles["bold"] = True
            elif child.type == "strong_close":
                current_styles["bold"] = False
            elif child.type == "em_open":
                current_styles["italic"] = True
            elif child.type == "em_close":
                current_styles["italic"] = False
            elif child.type == "s_open":
                current_styles["strikethrough"] = True
            elif child.type == "s_close":
                current_styles["strikethrough"] = False
            elif child.type == "link_open":
                if child.attrs:
                    attrs_dict = dict(child.attrs) if isinstance(child.attrs, list) else child.attrs
                    current_link = attrs_dict.get("href")
            elif child.type == "link_close":
                current_link = None
            elif child.type == "image":
                # Handle inline images or link fallback
                if child.attrs:
                    attrs_dict = dict(child.attrs) if isinstance(child.attrs, list) else child.attrs
                    src = attrs_dict.get("src", "")
                    alt = child.content or "image"
                    text_obj = {
                        "content": f"[Image: {alt}]({src})"
                    }
                    rich_text.append({
                        "type": "text",
                        "text": text_obj,
                        "annotations": {"italic": True}
                    })

        return rich_text

    @classmethod
    def to_notion_blocks(cls, md_content):
        # Enable GFM features like tables
        md = MarkdownIt().enable("table")
        tokens = md.parse(md_content)
        blocks = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == "heading_open":
                level = int(token.tag[1])
                inline_token = tokens[i + 1]
                rich_text = cls.parse_inline_to_rich_text(inline_token)
                
                heading_type = f"heading_{min(level, 3)}"
                blocks.append({
                    "object": "block",
                    "type": heading_type,
                    heading_type: {
                        "rich_text": rich_text
                    }
                })
                i += 3
                
            elif token.type == "paragraph_open":
                inline_token = tokens[i + 1]
                # Check for image only inside paragraph
                if inline_token.children and len(inline_token.children) == 1 and inline_token.children[0].type == "image":
                    img_child = inline_token.children[0]
                    attrs_dict = dict(img_child.attrs) if isinstance(img_child.attrs, list) else img_child.attrs
                    src = attrs_dict.get("src", "")
                    blocks.append({
                        "object": "block",
                        "type": "image",
                        "image": {
                            "type": "external",
                            "external": {
                                "url": src
                            }
                        }
                    })
                else:
                    rich_text = cls.parse_inline_to_rich_text(inline_token)
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": rich_text
                        }
                    })
                i += 3
                
            elif token.type == "bullet_list_open" or token.type == "ordered_list_open":
                list_type = "bulleted_list_item" if token.type == "bullet_list_open" else "numbered_list_item"
                i += 1
                while i < len(tokens) and tokens[i].type != token.type.replace("_open", "_close"):
                    if tokens[i].type == "list_item_open":
                        i += 1
                        item_rich_text = []
                        while i < len(tokens) and tokens[i].type != "list_item_close":
                            sub_token = tokens[i]
                            if sub_token.type == "paragraph_open":
                                inline_token = tokens[i + 1]
                                item_rich_text.extend(cls.parse_inline_to_rich_text(inline_token))
                                i += 3
                            elif sub_token.type == "inline":
                                item_rich_text.extend(cls.parse_inline_to_rich_text(sub_token))
                                i += 1
                            else:
                                i += 1
                        blocks.append({
                            "object": "block",
                            "type": list_type,
                            list_type: {
                                "rich_text": item_rich_text
                            }
                        })
                    else:
                        i += 1
                i += 1
                
            elif token.type == "fence":
                language = token.info if token.info else "plain text"
                # Map common markdown extensions to Notion-supported languages
                lang_mapping = {
                    "js": "javascript",
                    "ts": "typescript",
                    "py": "python",
                    "sh": "shell",
                    "bash": "bash",
                    "json": "json",
                    "html": "html",
                    "css": "css"
                }
                lang_clean = lang_mapping.get(language.lower(), language.lower())
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": token.content}
                        }],
                        "language": lang_clean if lang_clean else "plain text"
                    }
                })
                i += 1
                
            elif token.type == "blockquote_open":
                # Collect paragraph/inline inside blockquote
                i += 1
                quote_rich_text = []
                while i < len(tokens) and tokens[i].type != "blockquote_close":
                    sub_token = tokens[i]
                    if sub_token.type == "paragraph_open":
                        inline_token = tokens[i + 1]
                        quote_rich_text.extend(cls.parse_inline_to_rich_text(inline_token))
                        i += 3
                    elif sub_token.type == "inline":
                        quote_rich_text.extend(cls.parse_inline_to_rich_text(sub_token))
                        i += 1
                    else:
                        i += 1
                blocks.append({
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": quote_rich_text
                    }
                })
                i += 1
                
            elif token.type == "hr":
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
                i += 1
                
            elif token.type == "table_open":
                # Parse simple table
                table_rows = []
                headers = []
                i += 1
                while i < len(tokens) and tokens[i].type != "table_close":
                    sub_token = tokens[i]
                    if sub_token.type == "tr_open":
                        i += 1
                        cells = []
                        while i < len(tokens) and tokens[i].type != "tr_close":
                            cell_token = tokens[i]
                            if cell_token.type in ("th_open", "td_open"):
                                is_head = cell_token.type == "th_open"
                                i += 1
                                cell_rich_text = []
                                while i < len(tokens) and tokens[i].type not in ("th_close", "td_close"):
                                    if tokens[i].type == "inline":
                                        cell_rich_text.extend(cls.parse_inline_to_rich_text(tokens[i]))
                                    i += 1
                                cells.append(cell_rich_text)
                                if is_head:
                                    headers.append(True)
                            i += 1
                        table_rows.append(cells)
                    i += 1
                    
                if table_rows:
                    width = len(table_rows[0])
                    has_header = bool(headers)
                    # Convert to table block
                    table_children = []
                    for row in table_rows:
                        # Make sure row matches width
                        row_cells = row + [[]] * (width - len(row))
                        table_children.append({
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": row_cells
                            }
                        })
                    
                    blocks.append({
                        "object": "block",
                        "type": "table",
                        "table": {
                            "table_width": width,
                            "has_column_header": has_header,
                            "has_row_header": False,
                            "children": table_children
                        }
                    })
                i += 1
            else:
                i += 1
                
        return blocks

    @staticmethod
    def plain_text_to_notion_blocks(content, language="plain text"):
        rich_text = []
        chunk_size = 2000
        for i in range(0, len(content), chunk_size):
            rich_text.append({
                "type": "text",
                "text": {"content": content[i:i+chunk_size]}
            })
        return [{
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": rich_text,
                "language": language
            }
        }]
