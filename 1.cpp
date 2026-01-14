#include<iostream>
#include <vector>
#include<queue>

using namespace std;

class Graph
{
private:
    int V;
    int E;
    vector<vector<pair<int,int>>> adj;
public:
    Graph(int v,int e)
    {
        V=v;E=e;
        int first,second,weight;
        adj.resize(V+1);
        for (int i=0;i<E;i++)
        {
            cin>>first>>second>>weight;
            adj[first].push_back({second,weight});
        }
    }
    void printGraph()
    {
        for (int i=1;i<V+1;i++)
        {
            cout<<i<<"=";
            for (auto j:adj[i])
            {
                cout<<j.first<<" "<<j.second<<" ";
            }
            cout<<endl;
        }
    }

    int djikstra(int src)
    {
        vector<int> nocoupondist(V+1,INT_MAX);
        vector<int> coupondist(V+1,INT_MAX);
        nocoupondist[src]=0;
        priority_queue<vector<int>,vector<vector<int>>,greater<vector<int>>> pq;
        pq.push({0,src,0});
        while (!pq.empty())
        {
            vector<int> top= pq.top();
            pq.pop();
            int currentdistance=top[0];
            int u=top[1];
            int coupon=top[2];
            if (coupon==0&&currentdistance!=nocoupondist[u]) continue;
            if (coupon==1&&currentdistance!=coupondist[u]) continue;
            for (auto edge:adj[u])
            {
                int v=edge.first;
                int w=edge.second;
                if (coupon==0&&nocoupondist[u]+w<nocoupondist[v])
                {
                    nocoupondist[v]=nocoupondist[u]+w;
                    pq.push({nocoupondist[v],v,0});
                }
                if (coupon==1&&coupondist[u]+w<coupondist[v])
                {
                    coupondist[v]=coupondist[u]+w;
                    pq.push({coupondist[v],v,1});
                }
                if (coupon==0&&nocoupondist[u]+w/2<coupondist[v])
                {
                    coupondist[v]=nocoupondist[u]+w/2;
                    pq.push({coupondist[v],v,1});
                }
            }
        }
        if (nocoupondist[V]<nocoupondist[V]) return nocoupondist[V];
        return coupondist[V];
    }
    // int djikstra(int src) //normal djikstra
    // {
    //     vector<int> dist(V+1, INT_MAX);
    //     dist[src]=0;
    //     priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
    //     pq.push({0, src});
    //     while (!pq.empty())
    //     {
    //         pair<int,int> top=pq.top();
    //         u=top.first;
    //         d=top.second;
    //         pq.pop();
    //         if (d!=dist[u]) continue;
    //         for (auto edge:adj[u])
    //         {
    //             int v=edge.first;
    //             int w=edge.second;
    //             if (dist[u]+w<dist[v])
    //             {
    //                 dist[v]=dist[u]+w;
    //                 pq.push({dist[v],v});
    //             }
    //         }
    //     }
    //     return dist[V];
    // }
    // int halfEdgeDjikstra(int src) //shob edge aladavabe halve kore
    // {
    //     int mincost=djikstra(src);
    //     for (int u=1;u<=V;u++)
    //     {
    //         for (int j=0;j<adj[u].size();j++)
    //         {
    //             int puran=adj[u][j].second;
    //             adj[u][j].second=puran/2;
    //             int notun=djikstra(src);
    //             minCost=min(minCost,notun);
    //             adj[u][j].second=puran;
    //         }
    //     }
    //     return minCost;
    // }
};
int main()
{
    int v,e;
    cin>>v>>e;
    Graph g(v,e);
    //g.printGraph();
    cout<<g.djikstra(1)<<endl;
    return 0;
}
