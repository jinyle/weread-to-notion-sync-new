import os
import requests
import json

class WeReadAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Authorization': f'Bearer {self.token}',
            'Referer': 'https://weread.qq.com/'
        }
    
    def get_notebooks(self):
        """获取所有笔记本（包含书籍列表）"""
        url = "https://i.weread.qq.com/user/notebooks"
        return self._make_request(url)
    
    def get_book_info(self, book_id):
        """获取书籍详细信息"""
        url = f"https://i.weread.qq.com/book/info?bookId={book_id}"
        return self._make_request(url)
    
    def get_book_notes(self, book_id):
        """获取书籍笔记"""
        url = f"https://i.weread.qq.com/book/bookmarklist?bookId={book_id}"
        return self._make_request(url)
    
    def _make_request(self, url):
        """发送API请求"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise Exception("微信读书Token已失效，请重新获取")
            else:
                raise Exception(f"API请求失败: {response.status_code}")
        except Exception as e:
            print(f"请求失败: {str(e)}")
            return None
