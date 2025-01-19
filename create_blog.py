import os
import shutil
from datetime import datetime

def create_new_blog(title, description, markdown_path):
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create blog number
    blogs_dir = "./blogs"
    existing_blogs = [f for f in os.listdir(blogs_dir) if f.startswith("blog")]
    new_blog_num = len(existing_blogs) + 1
    new_blog_file = f"blog{new_blog_num}.html"
    
    # Copy template
    shutil.copy("./blogs/blog1.html", f"./blogs/{new_blog_file}")
    
    # Update blog HTML content
    with open(f"./blogs/{new_blog_file}", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace title
    content = content.replace("萌新の概率与期望", title)
    
    with open(f"./blogs/{new_blog_file}", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Update index.html
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
    
    # Create new blog entry
    new_blog_entry = f"""
            <article class="blog-post">
                <h2>{title}</h2>
                <p class="date">{current_date}</p>
                <p>{description}</p>
                <a href="blogs/{new_blog_file}">阅读更多</a>
            </article>
"""
    
    # Insert new blog entry after the first article
    insert_point = index_content.find('<article class="blog-post">')
    index_content = index_content[:insert_point] + new_blog_entry + index_content[insert_point:]
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"Blog created successfully: {new_blog_file}")
    print(f"Index.html updated")

if __name__ == "__main__":
    title = input("Enter blog title: ")
    description = input("Enter blog description: ")
    markdown_path = input("Enter path to markdown file: ")
    
    create_new_blog(title, description, markdown_path)
    