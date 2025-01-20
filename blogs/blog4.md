## Atcoder Grand Contest 005

### A - STring

#### 题目大意 

有一个字符串 $X$ ，它的字符数是偶数。其中一半字符为 "S"，另一半字符为 "T"。

现执行以下操作 $10^{10000}$ 次：

- 在 $X$ 中（连续）出现的 `ST` 子串中，删除最左边的一个。如果没有出现，则不做任何操作。

找出 $X$ 的最终长度。

#### 解题思路

简单题，考虑维护一个栈。

扫一遍字符串 $X$，将所有的 "S" 都压进栈，每次遇到一个 "T" 就弹出一个元素。

再维护一个字符串的长度变量，根据栈内元素的变化加减。

```cpp
int ans=0;
for(int i=0;i<n;i++){
    ans++;
    if(s[i]=='S'){
        stk.push(1);
    }
    else if(!stk.empty()){
        stk.pop();
        ans-=2;
    }
}

cout<<ans<<'\n';
```

### B - Minimum Sum

#### 题目大意

有一个长度为 $N$ , $a_1, a_2, ..., a_N$ 的排列组合。

试求： $\sum _{i=1}^{n} \sum _{j=i}^n \min _{i \leq k \leq j} a_{k}$

#### 解题思路

有一个很明显的转换，如果一个数可以成为一个区间的最小值，说明它前面没有比它小的元素，后面也没有比它小的元素。

这看上去是一句废话，但实际上就转化为了维护一个单调栈的问题：

- $l_i$ 表示 $a_i$ 左边能到达最远的比 $a_i$ 大的元素。

- $r_i$ 表示 $a_i$ 右边能到达最远的比 $a_i$ 大的元素。

- 那么最终答案就是 $\sum _{i=1}^{n} (r_i-i)\times (i-l_i) \times a_i$

$l_i$ $r_i$ 就是一个单调栈可以维护的。

```cpp
for(int i=1;i<=n;i++){
    while(!stk.empty()&&a[stk.top()]>a[i]){
        r[stk.top()]=i;
        stk.pop();
    }
    l[i]=stk.empty()?0:stk.top();
    stk.push(i);
}

int ans=0;
for(int i=1;i<=n;i++){
    ans+=(r[i]-i)*(i-l[i])*a[i];
}

cout<<ans<<'\n';
```

### C - Tree Restoring

#### 题目大意

有一个长度为 $N$ , $a_1, a_2, ..., a_N$ 的整数序列,判断是否存在这样一棵树：

树上有 $N$ 个顶点，编号为 $1$ 到 $N$ ，假设每条边的长度为 $1$ ，对于每个 $i = 1,2,...,N$，顶点 $i$ 与离它最远的顶点之间的距离为 $a_i$。

#### 解题思路

考虑将最长距离直接拆成一条链，然后讨论其中点的位置与个数，记录下 $a_i$ 中的最小和最大值，进行极值判断。

还要对中点的个数进行判断，偶数长度的链，有两个中点，奇数长度的链，有一个中点，如果不对，说明不可行。

其次，我们注意到中点两边的点的中点个数应该大于 $2$。

`check` 函数：

```cpp
void check(vector<int> &f,int Max){
	for(int i=(Max+1)/2+1;i<=Max;i++){	
		if(f[i]<2){	
			cout<<"Impossible\n";
			return ;
		}
	}
	cout<<"Possible\n";
}
```

```cpp
int maxn=0,minn=1<<30;

vector<int> a(n+5),f(n+5,0);
for(int i=1;i<=n;i++){
    cin>>a[i];
    f[a[i]]++;
    maxn=max(maxn,a[i]);
    minn=min(minn,a[i]);
}

if(minn<(maxn+1)/2){
    cout<<"Impossible\n";
    return 0;
}

if(maxn&1){						
    if(f[(maxn+1)/2]!=2){		
        cout<<"Impossible\n";	
        return 0;
    }
    check(f,maxn);
}
else {				
    if(f[maxn/2]!=1){			
        cout<<"Impossible\n";
        return 0;
    }
    check(f,maxn);
}
```

### D - ~K Perm Counting

#### 题目大意

有一个长度为 $N$ 的排列，满足以下条件：

- 假设该排列为 $a_1, a_2, ..., a_N$ 。对于每个 $i = 1,2,...,N$ , $|a_i - i| \neq K$ .

在长度为 $N$ 的 $N!$ 个排列中，有多少个满足这个条件？

答案对 $924844033$ 取模。

#### 解题思路

自己做的时候没有想到 dp，只能打了暴力。

正难则反，考虑容斥。

记 $f_i$ 表示至少有 $i$ 个位置不满足条件的方案数，答案为 $\sum _{i=0}^{n} (-1)^i \times f_i$

这里需要用到这条性质：对于每个数，与它的差的绝对值为 $k$ 的数不超过 $2$ 个。

因此，如果再 $x$ 和 $x+k$ 之间连边，就会形成 $k$ 条链，每个点只能和与它有相连的边配对。

```cpp
vector<vector<array<array<int,2>,2> > > f(n+1,vector<array<array<int,2>,2> >(n+1));

int tot=0;
for(int i=1;i<=n;i++){
    if(!vis[i]){
        for(int j=i;j<=n;j+=k){
            vis[j]=1;
            a[++tot]=j;
        }
    }
}

f[0][0][0][0]=1;
a[0]=-(1<<30);

for(int i=1;i<=n;i++){
    f[i][0][0][0]=1;
    for(int j=1;j<=i;j++){
        f[i][j][0][0]=(f[i-1][j][1][0]+f[i-1][j][0][0]+(a[i]-a[i-1]==k)*f[i-1][j-1][0][0])%mod;
        f[i][j][0][1]=(a[i+1]-a[i]==k)*(f[i-1][j-1][1][0]+f[i-1][j-1][0][0])%mod;
        f[i][j][1][0]=(f[i-1][j][0][1]+f[i-1][j][1][1]+(a[i]-a[i-1]==k)*f[i-1][j-1][0][1])%mod;
        f[i][j][1][1]=(a[i+1]-a[i]==k)*(f[i-1][j-1][0][1]+f[i-1][j-1][1][1])%mod;
    }
}

for(int i=0;i<=n;i++){
    int sum=(f[n][i][0][0]+f[n][i][0][1]+f[n][i][1][0]+f[n][i][1][1])%mod;
    if(i&1){
        ans=(ans+mod-sum*fac[n-i]%mod)%mod;
    }
    else{
        ans=(ans+sum*fac[n-i]%mod)%mod;
    }
}

```