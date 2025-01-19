### 不说闲话

概率和期望一直是自己非常薄弱的板块，最早学的时候其实就没有完全听懂。

导致打模拟赛，甚至是 ABC 的时候遇到概率期望相关的题基本上都是绕道走，有时候暴力都打不出来。

重修一下概率论，接下来是做题笔记，后面也会整理成讲题。

### [P1365 WJMZBMR打osu! / Easy](https://www.luogu.com.cn/problem/P1365)

期望入门题。

#### 题目大意

有一个长度为 $N$ 的字符串，由 `o`，`x` 和 `?` 组成。

定义总分数为：字符串中每一段最长连续 `o` 字串长度的平方和。

`?` 的含义是该字符不确定，是 `o` 或 `x`，各有 $50 \%$ 的可能性。

求总分数的期望值。

#### 解题思路

很容易想到 dp。

- 设 $f_i$ 表示前 $i$ 个字符分数的期望值；
- 设 $g_i$ 表示前 $i$ 个字符中以 $i$ 为最后一个字符的连续 `o` 字串的期望长度。

接下来就可以分类讨论进行状态转移：

##### 

$\begin{cases} s_i=o \begin{cases} f_i= f_{i-1}+ 2\times g_{i-1} +1 \\ g_i=g_{i-1}+1 \end{cases}\\ \\ s_i=x \begin{cases} f_i= f_{i-1} \\ g_i=0 \\ \end{cases}\\ \\ s_i=?\ \ \begin{cases} f_i=f_{i-1}+g_{i-1}+0.5 \\ g_i=0.5\times g_{i-1} + 0.5  \end{cases}\\ \end{cases}$

时间复杂度 $O(N)$

后续的相关练习：

### [P4927 [1007] 梦美与线段树](https://www.luogu.com.cn/problem/P4927)

恶心题，式子并不难推，但是代码有一点繁琐。

#### 题目大意

有一颗线段树，每次按节点权值的占比的概率进入该子树，求走过的权值和的期望值。

#### 解题思路

令当前节点为 $rt$，则不难看出进入 $rt$ 左子树的期望为：

$sum_l \times P(l) = sum_l \times \frac {sum_l}{sum_{rt}} = \frac {sum_l^2}{sum_{rt}}$。

同理，进入 $rt$ 右子树的期望为：

$sum_r \times P(r) = sum_r \times \frac {sum_r}{sum_{rt}} = \frac {sum_r^2}{sum_{rt}}$。

那么就可以得出 $rt$ 节点走过的权值和的期望值为：$\frac {sum_l^2+sum_r^2}{sum_{rt}}$。

下半部分是很好维护的，仅需要维护区间和的线段树即可，而不难看出上半部分就是一个维护区间平方和。

怎么维护呢？考虑每次更新，设增加的数值为 $\Delta V$。

那么 $rt$ 节点的平方和就成为了 $(sum_{rt} + len_{rt} \times \Delta V)^2$。

考虑完全平方公式展开：

$(sum_{rt} + len_{rt} \times \Delta V)^2 = {sum_{rt}^2 + 2 \times len_{rt} \times sum_{rt} \times \Delta V + len_{rt}^2} \times {\Delta V}^2 $。

$len$ 和 ${len}^2$ 都可以在线段树的 `build` 阶段维护。

那么我们只需要知道如何维护 $len_{rt} \times sum_{rt}$，这道题就做完了。

每次更新，$len_rt \times sum_{rt}$ 就会变成 $len_{rt} \times (sum_{rt} + len_{rt} \times \Delta V)$

再拆开来：

$len_{rt} \times sum_{rt} + len_{rt}^2 \times \Delta V$。

所以每次更新，$len_{rt} \times sum_{rt}$ 只需要加上 $len_{rt}^2 \times \Delta V$ 即可， $len^2$ 前边已经说过如何维护了。

乍一看，这棵线段树要维护的东西似乎有点多，比较繁琐。

线段树部分代码：

```cpp
struct Sgt_Tree{
    #define lson rt<<1,l,md
    #define rson rt<<1|1,md+1,r

    int sum[N<<2],sum_2[N<<2];
    int len[N<<2],len_2[N<<2]; 
    int len_sum[N<<2],tag[N<<2];

    void push_up(int rt,int l,int r){
        sum[rt]=sum[rt<<1]+sum[rt<<1|1];
        sum_2[rt]=sum_2[rt<<1]+sum_2[rt<<1|1]+sum[rt]*sum[rt];
        len_sum[rt]=len_sum[rt<<1]+len_sum[rt<<1|1]+(r-l+1)*sum[rt];
    }
    void build(int rt,int l,int r){
        if(l==r){
            sum[rt]=a[l];
            len[rt]=1,len_2[rt]=1;
            sum_2[rt]=sum[rt]*sum[rt];
            tag[rt]=0;
            len_sum[rt]=sum[rt];
            return;
        }

        int md=(l+r)>>1;
        build(lson);build(rson);
        len[rt]=(len[rt<<1]+len[rt<<1|1]+(r-l+1))%mod;
        len_2[rt]=(len_2[rt<<1]+len_2[rt<<1|1]+(r-l+1)*(r-l+1))%mod;
        push_up(rt,l,r);
    }
    
    void make_tag(int rt,int len,int x){
        tag[rt]+=x;
        sum_2[rt]=sum_2[rt]+2*len_sum[rt]*x;
        sum_2[rt]=sum_2[rt]+len_2[rt]*x*x;
        len_sum[rt]+=len_2[rt]*x;
        sum[rt]+=len*x;  
    }
    void push_down(int rt,int l,int r){
        if(tag[rt]){
            int md=(l+r)>>1;
            make_tag(rt<<1,md-l+1,tag[rt]);
            make_tag(rt<<1|1,r-md,tag[rt]);
        }
        tag[rt]=0;
    }
    void update(int rt,int l,int r,int L,int R,int x){
        if(L<=l&&r<=R){
            make_tag(rt,r-l+1,x);
            return ;
        }

        push_down(rt,l,r);

        int md=(l+r)>>1;        
        if(L<=md)update(lson,L,R,x);
        if(R>md)update(rson,L,R,x);
        
        push_up(rt,l,r);
    }

}Tr;
```

[P3317 [SDOI2014] 重建](https://www.luogu.com.cn/problem/P3317)

[P5405 [CTS2019] 氪金手游](https://www.luogu.com.cn/problem/P5405)

[P2081 [NOI2012] 迷失游乐园](https://www.luogu.com.cn/problem/P2081)