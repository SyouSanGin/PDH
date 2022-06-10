#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int _read(void){
    int x=0;
    int ch=getchar();
    while(ch<'0'||ch>'9'){
        ch=getchar();
    }
    while(ch>='0'&&ch<='9'){
        x=x*10+ch-48;
        ch=getchar();
    }
    return x;
}
struct vedio{
    char av[50];
    double score;
    int view,danmaku,favorite,coin,share,like;
}a[50000],b[50000];
char add[]="_information.txt";

void sort(int l,int r){
    if(l==r) return;
    int mid=(l+r)/2;
    sort(l,mid);sort(mid+1,r);
    int i=l,j=mid+1,tmp=i;
    while(i<=mid&&j<=r){
        if(a[i].score>a[j].score){
            b[tmp++]=a[i++];
        }
        else{
            b[tmp++]=a[j++];
        }
    }
    while(i<=mid){
        b[tmp++]=a[i++];
    }
    while(j<=r){
        b[tmp++]=a[j++];
    }
    for(int i=l;i<=r;i++){
        a[i]=b[i];
    }
}

int main(int argc, const char * argv[]) {
    int n=0;
    freopen("list.txt","r",stdin);
    while(scanf("%s",a[n].av)!=EOF){
        n++;
    }
    for(int i=0;i<n;i++){
        char tmp[50];
        memset(tmp,0,50);
        for(int j=0;j<strlen(a[i].av);j++){
            tmp[j]=a[i].av[j];
        }
        for(int j=0;j<strlen(add);j++){
            tmp[strlen(tmp)]=add[j];
        }
        freopen(tmp,"r",stdin);
        a[i].view=_read();
        a[i].danmaku=_read();
        a[i].favorite=_read();
        a[i].coin=_read();
        a[i].share=_read();
        a[i].like=_read();
        a[i].score=log10(a[i].view)/8*0.2+log10(a[i].favorite)/7*0.2+log10(a[i].coin)/6*0.3+log10(a[i].like)/6*0.3;
    }
    sort(0,n-1);
    freopen("result.txt","w",stdout);
    for(int i=0;i<n;i++){
        printf("%s\n",a[i].av);
    }
    return 0;
}