import os
import shutil
from datetime import datetime

def create_new_blog(title, description, markdown_path):
    # Convert relative path to absolute path if needed
    if not os.path.isabs(markdown_path):
        markdown_path = os.path.abspath(markdown_path)
    
    # Check if markdown file exists
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file not found at {markdown_path}")
        return
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create blog number
    blogs_dir = os.path.join(os.path.dirname(__file__), "blogs")
    existing_blogs = [f for f in os.listdir(blogs_dir) if f.startswith("blog") and f.endswith(".html")]
    new_blog_num = len(existing_blogs) + 1
    new_blog_file = f"blog{new_blog_num}.html"
    new_md_file = f"blog{new_blog_num}.md"
    
    # Create full paths
    template_path = os.path.join(blogs_dir, "blog1.html")
    new_blog_path = os.path.join(blogs_dir, new_blog_file)
    new_md_path = os.path.join(blogs_dir, new_md_file)
    
    # Copy template and markdown
    shutil.copy(template_path, new_blog_path)
    shutil.copy(markdown_path, new_md_path)
    
    # Update blog HTML content
    with open(new_blog_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace title and description
    content = content.replace("萌新の概率与期望", title)
    content = content.replace("算法学习笔记", description)
    
    # Update the markdown file path in the JavaScript fetch call
    content = content.replace(
        "fetch('../blogs/blog1.md')",
        f"fetch('../blogs/{new_md_file}')"
    )
    
    with open(new_blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Update index.html
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()
    
    # Create new blog entry
    new_blog_entry = f"""            <article class="blog-post">
                <h2>{title}</h2>
                <p class="date">{current_date}</p>
                <p>{description}</p>
                <a href="blogs/{new_blog_file}">阅读更多</a>
            </article>
"""
    
    # Find the main section and insert the new blog entry at the top
    main_start = index_content.find('<main>')
    insert_point = index_content.find('<article class="blog-post">', main_start)
    
    index_content = (
        index_content[:insert_point] +
        new_blog_entry +
        index_content[insert_point:]
    )
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"Blog created successfully: {new_blog_file}")
    print(f"Markdown file copied to: {new_md_file}")
    print(f"Index.html updated")

if __name__ == "__main__":
    title = input("Enter blog title: ")
    description = input("Enter blog description: ")
    markdown_path = input("Enter path to markdown file: ")
    
    create_new_blog(title, description, markdown_path)
