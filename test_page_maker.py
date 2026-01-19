#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for page_maker.py - validates template parsing functionality
"""

import os
import sys
from html.parser import HTMLParser


class PTagParser(HTMLParser):
    """Parser to find <p> tags with class attribute"""
    
    def __init__(self):
        super().__init__()
        self.p_tags = []
        self.current_p_class = None
        self.current_p_start = None
        self.capture_content = False
        self.current_content = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for attr_name, attr_value in attrs:
                if attr_name == 'class' and attr_value:
                    self.current_p_class = attr_value
                    self.current_p_start = self.getpos()
                    self.capture_content = True
                    self.current_content = []
                    break
    
    def handle_endtag(self, tag):
        if tag == 'p' and self.capture_content:
            content = ''.join(self.current_content)
            self.p_tags.append({
                'class': self.current_p_class,
                'content': content,
                'start_pos': self.current_p_start
            })
            self.capture_content = False
            self.current_p_class = None
            self.current_content = []
    
    def handle_data(self, data):
        if self.capture_content:
            self.current_content.append(data)


def test_template_parsing():
    """Test that templates can be parsed correctly"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    if not os.path.exists(templates_dir):
        print(f"❌ Templates directory not found: {templates_dir}")
        return False
    
    templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    
    if not templates:
        print("❌ No HTML templates found")
        return False
    
    print(f"✓ Found {len(templates)} template(s)")
    
    all_passed = True
    for template_name in templates:
        template_path = os.path.join(templates_dir, template_name)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parser = PTagParser()
            parser.feed(content)
            
            print(f"\n📄 Template: {template_name}")
            print(f"  Found {len(parser.p_tags)} editable field(s):")
            
            for field in parser.p_tags:
                print(f"    - class=\"{field['class']}\": {field['content'][:50]}...")
            
            if len(parser.p_tags) == 0:
                print("  ⚠️  Warning: No editable fields found in this template")
            
        except Exception as e:
            print(f"❌ Error parsing {template_name}: {str(e)}")
            all_passed = False
    
    return all_passed


def test_output_directory():
    """Test that output directory exists"""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    if os.path.exists(output_dir):
        print(f"\n✓ Output directory exists: {output_dir}")
        return True
    else:
        print(f"\n❌ Output directory not found: {output_dir}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Page Maker - Testing Core Functionality")
    print("=" * 60)
    
    test1 = test_template_parsing()
    test2 = test_output_directory()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
