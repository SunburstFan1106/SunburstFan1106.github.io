// 主题切换功能
const themeToggle = document.getElementById('themeToggle');
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// 从本地存储或系统首选项加载主题
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    setTheme(savedTheme);
} else if (prefersDarkScheme.matches) {
    setTheme('dark');
}

// 搜索功能
const searchToggle = document.getElementById('searchToggle');
const searchModal = document.getElementById('searchModal');
const closeSearch = document.getElementById('closeSearch');
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

function initializeSearch() {
    if (!searchToggle || !searchModal || !closeSearch || !searchInput || !searchResults) {
        console.warn('搜索功能初始化失败：缺少必要元素');
        return;
    }

    searchToggle.addEventListener('click', () => {
        searchModal.style.display = 'block';
        searchInput.focus();
    });

    closeSearch.addEventListener('click', () => {
        searchModal.style.display = 'none';
    });

    searchInput.addEventListener('input', debounce(() => {
        const query = searchInput.value.toLowerCase();
        if (query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }
        
        const articles = document.querySelectorAll('.blog-post, .blog-content');
        const results = [];
        
        articles.forEach(article => {
            const titleEl = article.querySelector('h1, h2');
            const contentEl = article.querySelector('p');
            
            if (!titleEl || !contentEl) return;
            
            const title = titleEl.textContent.toLowerCase();
            const content = contentEl.textContent.toLowerCase();
            
            if (title.includes(query) || content.includes(query)) {
                results.push(`
                    <div class="search-result">
                        <h3>${titleEl.textContent}</h3>
                        <p>${contentEl.textContent.substring(0, 200)}...</p>
                    </div>
                `);
            }
        });
        
        searchResults.innerHTML = results.length ? 
            results.join('') : 
            '<p class="no-results">未找到相关内容</p>';
    }, 300));
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 初始化主题切换
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }

    // 初始化搜索功能
    initializeSearch();
});// 主题切换功能