## K0be_Bl0gant 1.0 --基于 Github Pages 的个人博客搭建

### 写在前面

这是一篇搭建博客的教程。

常见的博客网站有*博客园*、*洛谷专栏*、*CSDN博客*等。

但是受限于第三方网站的限制，博客的自由度不够，想要自定义，就需要自己搭建一个博客网站。

这里提供一个基于 Github Pages 的静态个人博客搭建开源模版，同时还可以通过 Git commit 的方式上传博文，维护博客。

### 你需要准备什么

- 一个 Github 账号

- Git

- python 编译器

这些如何注册安装网上的教程很多，这里不再赘述。

### 开始搭建

#### 第一步：创建仓库

打开 Github 网页，登录账号，找到创建仓库的按钮，开始创建。

将仓库的名字命名为 XXX.github.io，其中 XXX 为你的Github用户名。

创建成功后，从本地克隆该仓库，创建 `index.html` 文件，可以现在里边写：

```
<h1>Hello World!</h1>
```

保存并上传同步，等待一段时间后，访问 XXX.github.io 这个网址，如果出现 `Hello World!`，则说明仓库搭建成功。

#### 第二步：撰写 index.html

index.html 是访问你个人博客的首页。

你可以根据自己的需要搭建你的首页。

这里提供 K0be_Bl0gant 1.0 的 index.html [代码](https://www.luogu.com.cn/paste/q8pxj23i)。

还有提供渲染的 [Rei.css](https://www.luogu.com.cn/paste/j8ez0ktr)。

我的代码针对手机等小屏幕的设备进行了优化，做了 Responsive Design。

#### 第三步：撰写博文

在仓库中创建一个名为 `blogs` 的文件夹，将你所写的 markdown 复制进来，然后写一个 blog.html 将其显示出来。

我的 [blog.html 代码](https://www.luogu.com.cn/paste/irz6bcdc)。

还有提供渲染的 [Rei_blog.css](https://www.luogu.com.cn/paste/kvn1c9cr)。

#### 第四部：自动化脚本

这样的自定义博客是一个静态网站，每次添加新文章都需要手动加文件重写 index.html 手动 commit，很麻烦。

可以写一个 python 脚本实现自动化维护：

首先是 [git 同步的脚本](https://www.luogu.com.cn/paste/3g0hd7jm)。

然后是完整的[维护博客的 python 脚本](https://www.luogu.com.cn/paste/oxg0lhmz)。

每次更新只需要运行 blog_update.py 即可。

### 成品展示

[M_WC1S_M0的博客](https://www.sunburstfan1106.github.io)。

大家如果没看明白的话也可以先看看[我的仓库](https://github.com/SunburstFan1106/SunburstFan1106.github.io)，复制到你们自己的仓库里，不要克隆我的仓库然后帮我乱 commit（雾。

Done.