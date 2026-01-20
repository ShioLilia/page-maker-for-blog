#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for page_maker.py - simulates HTML generation
"""

import os
from html_utils import PTagParser, replace_content_safe


def test_html_generation():
    """Test HTML generation with sample data"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Test with blog_post.html template
    template_path = os.path.join(templates_dir, 'blog_post.html')
    
    print("Testing HTML generation...")
    print(f"Using template: blog_post.html")
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Parse template
    parser = PTagParser()
    parser.feed(template_content)
    
    print(f"Found {len(parser.p_tags)} editable fields")
    
    # Simulate user input
    user_inputs = {
        'title': '我的第一篇博客',
        'author': '作者: 张三',
        'date': '日期: 2024-01-19',
        'content-main': '这是一篇测试博客文章。通过Page Maker工具生成，验证功能是否正常工作。'
    }
    
    print("\nSimulating user inputs:")
    for class_name, content in user_inputs.items():
        print(f"  {class_name}: {content}")
    
    # Generate HTML
    result_html = template_content
    
    for class_name, new_content in user_inputs.items():
        result_html = replace_content_safe(result_html, class_name, new_content)
    
    # Save result
    output_path = os.path.join(output_dir, 'test_output.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_html)
    
    print(f"\n✅ HTML file generated successfully: {output_path}")
    
    # Verify content
    with open(output_path, 'r', encoding='utf-8') as f:
        generated_content = f.read()
    
    # Check if user inputs are in the generated file
    all_present = True
    for class_name, content in user_inputs.items():
        if content in generated_content:
            print(f"  ✓ Content for '{class_name}' found in output")
        else:
            print(f"  ❌ Content for '{class_name}' NOT found in output")
            all_present = False
    
    return all_present


if __name__ == "__main__":
    print("=" * 60)
    print("Page Maker - Integration Test")
    print("=" * 60 + "\n")
    
    success = test_html_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Integration test passed!")
    else:
        print("❌ Integration test failed!")
    print("=" * 60)
