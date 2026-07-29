import json
from pathlib import Path
from datetime import datetime
from logger import logger

class SyncCache:
    CACHE_VERSION = 1
    
    def __init__(self, repository_name="Prompt System", cache_dir=".notion_sync"):
        self.repository_name = repository_name
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / "cache.json"
        self.data = self._create_empty_cache()
        
    def _create_empty_cache(self):
        return {
            "version": self.CACHE_VERSION,
            "repository": self.repository_name,
            "last_sync": None,
            "pages": {}
        }
        
    def load(self):
        if not self.cache_file.exists():
            logger.info("No cache file found. Starting fresh.")
            self.data = self._create_empty_cache()
            return
            
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                
            if loaded_data.get("version") != self.CACHE_VERSION:
                logger.warning(
                    f"Cache version mismatch (got {loaded_data.get('version')}, "
                    f"expected {self.CACHE_VERSION}). Resetting cache."
                )
                self.data = self._create_empty_cache()
            else:
                self.data = loaded_data
                logger.info(f"Loaded cache with {len(self.data['pages'])} entries.")
        except Exception as e:
            logger.error(f"Failed to load cache.json: {e}. Resetting cache.")
            self.data = self._create_empty_cache()
            
    def save(self):
        try:
            self.cache_dir.mkdir(exist_ok=True)
            self.data["last_sync"] = datetime.utcnow().isoformat() + "Z"
            
            # Temporary write to prevent corruption on crash
            temp_file = self.cache_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            temp_file.replace(self.cache_file)
            logger.info("Cache saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save cache.json: {e}")
            
    def clean(self):
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
                logger.info("Cache file removed.")
            except Exception as e:
                logger.error(f"Failed to remove cache: {e}")
                
    def get_page(self, path_str):
        return self.data["pages"].get(path_str)
        
    def set_page(self, path_str, page_id, parent_path, title, sha256=None, is_dir=False):
        self.data["pages"][path_str] = {
            "id": page_id,
            "parent": parent_path,
            "title": title,
            "sha256": sha256,
            "last_sync": datetime.utcnow().isoformat() + "Z",
            "is_dir": is_dir
        }
        
    def remove_page(self, path_str):
        if path_str in self.data["pages"]:
            del self.data["pages"][path_str]
            
    def list_pages(self):
        return self.data["pages"]
