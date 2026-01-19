# Page Maker - 使用指南 / Usage Guide

## 快速开始 / Quick Start

### 方式1: 使用图形界面 (GUI)

运行主程序：
```bash
python3 page_maker.py
# 或者
python3 run.py
```

使用步骤：
1. 从下拉菜单选择一个模板
2. 点击"加载模板"按钮
3. 在显示的输入框中编辑内容（保留默认值或输入新内容）
4. 输入要保存的文件名
5. 点击"完成 - 生成HTML文件"按钮

生成的文件保存在 `output/` 目录中。

### 方式2: 运行演示脚本

查看自动生成的示例：
```bash
python3 demo.py
```

这会生成三个示例HTML文件：
- `output/demo_blog_post.html` - 博客文章示例
- `output/demo_article.html` - 简单文章示例  
- `output/demo_tech_note.html` - 技术笔记示例

### 方式3: 编程方式使用

```python
from html_utils import PTagParser, replace_content_safe
import os

# 读取模板
template_path = 'templates/blog_post.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# 解析模板找到可编辑字段
parser = PTagParser()
parser.feed(template)

# 替换内容
result = template
result = replace_content_safe(result, 'title', '我的标题')
result = replace_content_safe(result, 'content-main', '文章内容...')

# 保存
with open('output/my_page.html', 'w', encoding='utf-8') as f:
    f.write(result)
```

## 模板说明

### 可编辑区域

模板中的可编辑区域使用以下格式标记：
```html
<p class="unique-class-name">默认内容</p>
```

**重要事项：**
- 每个 class 名称应该是唯一的
- 只有 `<p>` 标签带 class 属性的才会被识别
- 默认内容会显示在输入框中

### 现有模板

#### 1. blog_post.html - 博客文章模板
可编辑字段：
- `title` - 博客标题
- `author` - 作者
- `date` - 日期
- `content-main` - 主要内容

#### 2. simple_article.html - 简单文章模板
可编辑字段：
- `heading` - 标题
- `subtitle-text` - 副标题
- `paragraph1` - 第一段
- `paragraph2` - 第二段

#### 3. tech_note.html - 技术笔记模板
可编辑字段：
- `note-title` - 笔记标题
- `note-desc` - 描述/标签
- `problem` - 问题描述
- `solution` - 解决方案
- `summary` - 总结

## 创建自定义模板

1. 在 `templates/` 目录创建新的 HTML 文件
2. 使用 `<p class="field-name">默认值</p>` 标记可编辑区域
3. 保存文件
4. 重新运行程序，新模板会自动出现在列表中

### 模板示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的模板</title>
    <style>
        body { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <h1><p class="page-title">页面标题</p></h1>
    <p class="intro">这是引言部分</p>
    <div class="content">
        <p class="main-text">主要内容区域</p>
    </div>
</body>
</html>
```

## 安全提示

- 默认情况下，用户输入会被自动转义以防止XSS攻击
- 特殊字符（`<`, `>`, `&`, `"`）会被转换为HTML实体
- 如果需要插入原始HTML，可以修改 `html_utils.py` 中的 `escape_html` 参数

## 故障排除

### 问题：GUI 无法启动
**原因：** 没有图形显示环境（如SSH连接）  
**解决：** 使用 `demo.py` 或编程方式生成HTML

### 问题：找不到模板
**原因：** `templates/` 目录不存在或为空  
**解决：** 确保 `templates/` 目录存在且包含 `.html` 文件

### 问题：生成的文件覆盖了旧文件
**原因：** 使用了相同的文件名  
**解决：** 每次使用不同的文件名，或备份重要文件

### 问题：模板中的某些标签未被识别
**原因：** 只有 `<p class="...">` 标签会被识别  
**解决：** 确保可编辑区域使用正确的格式

## 测试

运行测试以验证安装：
```bash
# 测试模板解析
python3 test_page_maker.py

# 测试HTML生成
python3 test_integration.py

# 运行完整演示
python3 demo.py
```

## 系统要求

- Python 3.6+
- tkinter（GUI支持，通常随Python安装）
- 无需额外依赖

## 许可证

MIT License - 详见 LICENSE 文件
