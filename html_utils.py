#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for page maker - shared HTML parsing and replacement logic
"""

import re
from html import escape
from html.parser import HTMLParser


class PTagParser(HTMLParser):
    """Parser to find <p> tags with class attribute"""
    
    def __init__(self):
        super().__init__()
        self.p_tags = []  # List of (class_name, content, start_pos)
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


def replace_content_safe(template, class_name, new_content, escape_html=True):
    """
    Safely replace content in a <p class="..."> tag.
    
    Args:
        template: HTML template string
        class_name: CSS class name of the <p> tag
        new_content: New content to insert
        escape_html: If True, escapes HTML entities to prevent XSS (default: True)
        
    Returns:
        Modified HTML string with content replaced
    """
    # Escape HTML to prevent XSS vulnerabilities
    if escape_html:
        new_content = escape(new_content)
    
    # Pattern handles both double and single quotes
    pattern = rf'(<p\s+class=["\']?{re.escape(class_name)}["\']?>)(.*?)(</p>)'
    
    def replacement_func(match):
        return match.group(1) + new_content + match.group(3)
    
    return re.sub(pattern, replacement_func, template, flags=re.DOTALL)
