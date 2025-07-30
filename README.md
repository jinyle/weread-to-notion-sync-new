# 微信读书到 Notion 同步工具

自动将微信读书的笔记和阅读进度同步到 Notion 数据库。

## 功能特点
- 自动同步微信读书的书籍列表
- 同步每本书的阅读进度
- 同步书籍笔记和书签
- 每日自动同步（通过 GitHub Actions）

## 设置指南

### 1. 获取微信读书 Token
1. 登录 [微信读书网页版](https://weread.qq.com)
2. 按 `F12` 打开开发者工具
3. 切换到 **Console** 标签
4. 输入以下代码并回车：
   ```javascript
   // 获取所有 Cookie
   const cookies = document.cookie.split(';');
   let token = '';
   for (let cookie of cookies) {
     if (cookie.includes('wr_skey=')) {
       token = cookie.split('wr_skey=')[1];
       break;
     }
     if (cookie.includes('wr_vid=')) {
       token = cookie.split('wr_vid=')[1];
       break;
     }
   }
   if (token) {
     console.log('✅ 请复制以下 Token 值:');
     console.log('\n' + token + '\n');
   } else {
     console.log('❌ 未找到有效 Token，请确认已登录');
   }
   ```
5. 复制输出的 Token 值

### 2. Notion 设置
1. 创建 Notion 集成：[https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 创建 Notion 数据库，包含以下字段：
   - **书名** (Title)
   - **作者** (Text)
   - **进度** (Number)
   - **微信读书ID** (Text)
   - **URL** (URL)
3. 复制数据库 ID（从 URL 中获取32位字符）

### 3. GitHub 设置
1. 在仓库的 **Settings > Secrets** 中添加：
   - `WR_TOKEN`: 微信读书 Token
   - `NOTION_TOKEN`: Notion 集成 Token
   - `DATABASE_ID`: Notion 数据库 ID
2. 手动触发同步：**Actions > Sync WeRead to Notion > Run workflow**

## 技术说明
- 每日自动同步（北京时间20:00）
- 使用 GitHub Actions 运行
- 安全存储凭证
