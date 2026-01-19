# Page Maker for Blog - 博客页面生成器

一个简单的Python工具，用于从HTML模板快速创建博客页面。

## 功能特点

- 📝 从预定义的HTML模板中选择
- ✏️ 自动识别模板中的可编辑区域（`<p class="..."></p>` 标签）
- 🖊️ 图形化界面输入内容
- 💾 一键生成HTML文件
- 🎨 支持多个模板样式

## 系统要求

- Python 3.6 或更高版本
- tkinter（通常随Python一起安装）

## 安装

克隆此仓库：

```bash
git clone https://github.com/ShioLilia/page-maker-for-blog.git
cd page-maker-for-blog
```

## 使用方法

### 启动程序

```bash
python page_maker.py
```

或者在支持的系统上：

```bash
python3 page_maker.py
```

### 使用步骤

1. **选择模板**：从下拉菜单中选择一个HTML模板，点击"加载模板"
2. **编辑内容**：在生成的输入框中编辑各个部分的内容（显示默认值）
3. **输入文件名**：在文件名输入框中输入要保存的文件名
4. **生成文件**：点击"完成 - 生成HTML文件"按钮

生成的HTML文件将保存在 `output/` 目录中。

## 目录结构

```
page-maker-for-blog/
├── page_maker.py          # 主程序
├── templates/             # HTML模板目录
│   ├── blog_post.html     # 博客文章模板
│   ├── simple_article.html # 简单文章模板
│   └── tech_note.html     # 技术笔记模板
└── output/                # 生成的HTML文件保存目录
```

## 添加自定义模板

1. 在 `templates/` 目录中创建新的HTML文件
2. 在需要用户输入的地方使用 `<p class="unique-class-name">默认内容</p>` 标签
3. 确保每个可编辑区域的 class 名称是唯一的

### 模板示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>My Template</title>
</head>
<body>
    <h1><p class="title">文章标题</p></h1>
    <p class="author">作者名</p>
    <p class="content">文章内容</p>
</body>
</html>
```

程序会自动检测所有带有 class 属性的 `<p>` 标签，并为每个标签创建输入框。

## 注意事项

- 只有带 class 属性的 `<p>` 标签会被识别为可编辑区域
- 每个 class 名称在模板中应该是唯一的，否则替换时可能产生意外结果
- 生成的文件会覆盖同名文件，请注意备份

## License

MIT License - 详见 LICENSE 文件
