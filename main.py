import os
import time
from weread_api import WeReadAPI
from notion_api import NotionAPI

def main():
    print("🚀 启动微信读书到 Notion 同步")
    
    # 获取环境变量
    wr_token = os.getenv('WR_TOKEN')
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('DATABASE_ID')
    
    if not wr_token or not notion_token or not database_id:
        print("❌ 缺少必要的环境变量")
        print(f"WR_TOKEN: {bool(wr_token)}")
        print(f"NOTION_TOKEN: {bool(notion_token)}")
        print(f"DATABASE_ID: {bool(database_id)}")
        return
    
    try:
        # 初始化API
        weread = WeReadAPI(wr_token)
        notion = NotionAPI(notion_token, database_id)
        
        # 获取微信读书数据
        print("📚 获取微信读书笔记本列表...")
        notebooks = weread.get_notebooks()
        
        if not notebooks or 'books' not in notebooks:
            print("⚠️ 未获取到笔记本数据，请检查Token是否有效")
            return
        
        # 同步每本书
        for book in notebooks['books']:
            book_id = book['bookId']
            print(f"\n📖 同步书籍: {book['title']} ({book_id})")
            
            # 获取书籍详情
            book_info = weread.get_book_info(book_id)
            
            # 获取笔记
            notes = weread.get_book_notes(book_id)
            
            # 同步到Notion
            notion_page = notion.create_or_update_page(book_info, notes)
            print(f"✅ 已同步到Notion: {notion_page['url']}")
            
            # 避免请求过快
            time.sleep(1)
        
        print("\n🎉 同步完成！共同步 {} 本书".format(len(notebooks['books'])))
        
    except Exception as e:
        print(f"❌ 同步失败: {str(e)}")
        raise

if __name__ == "__main__":
    main()
