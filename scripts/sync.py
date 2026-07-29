import os
import sys
import json
import hashlib
import fnmatch
from pathlib import Path
from notion_client import Client
from markdown_it import MarkdownIt

def load_config():
    config_path = Path("sync_config.json")
    if not config_path.exists():
        print("Error: sync_config.json not found.")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def should_sync(path_str, include_patterns, exclude_patterns):
    matched_include = False
    for pat in include_patterns:
        if pat.endswith("/**"):
            prefix = pat[:-3]
            if path_str.startswith(prefix + "/") or path_str == prefix:
                matched_include = True
                break
        elif fnmatch.fnmatch(path_str, pat):
            matched_include = True
            break
            
    if not matched_include:
        return False
        
    for pat in exclude_patterns:
        if pat.endswith("/**"):
            prefix = pat[:-3]
            if path_str.startswith(prefix + "/") or path_str == prefix:
                return False
        elif fnmatch.fnmatch(path_str, pat):
            return False
            
    return True

def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

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
    md = MarkdownIt()
    tokens = md.parse(md_content)
    blocks = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.type == "heading_open":
            level = int(token.tag[1])
            inline_token = tokens[i + 1]
            rich_text = parse_inline_to_rich_text(inline_token)
            
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
            rich_text = parse_inline_to_rich_text(inline_token)
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
            i += 1
            
        elif token.type == "fence":
            language = token.info if token.info else "plain text"
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

def make_metadata_block(path, sha256=None, is_dir=False):
    data = {
        "sync_metadata": {
            "path": str(path),
            "is_dir": is_dir
        }
    }
    if sha256:
        data["sync_metadata"]["sha256"] = sha256
        
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{
                "type": "text",
                "text": {"content": json.dumps(data, indent=2)}
            }],
            "language": "json"
        }
    }

def get_sync_metadata(client, page_id):
    try:
        response = client.blocks.children.list(block_id=page_id)
        for block in response.get("results", []):
            if block.get("type") == "code":
                code = block["code"]
                if code.get("language") == "json":
                    text_content = "".join([t["plain_text"] for t in code["rich_text"]])
                    data = json.loads(text_content)
                    if "sync_metadata" in data:
                        return block["id"], data["sync_metadata"]
    except Exception:
        pass
    return None, None

def scan_notion_tree(client, parent_id):
    managed_pages = {}
    to_visit = [parent_id]
    
    while to_visit:
        curr_id = to_visit.pop(0)
        cursor = None
        while True:
            response = client.blocks.children.list(block_id=curr_id, start_cursor=cursor)
            for block in response.get("results", []):
                if block.get("type") == "child_page":
                    child_id = block["id"]
                    meta_block_id, meta = get_sync_metadata(client, child_id)
                    if meta:
                        path = meta.get("path")
                        is_dir = meta.get("is_dir", False)
                        sha256 = meta.get("sha256")
                        managed_pages[path] = {
                            "id": child_id,
                            "is_dir": is_dir,
                            "sha256": sha256
                        }
                        if is_dir:
                            to_visit.append(child_id)
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
            
    return managed_pages

def delete_page_contents(client, page_id):
    cursor = None
    while True:
        response = client.blocks.children.list(block_id=page_id, start_cursor=cursor)
        results = response.get("results", [])
        for block in results:
            try:
                client.blocks.delete(block_id=block["id"])
            except Exception as e:
                print(f"Warning: failed to delete block {block['id']}: {e}")
        if not response.get("has_more"):
            break
        if not results:
            break

