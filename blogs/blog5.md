## Atcoder Grand Contest 010

### A - Addition

#### 题目大意

黑板上写着 $N$ 个整数。

对这些数字进行以下运算：

- 选择一对奇偶性相同的数 $A_i$ 和 $A_j$ 擦除。
- 然后，在黑板上写一个新的数，等于这两个数之和 $A_i+A_j$ 。

问黑板上是否可能只有一个数。

#### 解题思路

我们知道，一个数加上一个偶数后不会改变奇偶性，因此只需要看序列中有多少个奇数即可。

显然，当奇数的个数为奇数时，不能删的只剩一个数，否则一定可行。

### B - Boxes

#### 题目大意

$N$个数字$A_i$（顺时针给出）构成一个环，每次可以从一个起点出发顺时针给这个环依次$-1$、$-2$ .... $-n$。问是否存在一种方案使得能把所有数恰好都减成$0$。

#### 解题思路

首先注意到：如果这个环能够被完全删除，那么其操作的次数 $p = \frac {2 \times \sum _{i=1}{n} a_i}{n \times (n+1)}$。

因此第一个判断：$2\times sum $ 能否被 $n\times (n-1) $ 整除。

看到减去的序列是 $-1$、$-2$ .... $-n$，考虑差分。

记 $d_i = a_{i\%n +1} -a_i$。

每次操作， $d_i$ 的变化一定是有 $n-1$ 个 $d_i++$ 和 $1$ 个 $$d_i+=1-n$。

设对于每个元素 $i$，从 $i$ 开始的删除操作次数有 $x_i$ 次。

那么：$d_i = (p-x_i)\times 1 - (n-1)\times x_i = p-n\times x_i$。

移项后得： $x_i = \frac {p-d_i}{n}$。

显然， $x_i$ 一定是一个非负整数，所以对于每个 $i$，判断 $p \geq d_i$ 和 $n \mid p-d_i$ 即可。


``` cpp
vector<ll> a(n+1);
for(int i=1;i<=n;i++){
    cin>>a[i];
    sum+=a[i];
}

if(sum%((ll)n*(n+1)/2ll)){
    cout<<"NO\n";
    return 0;
}
ll p=sum/((ll)n*(n+1)/2ll);

vector<ll> d(n+1);
for(int i=1;i<=n;i++){
    d[i]=a[i%n+1]-a[i];
    if(d[i]>p||(p-d[i])%n){
        cout<<"NO\n";
        return 0;
    }
}
cout<<"YES\n";

```


### C - Cleaning

#### 解题思路

考虑对每个点处理它所有的儿子连上来的路径要不就是在当前子树内两两匹配，要不就是继续连到该点的父亲。

如果在子树内匹配，儿子两个儿子的石子数量减一，该节点的石子数量减一；对于连上去的，某个儿子的石子数量减一，该节点的石子数量减一。

所以设某节点处理完子树之后还要往父亲连 $f_x$ 条路径，有 $y$ 条路径在它的子树内互相匹配，它的子树内一共有条路径，它本身权值为 $a_x$ 那么有：

$2 \times y + f_x = sum$ ，$y+f_x=a_x$

由此得到 $y=sum-a_x,f_x=sum-2 \times y$

首先连上去的路径个数肯定不能超过它本身的权值 $a_x$，即 $f_x\leq a_x$；也不可以是负数，即 $f_x\geq 0$。

其次它的子树内部最多的两两互相匹配的路径个数要比需要的两两匹配的路径条数多，而这个最大值就是 $max(\frac {sum}{2},sum-max_{f_v})$，首先两两匹配最多就是 $\frac {sum}{2}$，每个点不能和自己匹配，所以还要和 $sum-max_{f_v}$ 取最小值。

注意 $f_root$ 必须是 $0$，因此根节点无法向上传递。

$N=2$ 的情况要特判。

``` cpp
void dfs(int u,int fa,vector<int> &a,vector<vector<int> > &G,vector<int> &d,vector<int> &f){
    f[u]= d[u]==1? a[u] : 2*a[u];
    for(auto v:G[u]){
        if(v==fa)continue;
        dfs(v,u,a,G,d,f);
        f[u]-=f[v];
        if(f[v]>a[u]){
            cout<<"NO\n";
            exit(0);
        }
    }
    if(f[u]>a[u]||f[u]<0){
        cout<<"NO\n";
        exit(0);
    }
}
```