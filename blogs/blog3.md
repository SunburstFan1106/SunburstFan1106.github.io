## Atcoder Beginner Contest 237

### C - kasaka

#### 题目大意

给出一个由小写英文字母组成的字符串 $S$ 。请判断在 $S$ 开头添加一定数量的 `a`(可能是零)是否能使其成为一个回文字符串。

#### 解题思路

分别记录字符串 $S$ 的前后连续的`a`的个数，判断去除了这些`a`之后的字符串还是否回文。

**需要注意**：**字符串 $S$ 开头连续的`a`的个数必须小于结尾连续的`a`的个数。**

```cpp
    while(i<len&&s[i]=='a') i++,tot1++;  // i,j为端点，tot1,tot2为个数
    while(j>=0&&s[j]=='a') j--,tot2++;

    string sub=s.substr(i,j-i+1); //生成字串
    string rev=sub; //判断回文
    reverse(rev.begin(),rev.end());

    if(tot2<tot1) cout<<"No\n"; //特判前缀 a 的个数大于后缀 a 的个数
    else if(sub==rev) cout<<"Yes\n";
    else cout<<"No\n";
```

### D - LR insertion

#### 题目大意

有一个序列 $A=(0)$ .  
还有一个长度为 $N$ , $S=s_1; s_2; \ldots s_N;$ 的字符串，由 `L` 和 `R` 组成。

对于这个顺序中的每个 $i=1, 2, \ldots, N$ 都将执行以下操作。

- 如果 $s_i$ 是 "L"，则在 $A$ 中 $i-1$ 的左侧插入 $i$ 。
- 如果 $s_i$ 是 "R"，则在 $A$ 中 $i-1$ 的右边插入 $i$ 。

求 $A$ 的最终内容。

#### 解题思路

考虑维护一个双端队列，先把最后一个元素 $N$ 加进来，然后根据 $S$ 倒着添加元素

```cpp
    q.push_front(n); //前将 n 压进队列
    for(int i=n;i>=1;i--){ //倒序遍历，反向操作
        if(s[i]=='L')q.push_back(i-1); 
        else q.push_front(i-1);
    }

    /*后面正序输出 q 即可*/

```

### E - Skiing

#### 题目大意

一共有 $n$ 个节点，$m$ 条边，每条边都有其权值，我们要计算 1 号节点到其他节点的最长路。

#### 解题思路

考虑按题目意思建边，之后将所有边取反，就转化为了最短路问题

最后答案为：$max(h_1-h_i-low_i)$

本题使用SPFA求最短路会被卡，因此需要用Dij，加一些方式避免负边

建边部分：

```cpp

    for(int i=1;i<=m;i++){
        int u,v;
        cin>>u>>v;
        if(h[u]>=h[v]){ //按照两个端点高度大小关系分类讨论
            G[u].push_back((node){v,h[u]-h[v]}); //产生正贡献的边
            G[v].push_back((node){u,2*(h[v]-h[u])}); //产生负贡献的边
        }
        else{
            G[u].push_back((node){v,2*(h[u]-h[v])});
            G[v].push_back((node){u,h[v]-h[u]});
        }
    }

```

Dij部分：

```cpp
    memset(low,0x3f,sizeof(low));
    priority_queue<node> q;

    low[1]=0;
    q.push((node){1,0});
    while(!q.empty()){
        int u=q.top().to; q.pop();
        if(vis[u])continue;
        
        vis[u]=1;
        for(auto i:G[u]){
            int v=i.to;
            ll w=i.val;

            w*=-1,w+=h[u]-h[v];
            if(low[u]+w<low[v]){
                low[v]=low[u]+w;
                q.push((node){v,-low[v]}); //取相反数跑最短路
            }
        }
    }
```

### F - |LIS| = 3

#### 题目大意

求以 $998244353$ 为模数，满足下列所有条件的序列数。

- 长度为 $N$ 。
- 每个元素都是介于 $1$ 和 $M$ 之间的整数。
- 它的最长递增子序列的长度正好是 $3$ 。

#### 解题思路

考虑 $1\leq m \leq 20$ ，且 LIS 的长度为3，设 $f_{i,u,v,w}$ 表示前 $i$ 个数，LIS 为 ${u,v,w}$ 的序列数。

状态转移：$f_{i,u,v,w} = \sum _{x=1}^{u} f_{i-1,x,v,w} + \sum _{x=u+1}^{v} f_{i-1,u,x,w}+ \sum _{x=v+1}^{w} f_{i-1,u,v,x}$

最终答案为 $\sum _{i=1}^{m} \sum _{j=i+1}^{m} \sum _{k=j+1}^{m} f_{n,i,j,k}$

