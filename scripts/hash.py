import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from logger import logger

class HashManager:
    @staticmethod
    def calculate_file_sha256(filepath):
        sha = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    sha.update(chunk)
            return sha.hexdigest()
        except Exception as e:
            logger.error(f"Failed to hash file {filepath}: {e}")
            return None
            
    @classmethod
    def calculate_hashes_parallel(cls, filepaths, max_workers=8):
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {
                executor.submit(cls.calculate_file_sha256, path): path
                for path in filepaths
            }
            for future in future_to_path:
                path = future_to_path[future]
                h = future.result()
                if h:
                    results[str(path)] = h
        return results

    @staticmethod
    def detect_renames(local_files_with_hashes, cached_pages):
        """
        Detect renamed files based on content hashes.
        
        Args:
            local_files_with_hashes: dict { path_str: sha256 }
            cached_pages: dict { path_str: page_info }
            
        Returns:
            dict { old_path_str: new_path_str }
        """
        # Find local files not in cache (potential rename targets)
        untracked_locals = {
            path: h for path, h in local_files_with_hashes.items()
            if path not in cached_pages
        }
        
        # Find cached files that no longer exist locally (potential rename sources)
        missing_cached = {
            path: info for path, info in cached_pages.items()
            if path not in local_files_with_hashes and not info.get("is_dir")
        }
        
        renames = {}
        # Group missing cached files by hash
        hash_to_cached_paths = {}
        for path, info in missing_cached.items():
            h = info.get("sha256")
            if h:
                hash_to_cached_paths.setdefault(h, []).append(path)
                
        # Match untracked locals to missing cached files by hash
        for local_path, local_hash in untracked_locals.items():
            if local_hash in hash_to_cached_paths:
                candidate_paths = hash_to_cached_paths[local_hash]
                if candidate_paths:
                    # Match the first candidate
                    old_path = candidate_paths.pop(0)
                    renames[old_path] = local_path
                    logger.info(f"Rename detected: '{old_path}' -> '{local_path}' (hash: {local_hash})")
                    
        return renames
