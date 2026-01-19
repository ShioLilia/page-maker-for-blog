#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing how to use page_maker programmatically (without GUI)
This demonstrates the core functionality.
"""

import os
from html_utils import PTagParser, replace_content_safe


def generate_blog_example():
    """Generate a blog post example"""
    print("=" * 70)
    print("Example 1: Generating a Blog Post")
    print("=" * 70)
    
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Load template
    template_path = os.path.join(templates_dir, 'blog_post.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Parse to find editable fields
    parser = PTagParser()
    parser.feed(template_content)
    
    print(f"\nTemplate: blog_post.html")
    print(f"Editable fields found: {len(parser.p_tags)}")
    for field in parser.p_tags:
        print(f"  - {field['class']}: \"{field['content']}\"")
    
    # Define custom content
    custom_content = {
        'title': 'Python学习心得',
        'author': '作者: 李明',
        'date': '日期: 2024-01-19',
        'content-main': 'Python是一门非常适合初学者的编程语言。它的语法简洁明了，拥有丰富的第三方库。通过学习Python，我掌握了数据分析、Web开发等多项技能。'
    }
    
    print("\nCustom content:")
    for key, value in custom_content.items():
        print(f"  - {key}: \"{value}\"")
    
    # Replace content
    result_html = template_content
    for class_name, new_content in custom_content.items():
        result_html = replace_content_safe(result_html, class_name, new_content)
    
    # Save
    output_path = os.path.join(output_dir, 'demo_blog_post.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_html)
    
    print(f"\n✅ Generated: {output_path}\n")


def generate_article_example():
    """Generate a simple article example"""
    print("=" * 70)
    print("Example 2: Generating a Simple Article")
    print("=" * 70)
    
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Load template
    template_path = os.path.join(templates_dir, 'simple_article.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Parse to find editable fields
    parser = PTagParser()
    parser.feed(template_content)
    
    print(f"\nTemplate: simple_article.html")
    print(f"Editable fields found: {len(parser.p_tags)}")
    for field in parser.p_tags:
        print(f"  - {field['class']}: \"{field['content']}\"")
    
    # Define custom content
    custom_content = {
        'heading': '阅读的力量',
        'subtitle-text': '探讨阅读如何改变我们的思维方式',
        'paragraph1': '阅读是获取知识最有效的途径之一。通过阅读，我们可以跨越时空，与不同时代的智者对话。',
        'paragraph2': '培养阅读习惯需要持之以恒。每天抽出30分钟阅读，一年就能读完数十本书，这将极大地拓展我们的视野。'
    }
    
    print("\nCustom content:")
    for key, value in custom_content.items():
        print(f"  - {key}: \"{value}\"")
    
    # Replace content
    result_html = template_content
    for class_name, new_content in custom_content.items():
        result_html = replace_content_safe(result_html, class_name, new_content)
    
    # Save
    output_path = os.path.join(output_dir, 'demo_article.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_html)
    
    print(f"\n✅ Generated: {output_path}\n")


def generate_tech_note_example():
    """Generate a tech note example"""
    print("=" * 70)
    print("Example 3: Generating a Technical Note")
    print("=" * 70)
    
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Load template
    template_path = os.path.join(templates_dir, 'tech_note.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Parse to find editable fields
    parser = PTagParser()
    parser.feed(template_content)
    
    print(f"\nTemplate: tech_note.html")
    print(f"Editable fields found: {len(parser.p_tags)}")
    for field in parser.p_tags:
        print(f"  - {field['class']}: \"{field['content']}\"")
    
    # Define custom content
    custom_content = {
        'note-title': 'Git合并冲突解决',
        'note-desc': 'Git, 版本控制, 合并冲突',
        'problem': '在团队协作中使用Git时，经常会遇到合并冲突的情况。特别是多人同时修改同一文件时。',
        'solution': '1. 使用git status查看冲突文件\n2. 编辑冲突文件，解决冲突标记\n3. 使用git add标记为已解决\n4. 提交合并结果',
        'summary': '理解Git的合并机制和冲突产生原因，可以帮助我们更好地预防和解决冲突。定期拉取远程代码，小步提交，可以有效减少冲突。'
    }
    
    print("\nCustom content:")
    for key, value in custom_content.items():
        print(f"  - {key}: \"{value[:50]}...\"")
    
    # Replace content
    result_html = template_content
    for class_name, new_content in custom_content.items():
        result_html = replace_content_safe(result_html, class_name, new_content)
    
    # Save
    output_path = os.path.join(output_dir, 'demo_tech_note.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_html)
    
    print(f"\n✅ Generated: {output_path}\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  Page Maker - Demo: Generating HTML files from templates")
    print("=" * 70 + "\n")
    
    generate_blog_example()
    generate_article_example()
    generate_tech_note_example()
    
    print("=" * 70)
    print("✅ All demo files generated successfully!")
    print("=" * 70)
    print("\nGenerated files are in the 'output/' directory:")
    print("  - demo_blog_post.html")
    print("  - demo_article.html")
    print("  - demo_tech_note.html")
    print("\nYou can open these files in a web browser to see the results.")
    print("=" * 70 + "\n")
