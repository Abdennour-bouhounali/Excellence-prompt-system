import fnmatch
from pathlib import Path
from logger import logger

class RepositoryScanner:
    def __init__(self, config_data):
        self.include_patterns = config_data.get("sync", [])
        self.exclude_patterns = config_data.get("ignore", [])
        
    def should_sync(self, path_str):
        matched_include = False
        for pat in self.include_patterns:
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
            
        for pat in self.exclude_patterns:
            if pat.endswith("/**"):
                prefix = pat[:-3]
                if path_str.startswith(prefix + "/") or path_str == prefix:
                    return False
            elif fnmatch.fnmatch(path_str, pat):
                return False
                
        return True

    def scan(self, root_dir="."):
        root_path = Path(root_dir)
        local_files = []
        local_dirs = set()
        
        for path in root_path.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(root_path)
                path_str = str(rel_path)
                
                # Normalize windows separators to forward slashes
                path_str = path_str.replace("\\", "/")
                
                if self.should_sync(path_str):
                    local_files.append(rel_path)
                    
                    # Track parent directories
                    for parent in rel_path.parents:
                        if str(parent) != ".":
                            normalized_parent = str(parent).replace("\\", "/")
                            local_dirs.add(normalized_parent)
                            
        return local_files, local_dirs