时间复杂度为 $O(n \cdot m^4)$

```cpp
    f[0][m+1][m+1][m+1]=1;
    for(int i=1;i<=n;i++)
        for(int u=1;u<=m+1;u++)
            for(int v=1;v<=m+1;v++)
                for(int w=1;w<=m+1;w++){
                    for(int j=1;j<=m;j++){
                        if(j<=u){
                            (f[i][j][v][w]+=f[i-1][u][v][w])%=mod;
                        }   
                        else if(j<=v){
                            (f[i][u][j][w]+=f[i-1][u][v][w])%=mod;
                        }
                        else if(j<=w){
                            (f[i][u][v][j]+=f[i-1][u][v][w])%=mod;
                        }
                    }
                }
```

### G - Range Sort Query

#### 题目大意

给定的是 $1,2,\ldots,N$ 的排列 $P=(P_1,P_2,\ldots,P_N)$ 和整数 $X$ 。

此外，还给出了 $Q$ 个查询。 $i$ \-th查询表示为数字 $(C_i,L_i,R_i)$ 的三重。每个查询都会对 perutation $P$ 进行以下操作。

- 如果是 $C_i=1$ ：按升序对 $P_{L_i},P_{L_i+1},\ldots,P_{R_i}$ 排序。
- 如果 $C_i=2$ ：按降序对 $P_{L_i},P_{L_i+1},\ldots,P_{R_i}$ 排序。

按照给定的顺序执行所有查询后，在最终排列 $P$ 中找到 $i$ ，使得 $P_i=X$ .

#### 解题思路

**考虑转化问题，将序列中大于 $k$ 的元素赋值为1，将序列中小于 $k$ 的元素赋值为0 。**

- 升序操作：

设区间 $[l,r]$ 中有 $a$ 个 1 。

将 $[l,l+a]$ 中的所有元素全部赋值为 1，将 $[l+a+1,r]$ 中的所有元素全部赋值为 0 。

- 降序操作：

设区间 $[l,r]$ 中有 $a$ 个 0 。

将 $[l,l+a]$ 中的所有元素全部赋值为 0，将 $[l+a+1,r]$ 中的所有元素全部赋值为 1 。

**动态维护 k 的位置，每一次升序/降序操作，判断 k 当前位置是否在 $[l,r]$ 内，如果在，那么它的位置就会变为 $[l,r]$ 中 0和1 的分界点**

考虑使用线段树维护区间推平（用于赋值0和1），区间求和（用于统计a）

线段树：

```cpp

    struct Sgt_Tree{
        /* ... */
        void make_tag(int rt,int x){
            xds[rt]=(rs[rt]-ls[rt]+1)*x;
            tag[rt]=x;
        }

        void push_down(int rt){
            if(tag[rt]==-1)return;
            make_tag(rt<<1,tag[rt]);
            make_tag(rt<<1|1,tag[rt]);
            tag[rt]=-1;
        }

        void update(int rt,int L,int R,int x){ //区间推平
            if(L>R)return;
            if(L<=ls[rt]&&rs[rt]<=R){
                make_tag(rt,x);
                return;
            }

            push_down(rt);
            int md=(ls[rt]+rs[rt])>>1;
            if(L<=md)update(rt<<1,L,R,x);
            if(R>md)update(rt<<1|1,L,R,x);

            push_up(rt);
            return;
        }

        int query(int rt,int L,int R){ //区间查询
            if(L<=ls[rt]&&rs[rt]<=R)return xds[rt];
            
            push_down(rt);

            int md=(ls[rt]+rs[rt])>>1,res=0;
            if(L<=md)res+=query(rt<<1,L,R);
            if(R>md)res+=query(rt<<1|1,L,R);

            return res;
        }

    }Tr;

```

主函数部分：

```cpp
    //pos 表示 k 所在的位置
    Tr.build(1,1,n,k);
    while(m--){
        int opt,l,r;
        cin>>opt>>l>>r;

        if(opt==1){
            int a=Tr.query(1,l,r); //[l,r]的和，即为1的个数
            if(l<=pos&&pos<=r){ //动态维护，将位置更新为分界点
                pos=l+a-1；
            }
            Tr.update(1,l,l+a-1,1); //升序操作
            Tr.update(1,l+a,r,0);
        }
        else{
            int a=(r-l+1)-Tr.query(1,l,r); //总长度减去1的个数
            if(l<=pos&&pos<=r){
                pos=l+a;
            }
            Tr.update(1,l,l+a-1,0); //降序操作
            Tr.update(1,l+a,r,1);
        }
    }
```