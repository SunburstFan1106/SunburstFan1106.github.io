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