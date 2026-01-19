#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Page Maker - A tool to create HTML pages from templates
"""

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from html.parser import HTMLParser
from typing import List, Tuple


class PTagParser(HTMLParser):
    """Parser to find <p> tags with class attribute"""
    
    def __init__(self):
        super().__init__()
        self.p_tags = []  # List of (class_name, content, start_pos, end_pos)
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


class PageMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog Page Maker - 博客页面生成器")
        self.root.geometry("800x700")
        
        # Variables
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        self.selected_template = None
        self.template_content = ""
        self.editable_fields = []
        self.input_widgets = {}
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create UI
        self.create_widgets()
        self.load_templates()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        
        # Template selection frame
        template_frame = ttk.LabelFrame(self.root, text="步骤1: 选择模板", padding="10")
        template_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(
            template_frame, 
            textvariable=self.template_var,
            state='readonly',
            width=50
        )
        self.template_combo.pack(side=tk.LEFT, padx=5)
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)
        
        ttk.Button(template_frame, text="加载模板", command=self.on_template_selected).pack(side=tk.LEFT, padx=5)
        
        # Editable fields frame (scrollable)
        fields_frame = ttk.LabelFrame(self.root, text="步骤2: 编辑内容", padding="10")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(fields_frame)
        scrollbar = ttk.Scrollbar(fields_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Filename frame
        filename_frame = ttk.LabelFrame(self.root, text="步骤3: 输入文件名", padding="10")
        filename_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filename_frame, text="文件名:").pack(side=tk.LEFT, padx=5)
        self.filename_var = tk.StringVar(value="output.html")
        ttk.Entry(filename_frame, textvariable=self.filename_var, width=40).pack(side=tk.LEFT, padx=5)
        
        # Generate button frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="完成 - 生成HTML文件", command=self.generate_html).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="重置", command=self.reset_fields).pack(side=tk.RIGHT, padx=5)
    
    def load_templates(self):
        """Load available templates from templates directory"""
        if not os.path.exists(self.templates_dir):
            messagebox.showerror("错误", f"模板目录不存在: {self.templates_dir}")
            return
        
        templates = [f for f in os.listdir(self.templates_dir) if f.endswith('.html')]
        if not templates:
            messagebox.showwarning("警告", "模板目录中没有找到HTML文件")
            return
        
        self.template_combo['values'] = templates
        if templates:
            self.template_combo.current(0)
    
    def on_template_selected(self, event=None):
        """Handle template selection"""
        template_name = self.template_var.get()
        if not template_name:
            return
        
        template_path = os.path.join(self.templates_dir, template_name)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            
            # Parse template to find editable fields
            parser = PTagParser()
            parser.feed(self.template_content)
            self.editable_fields = parser.p_tags
            
            # Create input widgets for each field
            self.create_input_fields()
            
            messagebox.showinfo("成功", f"已加载模板: {template_name}\n找到 {len(self.editable_fields)} 个可编辑字段")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载模板失败: {str(e)}")
    
    def create_input_fields(self):
        """Create input widgets for each editable field"""
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.input_widgets = {}
        
        if not self.editable_fields:
            ttk.Label(
                self.scrollable_frame, 
                text="该模板没有可编辑的 <p class=\"...\"></p> 标签",
                foreground="red"
            ).pack(pady=20)
            return
        
        for idx, field in enumerate(self.editable_fields):
            class_name = field['class']
            default_content = field['content']
            
            # Create frame for each field
            field_frame = ttk.Frame(self.scrollable_frame)
            field_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Label
            label_text = f"[{class_name}]"
            ttk.Label(field_frame, text=label_text, width=20).pack(side=tk.LEFT, padx=5)
            
            # Input widget (use Text widget for multiline support)
            text_widget = tk.Text(field_frame, height=3, width=60, wrap=tk.WORD)
            text_widget.insert(1.0, default_content)
            text_widget.pack(side=tk.LEFT, padx=5)
            
            # Store reference
            self.input_widgets[class_name] = {
                'widget': text_widget,
                'default': default_content
            }
    
    def reset_fields(self):
        """Reset all fields to default values"""
        for class_name, field_info in self.input_widgets.items():
            widget = field_info['widget']
            default = field_info['default']
            widget.delete(1.0, tk.END)
            widget.insert(1.0, default)
    
    def generate_html(self):
        """Generate HTML file with user inputs"""
        if not self.template_content:
            messagebox.showerror("错误", "请先选择并加载一个模板")
            return
        
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("错误", "请输入文件名")
            return
        
        if not filename.endswith('.html'):
            filename += '.html'
        
        # Replace content in template
        result_html = self.template_content
        
        for class_name, field_info in self.input_widgets.items():
            widget = field_info['widget']
            new_content = widget.get(1.0, tk.END).strip()
            
            # Use regex to replace content within <p class="class_name">...</p>
            pattern = rf'(<p\s+class="{re.escape(class_name)}">)(.*?)(</p>)'
            
            def replacement_func(match):
                return match.group(1) + new_content + match.group(3)
            
            result_html = re.sub(pattern, replacement_func, result_html, flags=re.DOTALL)
        
        # Save to output directory
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result_html)
            
            messagebox.showinfo(
                "成功", 
                f"HTML文件已生成!\n保存位置: {output_path}"
            )
            
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")


def main():
    root = tk.Tk()
    app = PageMakerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
