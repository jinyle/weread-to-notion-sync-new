import requests
import json

class WeReadAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Referer': 'https://weread.qq.com/',
            'Host': 'i.weread.qq.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*'
        }
        
        # 动态设置认证头
        if self.token:
            if self.token.startswith('wr_'):
                # 如果是类似 cookie 的 token
                self.headers['Cookie'] = f'wr_skey={self.token}'
            else:
                # 如果是 Bearer token
                self.headers['Authorization'] = f'Bearer {self.token}'
    
    def get_notebooks(self):
        """获取所有笔记本（包含书籍列表）"""
        return self._make_request("https://i.weread.qq.com/user/notebooks")
    
    def get_book_info(self, book_id):
        """获取书籍详细信息"""
        return self._make_request(f"https://i.weread.qq.com/book/info?bookId={book_id}")
    
    def get_book_notes(self, book_id):
        """获取书籍笔记"""
        return self._make_request(f"https://i.weread.qq.com/book/bookmarklist?bookId={book_id}")
    
    def _make_request(self, url):
        """发送API请求"""
        try:
            response = requests.get(
                url, 
                headers=self.headers,
                timeout=10,
                # 添加模拟浏览器行为的参数
                params={'_t': int(time.time() * 1000)}  # 添加时间戳避免缓存
            )
            
            # 打印请求详情用于调试
            print(f"请求 URL: {url}")
            print(f"请求头: {json.dumps(self.headers, indent=2, ensure_ascii=False)}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    print(f"❌ API错误响应: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                    
                    # 特定错误处理
                    if error_data.get('errcode') == -2010:
                        print("错误原因: 用户认证失败，请检查Token是否有效")
                except:
                    print(f"❌ 非JSON响应: {response.text[:200]}...")
                
                return None
        except Exception as e:
            print(f"⚠️ 请求异常: {str(e)}")
            return None
