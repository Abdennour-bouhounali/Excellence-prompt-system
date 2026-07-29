import os
import sys
from pathlib import Path
from notion_client import Client
from markdown_it import MarkdownIt

def parse_inline_to_rich_text(inline_token):
    """
    Parses a markdown-it inline token's children into Notion rich text objects.
    """
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

    for child in inline_token.children:
        if child.type == "text":
            if child.content:
                rich_text.append({
                    "type": "text",
                    "text": {"content": child.content},
                    "annotations": {k: v for k, v in current_styles.items() if v}
                })
        elif child.type == "code_inline":
            rich_text.append({
                "type": "text",
                "text": {"content": child.content},
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

    return rich_text

def markdown_to_notion_blocks(md_content):
    """
    Converts markdown string to Notion block structures.
    """
    md = MarkdownIt()
    tokens = md.parse(md_content)
    blocks = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.type == "heading_open":
            level = int(token.tag[1]) # h1, h2, h3
            inline_token = tokens[i + 1]
            rich_text = parse_inline_to_rich_text(inline_token)
            
            # Map level to Notion heading types (headings 1, 2, 3)
            heading_type = f"heading_{min(level, 3)}"
            blocks.append({
                "object": "block",
                "type": heading_type,
                heading_type: {
                    "rich_text": rich_text
                }
            })
            i += 3 # skip heading_open, inline, heading_close
            
        elif token.type == "paragraph_open":
            inline_token = tokens[i + 1]
            rich_text = parse_inline_to_rich_text(inline_token)
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": rich_text
                }
            })
            i += 3 # skip paragraph_open, inline, paragraph_close
            
        elif token.type == "bullet_list_open" or token.type == "ordered_list_open":
            list_type = "bulleted_list_item" if token.type == "bullet_list_open" else "numbered_list_item"
            i += 1
            # Parse list items
            while i < len(tokens) and tokens[i].type != token.type.replace("_open", "_close"):
                if tokens[i].type == "list_item_open":
                    i += 1
                    # List items can contain paragraphs or inline content directly
                    item_rich_text = []
                    while i < len(tokens) and tokens[i].type != "list_item_close":
                        sub_token = tokens[i]
                        if sub_token.type == "paragraph_open":
                            inline_token = tokens[i + 1]
                            item_rich_text.extend(parse_inline_to_rich_text(inline_token))
                            i += 3
                        elif sub_token.type == "inline":
                            item_rich_text.extend(parse_inline_to_rich_text(sub_token))
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
            i += 1 # skip close list token
            
        elif token.type == "fence":
            # Code block
            language = token.info if token.info else "plain text"
            # Notion expects specific language names, default to plain text or convert
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": token.content}
                    }],
                    "language": language.lower() if language else "plain text"
                }
            })
            i += 1
        else:
            i += 1
            
    return blocks

def get_child_pages(client, parent_id):
    """
    Returns a dictionary mapping titles to page IDs for direct child pages of parent_id.
    """
    results = {}
    cursor = None
    while True:
        response = client.blocks.children.list(block_id=parent_id, start_cursor=cursor)
        for block in response.get("results", []):
            if block.get("type") == "child_page":
                results[block["child_page"]["title"]] = block["id"]
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    return results

def delete_page_contents(client, page_id):
    """
    Deletes all block contents inside a page.
    """
    cursor = None
    while True:
        response = client.blocks.children.list(block_id=page_id, start_cursor=cursor)
        results = response.get("results", [])
        for block in results:
            client.blocks.delete(block_id=block["id"])
        if not response.get("has_more"):
            break
        # Since we are deleting, the next cursor changes or we can just query again starting from the beginning.
        # But to be safe, if we deleted everything in this page, we query again.
        # If no results were found, we stop.
        if not results:
            break

def upload_blocks_in_chunks(client, page_id, blocks):
    """
    Appends blocks to a page in chunks of 100 to stay within Notion's limits.
    """
    chunk_size = 100
    for i in range(0, len(blocks), chunk_size):
        chunk = blocks[i:i+chunk_size]
        client.blocks.children.append(block_id=page_id, children=chunk)

def main():
    notion_token = os.environ.get("NOTION_TOKEN")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE")
    
    if not notion_token or not parent_page_id:
        print("Error: NOTION_TOKEN and NOTION_PARENT_PAGE environment variables are required.")
        sys.exit(1)
        
    client = Client(auth=notion_token)
    docs_path = Path("docs")
    
    if not docs_path.exists():
        print(f"Error: {docs_path} directory does not exist.")
        sys.exit(1)
        
    for md_file in docs_path.rglob("*.md"):
        print(f"Processing {md_file}...")
        
        # Calculate parts relative to the docs folder
        relative_path = md_file.relative_to(docs_path)
        parts = list(relative_path.parent.parts)
        file_title = md_file.stem
        
        # 1. Resolve folder path structure in Notion
        current_parent_id = parent_page_id
        for folder_name in parts:
            children = get_child_pages(client, current_parent_id)
            if folder_name in children:
                current_parent_id = children[folder_name]
            else:
                print(f"Creating folder page: '{folder_name}' under parent {current_parent_id}")
                new_folder_page = client.pages.create(
                    parent={"page_id": current_parent_id},
                    properties={
                        "title": {
                            "title": [{"text": {"content": folder_name}}]
                        }
                    }
                )
                current_parent_id = new_folder_page["id"]
                
        # 2. Parse Markdown
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = markdown_to_notion_blocks(content)
        
        # 3. Create or Update Markdown File Page
        children = get_child_pages(client, current_parent_id)
        if file_title in children:
            page_id = children[file_title]
            print(f"Updating existing page '{file_title}' (ID: {page_id})...")
            delete_page_contents(client, page_id)
            upload_blocks_in_chunks(client, page_id, blocks)
        else:
            print(f"Creating new page '{file_title}'...")
            new_page = client.pages.create(
                parent={"page_id": current_parent_id},
                properties={
                    "title": {
                        "title": [{"text": {"content": file_title}}]
                    }
                },
                children=blocks[:100]
            )
            if len(blocks) > 100:
                upload_blocks_in_chunks(client, new_page["id"], blocks[100:])

if __name__ == "__main__":
    main()
