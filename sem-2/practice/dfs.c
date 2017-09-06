#include<stdio.h>
#include<stdlib.h>
typedef struct node{
	int num;
	struct node* next;
} node;
typedef struct adlist{
	node* head;

} adlist;
adlist arr[10000];
int vis[10000];
node* new(int n)
{
	node* newnode = (node*)malloc(sizeof(node));
	newnode -> num = n;
       	newnode -> next =NULL;
	return newnode;	
}

void addedge(int src,int dest)
{
	node* newnode = new(dest);
	newnode -> next = arr[src].head;
	arr[src].head = newnode;

}
void creategraph(int vert)
{
	int i;
	for(i=0;i<=vert;i++)
		arr[i].head = NULL;
}
void printgraph(int vert)
{
	int i;
	for(i=1;i<=vert;i++)
		{
			node* crawl = arr[i].head;
			while(crawl)
			{
				printf(" -> %d",crawl->num);	
				crawl = crawl -> next;
				}
			printf("\n");
			}
}
void dfs(int vert,int src)
{
	vis[src] = 1;
	printf("%d ->",src);
	node* crawl = arr[src].head;
	while(crawl)
	{
		if(vis[crawl -> num] == 0)
			dfs(vert ,crawl -> num);
		else
		{}
		crawl = crawl -> next;
			}

}
int main()
{
	int vert;
	printf("enter the number of vertices\n");
	scanf("%d",&vert);
	creategraph(vert);
	int m;
	scanf("%d",&m);
	int i;
	for(i=0;i<m;i++)
		{
			int src,dest;
			scanf("%d %d",&src,&dest);
			addedge(src,dest);
			
			}
	//printgraph(vert);
	for(i=1;i<=vert;i++)
		{
			if(vis[i] == 0)
				{
					dfs(vert,i);
					}
			else
			{
				printf("\n");
				}
		}
	return 0;
}
