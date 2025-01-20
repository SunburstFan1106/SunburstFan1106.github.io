## Atcoder Grand Contest 018

### B - Sports Festival

#### 题目大意 

有 $N$ 个人参加 $M$ 个项目的运动会，这 $M$ 可以至多被删去 $M-1$ 个。

第 $i$ 个人会参加序列 $a_i$ 中第一个可以被参加的项目 $a_{i,j}$。

现在要使参加人数最多的项目人数最少，求这个最小人数。

#### 解题思路

显然，删去 $M-1$ 个项目一定是最优的。

$N$ 和 $M$ 都比较小，考虑直接贪心并模拟：

- 最开始假设所有的 $M$ 个项目全部设立。
- 求出每个项目的人数，然后将人数最多的项目删去，知道只剩一个项目位置。

这样的策略显然是最优的。

时间复杂度 $O(N \times M)$，直接按照该策略模拟即可。

```cpp
int n,m;
cin>>n>>m;

vector<int> rk(n+5); //每个人当前会参加的项目
vector<vector<int> > a(n+5,vector<int>(m+5));
for(int i=1;i<=n;i++){
    for(int j=1;j<=m;j++){
        cin>>a[i][j];
    }
    rk[i]=1; //最开始一个都没有删除
}

int ans=1<<30;
vector<bool> deleted(m+5);

while(114514){
    int loc=0,maxn=0;
    vector<int> cnt(m+5,0);

    for(int i=1;i<=n;i++){
        while(deleted[a[i][rk[i]]])rk[i]++; //更新 rk
        if(a[i][rk[i]]==0)continue; 

        cnt[a[i][rk[i]]]++; //贡献人数加一
        if(cnt[a[i][rk[i]]]>maxn){ //更新人数最多的项目
            maxn=cnt[a[i][rk[i]]];
            loc=a[i][rk[i]];
        }
    }
    if(!maxn)break; //如果 maxn 为0，代表删的一个项目不剩了

    deleted[loc]=1;
    ans=min(ans,maxn);
    for(int i=1;i<=n;i++){
        if(a[i][rk[i]]==loc)rk[i]++;
    }
}

cout<<ans<<"\n";
```

### C - Coins

#### 题目大意

有 $X+Y+Z$ 个人，编号为 $1$ 到 $X+Y+Z$ 。人 $i$ 有 $A_i$ 枚金币、 $B_i$ 枚银币和 $C_i$ 枚铜币。

斯努克想从 $X$ 人那里得到金币，从 $Y$ 人那里得到银币，从 $Z$ 人那里得到铜币。从一个人身上不可能得到两种或两种以上不同颜色的硬币。另一方面，一个人会把斯努克指定颜色的硬币全部给他/她。

斯努克希望最大限度地增加他得到的所有颜色硬币的总数。请找出最大可能的硬币数量。

#### 解题思路

贪心好题。

首先三种 $X,Y,Z$ 个数有点多，考虑先将答案加上 $\sum c_i$。

然后将 $a_i$，$b_i$ 减去 $c_i$，问题就转化为了两部分。

假定当前已经找出了最优的 $z$ 个人，那么怎样才能筛出最优的 $x$ 个人？

显然是按照 $a_i-b_i$ 由大到小排序。

对于所有人，全部先减去 $c_i$ 后按照 $a_i-b_i$ 排序，然后再用两个优先队列维护即可。

```cpp
#include<bits/stdc++.h>
using namespace std;

#define ll long long

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);cout.tie(0); 

    int x,y,z;
    cin>>x>>y>>z;

    ll sumc=0;
    int n=x+y+z;
    
    vector<ll> id(n+5);
    vector<ll> a(n+5),b(n+5),c(n+5);
    
    for(int i=1;i<=n;i++){
        cin>>a[i]>>b[i]>>c[i];
        id[i]=i,sumc+=c[i];
    }

    sort(id.begin()+1,id.begin()+n+1,[&](ll x,ll y){
        return a[x]-b[x]>a[y]-b[y];
    });

    vector<ll> f(n+5,0),g(n+5,0);
    priority_queue<ll> pa,pb;

    f[0]=g[n+1]=0;
    for(int i=1;i<=n;i++){
        pa.push(c[id[i]]-a[id[i]]);
        f[i]=f[i-1]-c[id[i]]+a[id[i]];
        if(pa.size()>x){
            f[i]+=pa.top();
            pa.pop();
        }
    }

    for(int i=n;i>=1;i--){
        pb.push(c[id[i]]-b[id[i]]);
        g[i-1]=g[i]-c[id[i]]+b[id[i]];
        if(pb.size()>y){
            g[i-1]+=pb.top();
            pb.pop();
        }
    }

    ll ans=-1ll<<60;
    for(int i=x;i<=n-y;i++){
        ans=max(ans,sumc+f[i]+g[i]);
    }

    cout<<ans<<"\n";

    return 0;
}
```