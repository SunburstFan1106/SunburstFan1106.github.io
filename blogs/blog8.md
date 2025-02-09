# Atcoder Beginner Contest 392


## D - Doubles

### 题目大意

给定 $N$ 个骰子，每个骰子有不同数量的面，每个面上写着一个数字。选择两个骰子，同时掷出，计算两个骰子出现相同数字的概率。目标是找到选择哪两个骰子能使这个概率最大，并输出这个最大的概率。

### 解题思路

注意到数据范围中有一条 $K_1 + K_2 + \dots + K_N \leq 10^5$。

考虑使用 `unordered_map` 统计每个骰子各数字出现的频率，遍历每个骰子对，计算相同数字出现的概率之和，取最大值就是答案。

### 核心代码

```cpp
vector<unordered_map<int,int>> freq(n+1);
for(int i=1;i<=n;i++){
    for(int j=1;j<=k[i];j++){
        freq[i][a[i][j]]++;
    }
}

double ans=0.0;
for(int i=1;i<=n;i++){
    for(int j=i+1;j<=n;j++){
        double prob = 0.0;
        for(auto &p:freq[i]){
            int num=p.first;
            int cnt_i=p.second;
            if(freq[j].count(num)){
                int cnt_j=freq[j][num];
                prob+=((double)cnt_i/k[i])*((double)cnt_j/k[j]);
            }
        }
        ans=max(ans,prob);
    }
}

```

## F - Insert

### 题目大意

给定一个空数组 $A$，依次进行 $N$ 次插入操作。第 $i$ 次操作将数字 $i$ 插入到数组 $A$ 的第 $P_i$ 个位置（从 $1$ 开始计数）。输出最终的数组 $A$。

### 解题思路

使用树状数组维护数组 $A$ 的空位信息，快速找到插入位置。

对于**插入操作：** 每个 $i$ 从 $N$ 到 $1$，使用树状数组 `findKth` 操作，找到第 $P_i$ 个空位在数组 $A$ 中的位置 $pos$，将数字 $i$ 插入到数组 $A$ 的位置 $pos$，在树状数组中，将位置 $pos$ 的值更新为 $0$，表示该位置已被占用。

时间复杂度为 $O(N \times \log N)$，空间复杂度为 $O(N)$。

### 核心代码

```cpp
struct Fenwick{
    int n;
    vector<int> c;

    Fenwick(int n):n(n),c(n+1,0){}

    ...
    int findKth(int k){ //查找第 k 个空位操作
        int pos=0,bit=1<<20;
        for(;bit;bit>>=1){
            int nxt=pos+bit;
            if(nxt<=n&&c[nxt]<k){
                k-=c[nxt];
                pos=nxt;
            }
        }
        return pos+1;
    }
};

int main(){
    ...

    vector<int> ans(n+1,0);

    Fenwick t(n);
    for(int i=1;i<=n;i++)
        t.update(i,1);

    for(int i=n;i>=1;i--){
        int pos=t.findKth(P[i]);
        ans[pos]=i;
        t.update(pos,-1);
    }

    for(int i=1;i<=n;i++)
        cout<<ans[i]<<" ";
    cout<<"\n";

    return 0;
}
```
## G - Fine Triplets

### 题目大意

给定一个包含 $N$ 个不同正整数的集合 $S$。

如果三个整数 $A, B, C (A < B < C)$ 满足 $B - A = C - B$，则称 $(A, B, C)$ 为一个“好三元组”。

求集合 $S$ 中有多少个好三元组。

### 解题思路

利用 FFT 加速卷积运算，快速统计。

使用 FFT 计算数组 $f$ 与自身的卷积，得到数组 $conv$。数组 $conv$ 的第 $i$ 个元素表示集合 $S$ 中有多少对数字 $(x, y)$ 满足 $x + y = i$。

遍历集合 $S$ 中的每个元素 $b$。

对于每个元素 $b$，计算 $2 \times b$ 的值。

如果 $2\times b$ 小于数组 $conv$ 的大小，则 $conv_{2\times b}$ 表示集合 $S$ 中有多少对数字 $(x, y)$ 满足 $x + y = 2\times b$。

由于 $x$ 和 $y$ 可以相同，因此需要减去 $1$（即 $x = y = b$ 的情况）。

由于 $(x, y)$ 和 $(y, x)$ 算作同一种情况，因此需要除以 $2$。

每次计算完之后将结果累加到 `ans` 中。

时间复杂度 $O(m \times \log m)$

#### 核心代码

```c++
void FFT(vector<db>&a,bool invert){
    int n=a.size();

    for(int i=1,j=0;i<n;i++){
        int bit=n>>1;
        for(;j&bit;bit>>=1)j-=bit;
        j+=bit;
        if(i<j)swap(a[i],a[j]);
    }

    for(int len=2;len<=n;len<<=1){
        double ang=2*PI/len*(invert?-1:1);
        db wlen(cos(ang),sin(ang));

        for(int i=0;i<n;i+=len){
            db w=1;

            for(int j=0;j<len/2;j++){
                db u=a[i+j],v=a[i+j+len/2]*w;

                a[i+j]=u+v;
                a[i+j+len/2]=u-v;
                w*=wlen;
            }
        }
    }
    if(invert)for(db&x:a)x/=n;
}

vector<ll> calc(vector<int>&a,vector<int>&b){
    vector<db> fa(a.begin(),a.end()),fb(b.begin(),b.end());

    int n=1;
    while(n<(int)(a.size()+b.size()-1))n<<=1;

    fa.resize(n);fb.resize(n);

    FFT(fa,0);FFT(fb,0);
    for(int i=0;i<n;i++)fa[i]*=fb[i];
    FFT(fa,1);

    vector<ll> res(n);
    for(int i=0;i<n;i++)res[i]=(ll)round(fa[i].real());

    return res;
}

int main(){
    ...
    
    int m=*max_element(s.begin(),s.end());

    vector<int>f(m+1,0);
    for(int x:s)f[x]=1;
    
    vector<ll>conv=calc(f,f);
    
    ll ans=0;
    for(int b:s){
        int idx=2*b;
        if(idx<conv.size())ans+=(conv[idx]-1)/2;
    }
    
    ...
}
```
