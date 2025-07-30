from notion_client import Client
from notion_client.helpers import get_id

class NotionAPI:
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id
    
    def create_or_update_page(self, book_info, notes):
        """创建或更新Notion页面"""
        # 基本书籍信息
        properties = {
            "书名": {"title": [{"text": {"content": book_info.get("title", "未知书名")}}]},
            "作者": {"rich_text": [{"text": {"content": book_info.get("author", "未知作者")}}]},
            "进度": {"number": book_info.get("progress", 0)},
            "URL": {"url": book_info.get("infoUrl", "")}
        }
        
        # 查找是否已存在
        existing_page = self.find_page_by_book_id(book_info.get("bookId"))
        
        # 创建/更新页面
        if existing_page:
            page_id = existing_page["id"]
            self.notion.pages.update(
                page_id=page_id,
                properties=properties
            )
            print(f"🔄 更新书籍: {book_info['title']}")
        else:
            new_page = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            page_id = new_page["id"]
            print(f"✨ 创建新书籍: {book_info['title']}")
        
        # 添加笔记内容
        self.add_notes_to_page(page_id, notes)
        
        return {"id": page_id, "url": f"https://notion.so/{page_id.replace('-', '')}"}
    
    def find_page_by_book_id(self, book_id):
        """根据微信读书ID查找页面"""
        if not book_id:
            return None
            
        response = self.notion.databases.query(
            database_id=self.database_id,
            filter={
                "property": "微信读书ID",
                "rich_text": {
                    "equals": book_id
                }
            }
        )
        return response["results"][0] if response["results"] else None
    
    def add_notes_to_page(self, page_id, notes):
        """添加笔记到页面"""
        if not notes or not notes.get("updated"):
            return
            
        # 创建笔记内容
        children = []
        for chapter in notes["updated"]:
            # 添加章节标题
            if chapter.get("chapterTitle"):
                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": chapter["chapterTitle"]}
                        }]
                    }
                })
            
            # 添加笔记内容
            for item in chapter.get("bookmarkList", []):
                children.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": item.get("markText", "")}
                        }],
                        "icon": {"emoji": "📌"}
                    }
                })
        
        # 添加到页面
        if children:
            self.notion.blocks.children.append(
                block_id=page_id,
                children=children
            )
