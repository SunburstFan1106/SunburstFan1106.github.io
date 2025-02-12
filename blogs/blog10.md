# [COCI 2024/2025 #2] 差异

## 题目大意

给定三个正整数 $n，m，k$，以及两个周期为 $n,m$ 的无线整数序列 $a$ 和 $b$。构造无限序列 $c$，求： $\sum _{i=1}^{k} c_i=a_i \oplus b_i$

## 解题思路

读题可以发现 $c$ 的循环节长度为 $\text lcm(n,m)$，那么就有一个 $O(\text lcm(n,m))$ 的暴力，可以获得 57pts。

考虑优化这个暴力，不难想到拆位计算贡献，对于每一个二进制位，先求出在周期内的贡献，再求出周期外的散段的贡献。

可以手模一下计算 $c$ 的过程，不难发现，对于序列 $a$ 中的元素 $a_i$，第一个与其进行异或运算的序列 $b$ 元素一定是 $b_i$，第二个则是 $b_{(i+n) \mod m}$，以此类推。

如果将这些元素全部一一建边，最终一定会形成一个环，且环的长度是 $\frac {m}{\gcd(n,m)}$。

考虑将这些环一个个存下来，然后跑一下环上前缀和，就可以开始统计贡献：

计算出周期的个数 $c$ 和剩余长度 $rst$。

- 如果 $a_i=0$，则对应的 $b$ 序列中该位的贡献就是整个环的总和乘 $c$，$rst$ 的贡献可以通过前缀和相减得到。

- 如果 $a_i=1$，则产生的贡献就是 $b$ 序列中该位 $0$ 的个数，即将总环长减去环的总和乘 $c$，$rst$ 的贡献就是拿 $rst$ 减去这一段的和得到。

统计完一位的贡献后乘上 $2^bit$，$bit$ 为当前位数，全部加起来就是答案。

**核心代码**：

这里给出计算每一位贡献的函数 `calc`。

```cpp
vector<int> p(2e5+5,0);
int calc(vector<int> &a,vector<int> &b){
    vector<vector<int> >cir(2e5+5,vector<int>(1));
    
    int GCD=__gcd(n,m),t=m/GCD;
    for(int i=0;i<GCD;i++){
        int head=i;
        for(int j=0;j<t;j++){
            p[head]=j+1; //记录该位对应的编号
            cir[i].push_back(b[head]); //记录这个环
            head=(head+n)%m; //更新指针
        }
        for(int j=0;j<t;j++){
            cir[i].push_back(cir[i][j+1]); //将环复制一遍，方便跑前缀和
        }
        for(int j=1;j<cir[i].size();j++){
            cir[i][j]=(cir[i][j]+cir[i][j-1])%mod; //计算前缀和
        }
    }

    int res=0;
    for(int i=0;i<n;i++){
        if(i>k)break;

        int x=p[i%m]; //找到编号
        int c=(k-i)/(n*t)%mod,rst=(k-i)%(n*t);
        // 算出 c 和 rst
        rst=(rst+n-1)/n; //向上取整
        if(a[i]==0){ //计算贡献部分，可以对照解题思路
            res=(res+c*cir[i%GCD][t]%mod)%mod;
            res=(res-cir[i%GCD][x-1]+cir[i%GCD][x+rst-1]+mod)%mod;
        }
        else{
            res=(res+c*(t-cir[i%GCD][t])%mod)%mod;
            res=(res+rst+cir[i%GCD][x-1]-cir[i%GCD][x+rst-1]+mod)%mod;
        }
    }

    return res;
}
```