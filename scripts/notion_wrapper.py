import time
import random
from notion_client import Client
from notion_client.errors import APIResponseError
from logger import logger

def retry_on_failure(func):
    def wrapper(*args, **kwargs):
        backoffs = [1.0, 2.0, 4.0, 8.0, 16.0]
        for i, delay in enumerate(backoffs):
            try:
                return func(*args, **kwargs)
            except APIResponseError as e:
                is_retryable = e.status in (429, 500, 502, 503, 504)
                if not is_retryable:
                    raise e
                
                jitter = random.uniform(0.1, 0.5)
                sleep_time = delay + jitter
                logger.warning(
                    f"Notion API status {e.status} on {func.__name__}. "
                    f"Retrying in {sleep_time:.2f}s... (Attempt {i+1}/{len(backoffs)})"
                )
                time.sleep(sleep_time)
            except Exception as e:
                jitter = random.uniform(0.1, 0.5)
                sleep_time = delay + jitter
                logger.warning(
                    f"Connection error on {func.__name__}: {e}. "
                    f"Retrying in {sleep_time:.2f}s... (Attempt {i+1}/{len(backoffs)})"
                )
                time.sleep(sleep_time)
        return func(*args, **kwargs)
    return wrapper

class NotionClientWrapper:
    def __init__(self, token):
        self.client = Client(auth=token)
        
    @retry_on_failure
    def create_page(self, parent_id, title, children_blocks=None):
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }
        if children_blocks:
            payload["children"] = children_blocks
        return self.client.pages.create(**payload)
        
    @retry_on_failure
    def update_page_title(self, page_id, new_title):
        return self.client.pages.update(
            page_id=page_id,
            properties={
                "title": {
                    "title": [{"text": {"content": new_title}}]
                }
            }
        )

    @retry_on_failure
    def archive_page(self, page_id):
        return self.client.pages.update(page_id=page_id, archived=True)
        
    @retry_on_failure
    def retrieve_page(self, page_id):
        return self.client.pages.retrieve(page_id=page_id)

    @retry_on_failure
    def list_page_children(self, block_id, start_cursor=None):
        return self.client.blocks.children.list(block_id=block_id, start_cursor=start_cursor)

    @retry_on_failure
    def delete_block(self, block_id):
        return self.client.blocks.delete(block_id=block_id)
        
    @retry_on_failure
    def append_page_children(self, block_id, children):
        return self.client.blocks.children.append(block_id=block_id, children=children)

    def delete_all_page_contents(self, page_id):
        cursor = None
        while True:
            response = self.list_page_children(page_id, start_cursor=cursor)
            results = response.get("results", [])
            for block in results:
                try:
                    self.delete_block(block["id"])
                except Exception as e:
                    logger.warning(f"Failed to delete block {block['id']}: {e}")
            if not response.get("has_more"):
                break
            if not results:
                break
                
    def upload_blocks_chunked(self, page_id, blocks):
        chunk_size = 100
        for i in range(0, len(blocks), chunk_size):
            chunk = blocks[i:i+chunk_size]
            self.append_page_children(page_id, chunk)
            
    def get_child_pages_manual(self, parent_id):
        results = []
        cursor = None
        while True:
            response = self.list_page_children(parent_id, start_cursor=cursor)
            for block in response.get("results", []):
                if block.get("type") == "child_page":
                    results.append({
                        "id": block["id"],
                        "title": block["child_page"]["title"]
                    })
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        return results
