# 3.1-3.8 做题笔记



开学了，加上月考，最近做题比较少。

## COCI 2024/2025 作业

### [P11752 [COCI 2024/2025 #5] 挂画 / Zid](https://www.luogu.com.cn/problem/P11752)

#### 题目大意

给一个 $n\times m$ 的矩阵，由 `.` 和 `#` 两种有元素组成，求有多少个子矩形满足其中有且仅有一个 `#`。

#### 解题思路

二维前缀和的 $O(N^4)$ 做法是简单的，考虑双指针优化：

枚举子矩形两个端点的所在行，再用双指针维护其所在列，时间复杂度 $O(N^3)$。

### [P11753 [COCI 2024/2025 #5] 塔楼 / Tornjevi](https://www.luogu.com.cn/problem/P11753)

#### 题目大意

有一个长度为 $N$ 的序列 $a_1,a_2,\dots ,a_N$ 。

定义 $f(i) = \max (r-l+1)$，其中 $a_i = \gcd(a_l,a_{l+1},\dots,a_r), l\leq i\leq r$。

#### 解题思路

注意到 $l \leq i \leq r$，首先使用 st 表预处理出序列 $a$ 的所有区间的 $\gcd$。

然后就可以很容易二分出 $\min(l_i)$ 和 $\max(r_i)$，即可求解 $\max (r_i-l_i+1)$。

### [P11753 [COCI 2024/2025 #5] 绘图 / Crtež 题解](https://www.luogu.com.cn/problem/P11753)

#### 题目大意

给定一个长度为 $n$ 的序列，初始全为 $0$。每次给定区间 $[l,r]$，将区间内的 $0$ 和 $-1$ 互相翻转。每次操作后，求出能够以当前序列为基础，进行若干次填数操作得到的互不等价序列数量。

#### 解题思路

对于每个位置，我们只关心它是 $0$ 还是 $-1$。用线段树维护区间翻转操作。

$n \leq 10^{18}$，不能直接建树，考虑离散化，每个 $0$ 可以贡献 $3$ 种状态(保持 $0$ or $-1$ or 正数)。

因此答案为 $3^{cnt0}$。

核心代码如下:

```cpp
// 线段树维护区间内0和-1的个数
namespace SGT{
    int tree[N<<2][2],rev[N<<2]; // [0]存0的个数,[1]存-1的个数
    
    void pushup(int rt){
        tree[rt][0]=tree[rt<<1][0]+tree[rt<<1|1][0];
        tree[rt][1]=tree[rt<<1][1]+tree[rt<<1|1][1];
    }

    void upd(int rt){
        swap(tree[rt][0],tree[rt][1]); // 翻转0和-1
        rev[rt]^=1;
    }

    void modify(int rt,int l,int r,int L,int R){
        if(L<=l&&r<=R){
            upd(rt);
            return;
        }
        pushdown(rt);
        int md=(l+r)>>1;
        if(L<=md)modify(lson,L,R);
        if(R>md)modify(rson,L,R);
        pushup(rt);
    }
}

// 每次查询时计算3^cnt0
printf("%lld\n",qpow(3,SGT::tree[1][0]));
```

时间复杂度 $O(q \log q)$。

### [P11755 [COCI 2024/2025 #5] 树树 2 / Stablo II](https://www.luogu.com.cn/problem/P11755)

#### 题目大意

有一棵树，初始点权为 $0$，每次操作将 $u$ 到 $v$ 最短路径上的点全部赋值为操作序号 $i$。

输出每条边的点权。

#### 解题思路

显然是树剖模板，但是数据范围 $N\leq 10^6$，需要卡常。

写了一个 $O(N\times \log N)$ 的树剖+线段树，可能是自己的模板常数很小，直接获得了 90pts。

本来想着用题解离线修改+记忆化查询的方法优化来着，但是加上 `inline` 和快读快写之后直接在洛谷和 cyezoj 上都过了？

## ABC 391-395 补题

由于自己太菜了，每次的 ABC 都会留一些没做完的题。

### [\[ABC391F\] K-th Largest Triplet](https://www.luogu.com.cn/problem/AT_abc391_f)

#### 题目大意

有 $3$ 个长度为 $N$ 的序列 $a,b,c$，对于所有的 $1\leq i,j,k \leq N$ ，求第 $K$ 大的 $a_i\times b_j +b_j\times c_k + c_k \times a_i$。

$1\leq N \leq 2\times 10^5$，$1\leq K \leq \min(N^3,5\times10^5)$。

#### 解题思路

求第 k 大很容易想到二分，但这道题并不是，因而赛时没有做出来。

定义 $f(i,j,k)=a_i\times b_j +b_j\times c_k + c_k \times a_i$。

将三个序列都降序排序，显然 $f(i,j,k)\geq f(i-1,j,k),f(i,j-1,k),f(i,j,k-1)$。

对于 $K$,枚举出所有 $f(i,j,k)$ 满足 $i\times j\times k \leq K$，然后找出第 $K$ 大的 $f(i,j,k)$ 即可。

### [\[ABC391G\] Many LCS](https://www.luogu.com.cn/problem/AT_abc391_g)

#### 题目大意
有一个长度为 $N$ 的小写英文字符串 $S$。需要统计对于所有可能的长度为 $M$ 的小写英文字符串 $T$，它们与 $S$ 的最长公共子序列长度为 $0,1,2,\dots,N$ 各自为多少。

#### 解题思路

dp of dp，之前并没有做过这类的题目。

回忆计算 $\operatorname{LCS}$ 的过程，注意到状态转移数组 `f` 的差分数组只由 `0` 和 `1` 组成。

对原串 $S$ 的状态进行位压缩，以二进制表示子序列选取情况。

对每个状态 $S$ 和待加入的字母 $x$，使用一个转移函数求出新状态。DP 里再根据已经转移到的子序列与生成的字母数位置，累加结果。

时间复杂度 $O(26 \times (n + m) \times 2^n)$。

这里给出核心代码：

```cpp
for(int i=1;i<=n;i++){
        a[i]=s[i-1]-'a';
    }
    for(int S=0;S<(1<<n);S++){
        for(int i=0;i<26;i++){
            nxt[S][i]=calc(S,i);
        }
    }

    f[0][0]=1;
    for(int i=0;i<m;i++){
        for(int S=0;S<(1<<n);S++){
            for(int j=0;j<26;j++){
                f[nxt[S][j]][i+1]=(f[nxt[S][j]][i+1]+f[S][i])%mod;
            }
        }
    }

```

`calc` 部分略。

### [\[ABC392E\] Cables and Servers](https://www.luogu.com.cn/problem/AT_abc392_e)

#### 题目大意

有 $N$ 台服务器和 $M$ 根电缆，每根电缆连接两台服务器。通过调整电缆的连接方式，使所有服务器连通，求最少的操作次数和具体方案。

#### 解题思路

并查集。

先处理非多余边，构建初始连通块,统计连通块数量，答案就是连通块数-1，使用多余边依次连接未连通的点。

赛时没有场切纯粹因为自己太弱智，交了n发没过。。。

### [\[ABC394F\ Alkane](https://www.luogu.com.cn/problem/AT_abc394_f)

#### 题目大意

给定一棵 $N$ 个点的树，求其包含的最大子树，满足所有点的度数为 $1$ 或 $4$，且至少有一个点度数为 $4$。

#### 解题思路

使用树形 DP 求解。设计状态 `f[u][i][j]` 表示：

- u：当前节点
- i：已选择的边数(0-4)
- j：当前节点是否为度数为4的点(0/1)

其中 `f[u][i][j]` 的值表示满足条件的最大点数。