def upload_blocks_in_chunks(client, page_id, blocks):
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
    config = load_config()
    include_patterns = config.get("sync", [])
    exclude_patterns = config.get("ignore", [])
    
    # 1. Collect all local files and folder structures to sync
    local_files = {}
    local_dirs = set()
    
    for path in Path(".").rglob("*"):
        if path.is_file():
            # Get path relative to repo root
            rel_path = path.relative_to(".")
            path_str = str(rel_path)
            if should_sync(path_str, include_patterns, exclude_patterns):
                local_files[path_str] = {
                    "path": path,
                    "sha256": calculate_sha256(path)
                }
                # Track parent directories
                for parent in rel_path.parents:
                    if str(parent) != ".":
                        local_dirs.add(str(parent))
                        
    print(f"Scanned {len(local_files)} files and {len(local_dirs)} folders to sync.")
    
    # 2. Retrieve existing Notion managed tree
    print("Scanning Notion tree for managed pages...")
    managed_pages = scan_notion_tree(client, parent_page_id)
    print(f"Found {len(managed_pages)} managed pages in Notion.")
    
    # 3. Create/verify directories (bottom-up hierarchy sorting)
    sorted_dirs = sorted(list(local_dirs), key=lambda x: len(Path(x).parts))
    for dir_path in sorted_dirs:
        if dir_path in managed_pages:
            continue
            
        # Determine parent Notion ID
        p_path = Path(dir_path).parent
        parent_id = parent_page_id
        if str(p_path) != ".":
            parent_id = managed_pages[str(p_path)]["id"]
            
        dir_name = Path(dir_path).name
        print(f"Creating folder page: '{dir_name}' (Path: {dir_path})")
        meta_block = make_metadata_block(dir_path, is_dir=True)
        new_folder = client.pages.create(
            parent={"page_id": parent_id},
            properties={
                "title": {
                    "title": [{"text": {"content": dir_name}}]
                }
            },
            children=[meta_block]
        )
        managed_pages[dir_path] = {
            "id": new_folder["id"],
            "is_dir": True,
            "sha256": None
        }
        
    # 4. Sync files
    for path_str, file_info in local_files.items():
        filepath = file_info["path"]
        local_hash = file_info["sha256"]
        file_title = filepath.stem
        
        # Parse content blocks
        if filepath.suffix.lower() == ".md":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = markdown_to_notion_blocks(content)
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Default HTML to html language, otherwise plain text
            lang = "html" if filepath.suffix.lower() == ".html" else "plain text"
            blocks = plain_text_to_notion_blocks(content, lang)
            
        # Insert metadata block at the beginning of blocks list
        meta_block = make_metadata_block(path_str, sha256=local_hash, is_dir=False)
        blocks.insert(0, meta_block)
        
        if path_str in managed_pages:
            notion_info = managed_pages[path_str]
            page_id = notion_info["id"]
            remote_hash = notion_info["sha256"]
            
            if remote_hash == local_hash:
                print(f"Skipping '{path_str}' (No changes detected).")
                continue
                
            print(f"Updating '{path_str}'...")
            delete_page_contents(client, page_id)
            upload_blocks_in_chunks(client, page_id, blocks)
        else:
            p_path = Path(path_str).parent
            parent_id = parent_page_id
            if str(p_path) != ".":
                parent_id = managed_pages[str(p_path)]["id"]
                
            print(f"Creating new page '{file_title}' (Path: {path_str})...")
            new_page = client.pages.create(
                parent={"page_id": parent_id},
                properties={
                    "title": {
                        "title": [{"text": {"content": file_title}}]
                    }
                },
                children=blocks[:100]
            )
            if len(blocks) > 100:
                upload_blocks_in_chunks(client, new_page["id"], blocks[100:])
                
    # 5. Archive removed files/folders
    for path_str, notion_info in managed_pages.items():
        # If it's a directory, check if it's still needed
        if notion_info["is_dir"]:
            if path_str not in local_dirs:
                print(f"Archiving folder '{path_str}' (deleted locally)...")
                client.pages.update(page_id=notion_info["id"], archived=True)
        else:
            if path_str not in local_files:
                print(f"Archiving file page '{path_str}' (deleted locally)...")
                client.pages.update(page_id=notion_info["id"], archived=True)

if __name__ == "__main__":
    main()
