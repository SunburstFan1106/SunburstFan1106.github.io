import os
from git_sync import git_sync

def list_blogs():
    """列出所有可用的博客"""
    blogs_dir = "./blogs"
    blogs = [f for f in os.listdir(blogs_dir) if f.startswith("blog") and f.endswith(".html")]
    
    if not blogs:
        print("没有找到任何博客！")
        return []
    
    print("\n可用的博客：")
    for i, blog in enumerate(blogs, 1):
        # 读取博客文件获取标题
        with open(os.path.join(blogs_dir, blog), "r", encoding="utf-8") as f:
            content = f.read()
            # 简单查找标题标签之间的内容
            start = content.find("<h1>") + 4
            end = content.find("</h1>")
            title = content[start:end] if start > 3 and end > 0 else blog
            print(f"{i}. {blog} - {title}")
    
    return blogs

def delete_blog(blog_file):
    """删除指定的博客文件及其关联文件"""
    blogs_dir = "./blogs"
    
    # 删除 HTML 文件
    html_path = os.path.join(blogs_dir, blog_file)
    if os.path.exists(html_path):
        os.remove(html_path)
        print(f"已删除 HTML 文件: {blog_file}")
    
    # 删除对应的 Markdown 文件
    md_file = blog_file.replace(".html", ".md")
    md_path = os.path.join(blogs_dir, md_file)
    if os.path.exists(md_path):
        os.remove(md_path)
        print(f"已删除 Markdown 文件: {md_file}")
    
    # 从 index.html 中移除博客条目
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
    
    # 查找并删除博客条目
    blog_entry_start = index_content.find(f'<a href="blogs/{blog_file}">')
    if blog_entry_start != -1:
        # 向前查找文章开始标记
        article_start = index_content.rfind('<article class="blog-post">', 0, blog_entry_start)
        # 向后查找文章结束标记
        article_end = index_content.find('</article>', blog_entry_start) + 10
        
        if article_start != -1 and article_end != -1:
            # 删除整个文章块
            index_content = index_content[:article_start] + index_content[article_end:]
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(index_content)
            print("已从首页移除博客条目")
    
    # 在删除完成后进行git同步
    git_sync(f"Delete blog: {blog_file}")

def main():
    while True:
        blogs = list_blogs()
        if not blogs:
            break
            
        try:
            choice = input("\n请输入要删除的博客编号 (输入 q 退出): ")
            if choice.lower() == 'q':
                break
                
            blog_index = int(choice) - 1
            if 0 <= blog_index < len(blogs):
                confirm = input(f"确定要删除 {blogs[blog_index]} 吗? (y/n): ")
                if confirm.lower() == 'y':
                    delete_blog(blogs[blog_index])
                    print("删除完成！")
            else:
                print("无效的博客编号！")
        except ValueError:
            print("请输入有效的数字！")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()
