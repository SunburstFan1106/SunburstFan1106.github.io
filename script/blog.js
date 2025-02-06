// 扩展 marked 以支持数学公式
const renderer = new marked.Renderer();
const originalCode = renderer.code.bind(renderer);

renderer.code = function(code, language) {
    if (language === 'math') {
        return `<div class="math-block">${code}</div>`;
    }
    // 使用 highlight.js 进行代码高亮
    const validLanguage = hljs.getLanguage(language) ? language : 'plaintext';
    const highlighted = hljs.highlight(code, {language: validLanguage}).value;
    return `<pre><code class="hljs language-${validLanguage}">${highlighted}</code></pre>`;
};

// 自定义数学公式处理
const mathExtension = {
    name: 'math',
    level: 'inline',
    start(src) { return src.match(/\$/)?.index; },
    tokenizer(src) {
        const match = src.match(/^\$+([^$\n]+?)\$+/);
        if (match) {
            return {
                type: 'math',
                raw: match[0],
                text: match[1].trim()
            };
        }
    },
    renderer(token) {
        return `\\(${token.text}\\)`;
    }
};

marked.use({ extensions: [mathExtension] });
marked.setOptions({
    renderer: renderer,
    gfm: true,
    breaks: true
});

// 等待 KaTeX 加载完成
window.addEventListener('load', () => {
    // 获取当前页面的文件名
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1);
    const blogName = filename.replace('.html', ''); // 提取 blog1, blog2 等

    // 构造 Markdown 文件的路径
    const mdFilePath = `../blogs/${blogName}.md`;

    fetch(mdFilePath)
        .then(response => response.text())
        .then(text => {
            // 预处理 LaTeX 公式
            text = text.replace(/\$\$([\s\S]+?)\$\$/g, '\n```math\n$1\n```\n');
            
            // 渲染 Markdown
            const rendered = marked.parse(text);
            document.getElementById('content').innerHTML = rendered;
            
            // 渲染数学公式
            renderMathInElement(document.getElementById('content'), {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false,
                strict: false,
                trust: true,
                macros: {
                    "\\cases": "\\begin{cases}#1\\end{cases}"
                }
            });

            // 初始化代码高亮
            document.querySelectorAll('pre code').forEach(block => {
                hljs.highlightBlock(block);
            });

            // 生成目录
            generateTOC();
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('content').innerHTML = 
                '<p style="color: red">加载文档失败，请检查文件路径或网络连接。</p>';
        });
});

// 修改目录生成函数
function generateTOC() {
    const toc = document.getElementById('toc');
    toc.innerHTML = '';

    // 创建目录树结构
    const tocTree = {children: [], level: 0};
    let currentNode = tocTree;
    const nodeStack = [tocTree];

    // 获取所有标题并生成目录树
    document.querySelectorAll('.blog-content h2, .blog-content h3, .blog-content h4').forEach((heading, index) => {
        const level = parseInt(heading.tagName[1]);
        const text = heading.textContent.trim();
        const id = `section-${index}`;
        heading.id = id;

        const node = {
            id,
            text,
            level,
            children: [],
            parent: null
        };

        // 调整当前节点位置
        while (nodeStack[nodeStack.length - 1].level >= level) {
            nodeStack.pop();
        }
        currentNode = nodeStack[nodeStack.length - 1];
        node.parent = currentNode;
        currentNode.children.push(node);
        nodeStack.push(node);
    });

    // 渲染目录树
    function renderTOC(node, container, level = 0) {
        if (!node.id) {
            node.children.forEach(child => renderTOC(child, container, level));
            return;
        }

        const item = document.createElement('div');
        item.className = 'toc-item';
        
        const link = document.createElement('a');
        link.href = '#' + node.id;
        link.textContent = node.text;
        link.dataset.level = `h${node.level}`;
        link.dataset.parentId = node.parent?.id || 'root';
        
        item.appendChild(link);
        container.appendChild(item);

        if (node.children.length > 0) {
            const subContainer = document.createElement('div');
            subContainer.className = 'toc-sub';
            item.appendChild(subContainer);
            node.children.forEach(child => renderTOC(child, subContainer, level + 1));
        }
    }

    renderTOC(tocTree, toc);

    // 监听滚动事件
    const headings = Array.from(document.querySelectorAll('.blog-content h2, .blog-content h3, .blog-content h4'));
    let lastActiveId = null;

    function updateActiveHeading() {
        const viewportHeight = window.innerHeight;
        const scrollPosition = window.scrollY;
        const docHeight = document.documentElement.scrollHeight;
        
        // 检查是否接近文档底部
        const isNearBottom = (scrollPosition + viewportHeight) >= docHeight - 50;
        
        if (isNearBottom) {
            // 如果接近底部，直接激活最后一个标题
            const lastHeading = headings[headings.length - 1];
            if (lastHeading && lastHeading.id !== lastActiveId) {
                document.querySelectorAll('#toc a').forEach(link => {
                    link.classList.remove('active', 'parent-active');
                });
                
                const tocLink = document.querySelector(`#toc a[href="#${lastHeading.id}"]`);
                if (tocLink) {
                    tocLink.classList.add('active');
                    // 高亮父级目录
                    let parent = tocLink.parentElement;
                    while (parent) {
                        const parentLink = parent.querySelector(':scope > a');
                        if (parentLink) {
                            parentLink.classList.add('parent-active');
                        }
                        parent = parent.parentElement.closest('.toc-item');
                    }
                }
                lastActiveId = lastHeading.id;
            }
            return;
        }
        
        // 正常滚动时的处理
        const visibleHeadings = headings.map(heading => {
            const rect = heading.getBoundingClientRect();
            if (rect.top > viewportHeight) {
                return { heading, score: -Infinity };
            }
            if (rect.bottom < 0) {
                return { heading, score: -Infinity };
            }
            
            // 优化得分计算：越接近顶部得分越高
            const distanceFromIdeal = Math.abs(rect.top - 100);  // 理想位置为距离顶部100px
            const score = 1000 - distanceFromIdeal;
            
            return { heading, score };
        });
        
        // 找出得分最高的可见标题
        const bestHeading = visibleHeadings.reduce((a, b) => 
            a.score > b.score ? a : b
        );
        
        if (bestHeading.heading && bestHeading.heading.id !== lastActiveId) {
            document.querySelectorAll('#toc a').forEach(link => {
                link.classList.remove('active', 'parent-active');
            });
            
            const tocLink = document.querySelector(`#toc a[href="#${bestHeading.heading.id}"]`);
            if (tocLink) {
                tocLink.classList.add('active');
                let parent = tocLink.parentElement;
                while (parent) {
                    const parentLink = parent.querySelector(':scope > a');
                    if (parentLink) {
                        parentLink.classList.add('parent-active');
                    }
                    parent = parent.parentElement.closest('.toc-item');
                }
            }
            
            lastActiveId = bestHeading.heading.id;
        }
    }

    // 使用 requestAnimationFrame 和防抖优化滚动处理
    let scrollTimer = null;
    window.addEventListener('scroll', () => {
        if (scrollTimer) return;
        scrollTimer = requestAnimationFrame(() => {
            updateActiveHeading();
            scrollTimer = null;
        });
    }, { passive: true });

    // 初始化激活状态
    updateActiveHeading();
}
// 主题切换逻辑
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// 检查本地存储中的主题设置
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    body.classList.add(currentTheme);
    themeToggle.textContent = currentTheme === 'dark-mode' ? '🌞' : '🌙';
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark-mode' : '');
    themeToggle.textContent = isDark ? '🌞' : '🌙';
});