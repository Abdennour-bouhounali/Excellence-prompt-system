#!/usr/bin/env python3
import os
import sys
import argparse
from logger import logger
from sync_engine import SyncEngine
from cache import SyncCache

def main():
    parser = argparse.ArgumentParser(
        description="Production-grade Notion Markdown Sync Engine."
    )
    parser.add_argument(
        "command",
        choices=["sync", "dry-run", "verify", "rebuild-cache", "clean", "force"],
        help="Command to execute."
    )
    
    args = parser.parse_args()
    
    # "clean" command does not require Notion API tokens
    if args.command == "clean":
        cache = SyncCache()
        cache.clean()
        sys.exit(0)
        
    notion_token = os.environ.get("NOTION_TOKEN")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE")
    
    if not notion_token or not parent_page_id:
        logger.error("NOTION_TOKEN and NOTION_PARENT_PAGE environment variables are required.")
        sys.exit(1)
        
    dry_run = (args.command == "dry-run")
    force = (args.command == "force")
    
    engine = SyncEngine(
        notion_token=notion_token,
        parent_page_id=parent_page_id,
        dry_run=dry_run,
        force=force
    )
    
    success = False
    if args.command in ("sync", "dry-run", "force"):
        success = engine.sync()
    elif args.command == "verify":
        success = engine.verify()
    elif args.command == "rebuild-cache":
        success = engine.rebuild_cache()
        
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
