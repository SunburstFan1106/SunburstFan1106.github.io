import os
import shutil
from datetime import datetime
from git_sync import git_sync

def list_blogs():
    """列出所有可用的博客"""
    blogs_dir = "./blogs"
    blogs = [f for f in os.listdir(blogs_dir) if f.startswith("blog") and f.endswith(".html")]
    
    if not blogs:
        print("\n当前没有任何博客！")
        return []
    
    print("\n现有博客列表：")
    for i, blog in enumerate(blogs, 1):
        with open(os.path.join(blogs_dir, blog), "r", encoding="utf-8") as f:
            content = f.read()
            start = content.find("<h1>") + 4
            end = content.find("</h1>")
            title = content[start:end] if start > 3 and end > 0 else blog
            print(f"{i}. {blog} - {title}")
    
    return blogs

def create_new_blog():
    """创建新博客"""
    print("\n=== 创建新博客 ===")
    title = input("请输入博客标题: ")
    description = input("请输入博客描述: ")
    markdown_path = input("请输入Markdown文件路径: ")
    
    # 转换为绝对路径
    if not os.path.isabs(markdown_path):
        markdown_path = os.path.abspath(markdown_path)
    
    if not os.path.exists(markdown_path):
        print(f"错误: 未找到Markdown文件 {markdown_path}")
        return
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    blogs_dir = os.path.join(os.path.dirname(__file__), "blogs")
    existing_blogs = [f for f in os.listdir(blogs_dir) if f.startswith("blog") and f.endswith(".html")]
    new_blog_num = len(existing_blogs) + 1
    new_blog_file = f"blog{new_blog_num}.html"
    new_md_file = f"blog{new_blog_num}.md"
    
    template_path = os.path.join(blogs_dir, "blog1.html")
    new_blog_path = os.path.join(blogs_dir, new_blog_file)
    new_md_path = os.path.join(blogs_dir, new_md_file)
    
    # 复制模板和markdown文件
    shutil.copy(template_path, new_blog_path)
    shutil.copy(markdown_path, new_md_path)
    
    # 更新博客HTML内容
    with open(new_blog_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("萌新の概率与期望", title)
    content = content.replace("算法学习笔记", description)
    content = content.replace(
        "fetch('../blogs/blog1.md')",
        f"fetch('../blogs/{new_md_file}')"
    )
    
    with open(new_blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # 更新index.html
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    
    new_blog_entry = f"""            <article class="blog-post">
                <h2>{title}</h2>
                <p class="date">{current_date}</p>
                <p>{description}</p>
                <a href="blogs/{new_blog_file}">阅读更多</a>
            </article>
"""
    
    main_start = index_content.find('<main>')
    insert_point = index_content.find('<article class="blog-post">', main_start)
    
    index_content = (
        index_content[:insert_point] +
        new_blog_entry +
        index_content[insert_point:]
    )
    
    # 添加归档条目
    archive_entry = f"""            <li>
                <span class="date">{current_date}</span>
                <a href="blogs/{new_blog_file}">{title}</a>
            </li>
"""
    
    archive_start = index_content.find('<ul class="archive-list">')
    archive_insert_point = index_content.find('<li>', archive_start)
    
    index_content = (
        index_content[:archive_insert_point] +
        archive_entry +
        index_content[archive_insert_point:]
    )
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"\n博客创建成功: {new_blog_file}")
    print(f"Markdown文件已复制到: {new_md_file}")
    print(f"首页已更新")
    
    git_sync(f"Add new blog: {title}")

def delete_blog():
    """删除博客"""
    print("\n=== 删除博客 ===")
    blogs = list_blogs()
    if not blogs:
        return
        
    try:
        choice = input("\n请输入要删除的博客编号 (按q返回): ")
        if choice.lower() == 'q':
            return
            
        blog_index = int(choice) - 1
        if 0 <= blog_index < len(blogs):
            blog_file = blogs[blog_index]
            confirm = input(f"确定要删除 {blog_file} 吗? (y/n): ")
            if confirm.lower() == 'y':
                blogs_dir = "./blogs"
                
                # 删除HTML文件
                html_path = os.path.join(blogs_dir, blog_file)
                if os.path.exists(html_path):
                    os.remove(html_path)
                    print(f"已删除HTML文件: {blog_file}")
                
                # 删除Markdown文件
                md_file = blog_file.replace(".html", ".md")
                md_path = os.path.join(blogs_dir, md_file)
                if os.path.exists(md_path):
                    os.remove(md_path)
                    print(f"已删除Markdown文件: {md_file}")
                
                # 更新index.html
                with open("index.html", "r", encoding="utf-8") as f:
                    index_content = f.read()
                
                # 移除博客列表条目
                blog_entry_start = index_content.find(f'<a href="blogs/{blog_file}">')
                if blog_entry_start != -1:
                    article_start = index_content.rfind('<article class="blog-post">', 0, blog_entry_start)
                    article_end = index_content.find('</article>', blog_entry_start) + 10
                    
                    if article_start != -1 and article_end != -1:
                        index_content = index_content[:article_start] + index_content[article_end:]
                        
                # 移除归档条目
                archive_entry_start = index_content.find(f'<a href="blogs/{blog_file}">', blog_entry_start)
                if archive_entry_start != -1:
                    li_start = index_content.rfind('<li>', 0, archive_entry_start)
                    li_end = index_content.find('</li>', archive_entry_start) + 5
                    
                    if li_start != -1 and li_end != -1:
                        index_content = index_content[:li_start] + index_content[li_end:]
                
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(index_content)
                print("已从首页移除博客条目")
                
                git_sync(f"Delete blog: {blog_file}")
                print("\n删除完成！")
        else:
            print("无效的博客编号！")
    except ValueError:
        print("请输入有效的数字！")

def update_blog():
    """更新现有博客"""
    print("\n=== 更新博客 ===")
    blogs = list_blogs()
    if not blogs:
        return
        
    try:
        choice = input("\n请输入要更新的博客编号 (按q返回): ")
        if choice.lower() == 'q':
            return
            
        blog_index = int(choice) - 1
        if 0 <= blog_index < len(blogs):
            blog_file = blogs[blog_index]
            blogs_dir = "./blogs"
            blog_path = os.path.join(blogs_dir, blog_file)
            
            print("\n请选择要更新的内容：")
            print("1. 更新标题")
            print("2. 更新描述")
            print("3. 更新Markdown内容")
            print("4. 全部更新")
            
            update_choice = input("\n请选择 (1-4): ")
            
            with open(blog_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            with open("index.html", "r", encoding="utf-8") as f:
                index_content = f.read()
            
            if update_choice in ["1", "4"]:
                new_title = input("请输入新标题: ")
                # 更新博客文件中的标题
                start = content.find("<h1>") + 4
                end = content.find("</h1>")
                if start > 3 and end > 0:
                    content = content[:start] + new_title + content[end:]
                
                # 更新index.html中的标题
                blog_entry_start = index_content.find(f'<a href="blogs/{blog_file}">')
                if blog_entry_start != -1:
                    article_start = index_content.rfind('<article class="blog-post">', 0, blog_entry_start)
                    h2_start = index_content.find("<h2>", article_start) + 4
                    h2_end = index_content.find("</h2>", h2_start)
                    if h2_start > 3 and h2_end > 0:
                        index_content = index_content[:h2_start] + new_title + index_content[h2_end:]
                
                # 更新归档列表中的标题
                archive_entry_start = index_content.find(f'<a href="blogs/{blog_file}">')
                if archive_entry_start != -1:
                    archive_text_start = archive_entry_start + len(f'<a href="blogs/{blog_file}">')
                    archive_text_end = index_content.find('</a>', archive_text_start)
                    if archive_text_end > 0:
                        index_content = index_content[:archive_text_start] + new_title + index_content[archive_text_end:]
            
            if update_choice in ["2", "4"]:
                new_description = input("请输入新描述: ")
                # 更新index.html中的描述
                blog_entry_start = index_content.find(f'<a href="blogs/{blog_file}">')
                if blog_entry_start != -1:
                    article_start = index_content.rfind('<article class="blog-post">', 0, blog_entry_start)
                    p_start = index_content.find("<p>", article_start)
                    p_start = index_content.find("<p>", p_start + 1) + 3  # 跳过日期，找到描述的<p>标签
                    p_end = index_content.find("</p>", p_start)
                    if p_start > 2 and p_end > 0:
                        index_content = index_content[:p_start] + new_description + index_content[p_end:]
            
            if update_choice in ["3", "4"]:
                new_md_path = input("请输入新的Markdown文件路径: ")
                if not os.path.isabs(new_md_path):
                    new_md_path = os.path.abspath(new_md_path)
                
                if os.path.exists(new_md_path):
                    # 复制新的Markdown文件
                    md_file = blog_file.replace(".html", ".md")
                    shutil.copy(new_md_path, os.path.join(blogs_dir, md_file))
                    print(f"Markdown文件已更新: {md_file}")
                else:
                    print(f"错误: 未找到Markdown文件 {new_md_path}")
                    return
            
            # 保存更新后的内容
            with open(blog_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(index_content)
            
            print("\n博客更新成功！")
            git_sync(f"Update blog: {blog_file}")
            
        else:
            print("无效的博客编号！")
    except ValueError:
        print("请输入有效的数字！")

def main():
    while True:
        print("\n=== 博客管理系统 ===")
        print("1. 查看所有博客")
        print("2. 创建新博客")
        print("3. 删除博客")
        print("4. 更新博客")
        print("5. 退出")
        
        choice = input("\n请选择操作 (1-5): ")
        
        if choice == "1":
            list_blogs()
        elif choice == "2":
            create_new_blog()
        elif choice == "3":
            delete_blog()
        elif choice == "4":
            update_blog()
        elif choice == "5":
            print("\n再见！")
            break
        else:
            print("\n无效的选择，请重试！")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()