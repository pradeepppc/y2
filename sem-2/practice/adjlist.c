#include<stdio.h>
#include<stdlib.h>
typedef struct node{
	int num;
	struct node*  next;
} node;
typedef struct adjlist{
	struct node* head;	
} adjlist;
adjlist arr[10000];
node* new(int n)
{
	node* newnode =(node*)malloc(sizeof(node));
	newnode -> num = n;
       	newnode -> next = NULL;	
	return newnode;
}
void creategraph(int vert){
	int i;
	for(int i=0;i<vert;i++)
	{
		arr[i].head = NULL;
		}
}
void addedge(int src,int dest)
{
	node* newnode = new(dest);
	newnode -> next = arr[src].head;
	arr[src].head = newnode;
	
	// since it is undirected graph add from both sides
	newnode = new(src);
	newnode -> next = arr[dest].head;
	arr[dest].head = newnode;	
}
void printgraph(int v)
{
		int i;
		for(i=0;i<v;i++)
			{
				node* crawl = arr[i].head;
				while(crawl)
						{
							printf(" -> %d" , crawl -> num);
							crawl = crawl -> next;
							}
				printf("\n");
				}

		}
int main()
{
	int v;
	printf("enter the number of vertices");
	scanf("%d",&v);
	creategraph(v);
	addedge(0,1);
	addedge(1,2);
	addedge(3,5);
	addedge(1,5);
	addedge(2,5);
	addedge(3,4);
	addedge(4,5);
	addedge(2,3);
	printgraph(v);	
	return 0;
}

