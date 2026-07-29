import os
from pathlib import Path
from logger import logger
from cache import SyncCache
from hash import HashManager
from scanner import RepositoryScanner
from notion_wrapper import NotionClientWrapper
from markdown_converter import MarkdownConverter

class SyncEngine:
    def __init__(self, notion_token, parent_page_id, dry_run=False, force=False):
        self.client = NotionClientWrapper(notion_token)
        self.parent_page_id = parent_page_id
        self.dry_run = dry_run
        self.force = force
        self.cache = SyncCache()
        self.cache.load()
        
    def _get_parent_id(self, path_str, cached_pages):
        p_path = str(Path(path_str).parent).replace("\\", "/")
        if p_path == "." or p_path == "":
            return self.parent_page_id
        if p_path in cached_pages:
            return cached_pages[p_path]["id"]
        return self.parent_page_id

    def sync(self):
        config_data = {}
        try:
            import json
            with open("sync_config.json", "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load sync_config.json: {e}")
            return False

        scanner = RepositoryScanner(config_data)
        local_files, local_dirs = scanner.scan()
        
        # Calculate local hashes in parallel
        logger.info("Computing hashes for local files...")
        local_filepaths = [Path(f) for f in local_files]
        local_hashes = HashManager.calculate_hashes_parallel(local_filepaths)
        
        cached_pages = self.cache.list_pages()
        
        # 1. Rename Detection
        renames = HashManager.detect_renames(local_hashes, cached_pages)
        for old_path, new_path in renames.items():
            page_info = cached_pages[old_path]
            page_id = page_info["id"]
            new_title = Path(new_path).stem
            
            if self.dry_run:
                logger.info(f"[DRY-RUN] Rename page title '{page_info['title']}' -> '{new_title}' (Path: {old_path} -> {new_path})")
            else:
                logger.info(f"Renaming Notion page title to '{new_title}' for path '{new_path}'")
                self.client.update_page_title(page_id, new_title)
                
            # Update cache key
            self.cache.set_page(
                path_str=new_path,
                page_id=page_id,
                parent_path=str(Path(new_path).parent).replace("\\", "/"),
                title=new_title,
                sha256=page_info["sha256"],
                is_dir=False
            )
            self.cache.remove_page(old_path)
            
        # Refresh cached_pages after renames
        cached_pages = self.cache.list_pages()
        
        # 2. Sync Directories
        sorted_dirs = sorted(list(local_dirs), key=lambda x: len(Path(x).parts))
        for dir_path in sorted_dirs:
            dir_name = Path(dir_path).name
            if dir_path in cached_pages:
                continue
                
            parent_id = self._get_parent_id(dir_path, cached_pages)
            if self.dry_run:
                logger.info(f"[DRY-RUN] + create folder '{dir_name}' (Path: {dir_path})")
                # Add mock entry for child parent resolution in dry run
                cached_pages[dir_path] = {"id": "mock_folder_id", "is_dir": True}
            else:
                logger.info(f"Creating folder page: '{dir_name}' (Path: {dir_path})")
                new_folder = self.client.create_page(parent_id, dir_name)
                self.cache.set_page(
                    path_str=dir_path,
                    page_id=new_folder["id"],
                    parent_path=str(Path(dir_path).parent).replace("\\", "/"),
                    title=dir_name,
                    sha256=None,
                    is_dir=True
                )
                
        # Refresh cached_pages
        cached_pages = self.cache.list_pages()
        
        # 3. Sync Files
        for path_str in sorted(local_files):
            filepath = Path(path_str)
            local_hash = local_hashes.get(path_str)
            file_title = filepath.stem
            
            # Read content and convert
            if filepath.suffix.lower() == ".md":
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = MarkdownConverter.to_notion_blocks(content)
            else:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                lang = "html" if filepath.suffix.lower() == ".html" else "plain text"
                blocks = MarkdownConverter.plain_text_to_notion_blocks(content, lang)
                
            if path_str in cached_pages:
                page_info = cached_pages[path_str]
                page_id = page_info["id"]
                remote_hash = page_info["sha256"]
                
                if remote_hash == local_hash and not self.force:
                    logger.info(f"0 skipped '{path_str}'")
                    continue
                    
                if self.dry_run:
                    logger.info(f"[DRY-RUN] + update file '{file_title}' (Path: {path_str})")
                else:
                    logger.info(f"Updating page '{file_title}' (Path: {path_str})...")
                    self.client.delete_all_page_contents(page_id)
                    self.client.upload_blocks_chunked(page_id, blocks)
                    self.cache.set_page(
                        path_str=path_str,
                        page_id=page_id,
                        parent_path=str(filepath.parent).replace("\\", "/"),
                        title=file_title,
                        sha256=local_hash,
                        is_dir=False
                    )
            else:
                parent_id = self._get_parent_id(path_str, cached_pages)
                if self.dry_run:
                    logger.info(f"[DRY-RUN] + create file '{file_title}' (Path: {path_str})")
                else:
                    logger.info(f"Creating page '{file_title}' (Path: {path_str})...")
                    new_page = self.client.create_page(parent_id, file_title, blocks[:100])
                    if len(blocks) > 100:
                        self.client.upload_blocks_chunked(new_page["id"], blocks[100:])
                    self.cache.set_page(
                        path_str=path_str,
                        page_id=new_page["id"],
                        parent_path=str(filepath.parent).replace("\\", "/"),
                        title=file_title,
                        sha256=local_hash,
                        is_dir=False
                    )
                    
        # 4. Archive removed files/folders
        # Refresh cached_pages
        cached_pages = self.cache.list_pages()
        paths_to_remove = []
        
        # Sort keys to archive files before parent folders
        for path_str in sorted(cached_pages.keys(), key=lambda x: len(Path(x).parts), reverse=True):
            page_info = cached_pages[path_str]
            is_dir = page_info["is_dir"]
            
            should_archive = False
            if is_dir:
                if path_str not in local_dirs:
                    should_archive = True
            else:
                if path_str not in local_files:
                    should_archive = True
                    
            if should_archive:
                if self.dry_run:
                    logger.info(f"[DRY-RUN] - archive {'folder' if is_dir else 'file'} '{path_str}'")
                else:
                    logger.info(f"Archiving {'folder' if is_dir else 'file'} '{path_str}'...")
                    try:
                        self.client.archive_page(page_info["id"])
                    except Exception as e:
                        logger.error(f"Failed to archive page {page_info['id']}: {e}")
                paths_to_remove.append(path_str)
                
        if not self.dry_run:
            for p in paths_to_remove:
                self.cache.remove_page(p)
            self.cache.save()
            
        logger.info("Sync complete.")
        return True

    def verify(self):
        cached_pages = self.cache.list_pages()
        logger.info(f"Verifying {len(cached_pages)} cached pages...")
        errors = 0
        
        for path_str, page_info in cached_pages.items():
            page_id = page_info["id"]
            try:
                page = self.client.retrieve_page(page_id)
                if page.get("archived"):
                    logger.error(f"Page '{path_str}' (ID: {page_id}) is archived in Notion but in cache.")
                    errors += 1
                else:
                    logger.info(f"Verified: '{path_str}' matches Notion page ID: {page_id}")
            except Exception as e:
                logger.error(f"Failed to verify page '{path_str}' (ID: {page_id}): {e}")
                errors += 1
                
        if errors == 0:
            logger.info("Verification SUCCESS: All cache entries match active pages in Notion.")
            return True
        else:
            logger.error(f"Verification FAILED: Found {errors} inconsistencies.")
            return False

    def rebuild_cache(self):
        logger.info("Starting cache rebuild recovery process...")
        new_pages = {}
        
        # Load local files to help map Notion titles to exact repo paths
        config_data = {}
        try:
            import json
            with open("sync_config.json", "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load sync_config.json: {e}")
            return False
            
        scanner = RepositoryScanner(config_data)
        local_files, local_dirs = scanner.scan()
        local_filepaths = [Path(f) for f in local_files]
        local_hashes = HashManager.calculate_hashes_parallel(local_filepaths)
        
        # We walk the Notion tree starting from the parent root page
        to_visit = [("", self.parent_page_id)] # (relative_path_prefix, notion_page_id)
        
        while to_visit:
            prefix, parent_id = to_visit.pop(0)
            child_pages = self.client.get_child_pages_manual(parent_id)
            
            for child in child_pages:
                child_id = child["id"]
                title = child["title"]
                
                # Try to map this child page to a local directory or file
                mapped_path = None
                is_dir = False
                
                # Check directories
                for d in local_dirs:
                    d_path = Path(d)
                    expected_prefix = str(d_path.parent).replace("\\", "/")
                    if (expected_prefix == prefix or (prefix == "" and expected_prefix == ".")) and d_path.name == title:
                        mapped_path = d
                        is_dir = True
                        break
                        
                # Check files if not mapped to a directory
                if not mapped_path:
                    for f in local_files:
                        f_path = Path(f)
                        expected_prefix = str(f_path.parent).replace("\\", "/")
                        if (expected_prefix == prefix or (prefix == "" and expected_prefix == ".")) and f_path.stem == title:
                            mapped_path = str(f).replace("\\", "/")
                            is_dir = False
                            break
                            
                if mapped_path:
                    logger.info(f"Rebuilt cache entry: '{mapped_path}' -> Notion ID {child_id}")
                    sha256 = local_hashes.get(mapped_path) if not is_dir else None
                    new_pages[mapped_path] = {
                        "id": child_id,
                        "parent": str(Path(mapped_path).parent).replace("\\", "/"),
                        "title": title,
                        "sha256": sha256,
                        "last_sync": "",
                        "is_dir": is_dir
                    }
                    if is_dir:
                        to_visit.append((mapped_path, child_id))
                else:
                    logger.warning(f"Unrecognized Notion page '{title}' under path '{prefix or '[root]'}'. Skipping.")
                    
        self.cache.data["pages"] = new_pages
        self.cache.save()
        logger.info("Cache rebuild complete.")
        return True
