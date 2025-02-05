document.addEventListener('DOMContentLoaded', () => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    const body = document.body;
    
    // 创建新图片对象
    const img = new Image();
    const bgUrl = '你的背景图片URL';
    
    img.onload = () => {
        // 图片加载完成后设置背景
        body.style.backgroundImage = `url(${bgUrl})`;
        
        // 淡出加载动画
        if (loadingOverlay) {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
            }, 300);
        }
    };
    
    img.onerror = () => {
        // 图片加载失败时使用备用背景
        body.style.backgroundColor = '#f0f0f0';
        console.warn('背景图片加载失败');
        
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    };
    
    // 开始加载图片
    img.src = bgUrl;
});document.addEventListener('DOMContentLoaded', () => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    const body = document.body;
    
    // 创建新图片对象
    const img = new Image();
    const bgUrl = '你的背景图片URL';
    
    img.onload = () => {
        // 图片加载完成后设置背景
        body.style.backgroundImage = `url(${bgUrl})`;
        
        // 淡出加载动画
        if (loadingOverlay) {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
            }, 300);
        }
    };
    
    img.onerror = () => {
        // 图片加载失败时使用备用背景
        body.style.backgroundColor = '#f0f0f0';
        console.warn('背景图片加载失败');
        
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    };
    
    // 开始加载图片
    img.src = bgUrl;
});