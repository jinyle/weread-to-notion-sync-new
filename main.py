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
        
        print(f"获取到 {len(notebooks['books'])} 本书")
        
        # 同步每本书（这里只同步前3本作为测试）
        for i, book in enumerate(notebooks['books'][:3]):
            book_id = book['bookId']
            print(f"\n📖 [{i+1}/3] 同步书籍: {book['title']} ({book_id})")
            
            # 获取书籍详情
            book_info = weread.get_book_info(book_id)
            if not book_info:
                print(f"⚠️ 获取书籍详情失败，跳过")
                continue
                
            # 获取笔记
            notes = weread.get_book_notes(book_id)
            if not notes:
                print("⚠️ 未获取到笔记，跳过")
                continue
                
            # 同步到Notion
            notion_page = notion.create_or_update_page(book_info, notes)
            print(f"✅ 已同步到Notion: {notion_page['url']}")
            
            # 避免请求过快
            time.sleep(1)
        
        print("\n🎉 测试同步完成！")
        
    except Exception as e:
        print(f"❌ 同步失败: {str(e)}")
        raise

if __name__ == "__main__":
    main()
