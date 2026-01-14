#include<iostream>
#include<vector>
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
            adj[first+1].push_back({second+1,weight});
            // adj[second].push_back({first,weight});
        }
    }
    explicit Graph(const vector<vector<pair<int,int>>>& adjList)
    {
        V = adjList.size();        // number of vertices (0-based)
        E = 0;
        adj.resize(V + 1);         // we still use 1-based internally

        for (int u = 0; u < V; u++)
        {
            for (auto edge : adjList[u])
            {
                int v = edge.first;
                int w = edge.second;
                adj[u + 1].push_back({v + 1, w});
                E++;
            }
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
    vector<vector<int>> floyd()
    {
        vector<vector<int>> dist(V+1,vector<int>(V+1, INT_MAX));
        for (int i=1;i<=V;i++)
        {
            dist[i][i]=0;
            for (auto edge:adj[i])
            {
                int v=edge.first;
                int w=edge.second;
                dist[i][v]=min(dist[i][v],w);
            }
        }
        for (int k=1;k<=V;k++)
            for (int i=1;i<=V;i++)
                if (dist[i][k]!=INT_MAX)
                    for (int j=1;j<=V;j++)
                        if (dist[k][j]!=INT_MAX)
                            dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j]);
        return dist;
    }
};
int main()
{
    int v,e,q;
    cin>>v>>e;
    vector<vector<pair<int,int>>> list(v);
    vector<vector<pair<int,int>>> list2(v);

    for (int i = 0; i < e; i++)
    {
        int a, b, w;
        cin >> a >> b >> w;
        list[a].push_back({b, w});
        list2[a].push_back({b, w-1});
        // list[b].push_back({a, w}); // if undirected
    }
    Graph g(list);
    Graph g2(list2);
    // Graph g(v,e);
    //g.printGraph();
    vector<vector<int>> answer=g.floyd();
    vector<vector<int>> answer2=g2.floyd();
    int Y;
    cin>>Y;
    Y++;
    cin>>q;
    for (int i = 0; i < q; i++)
    {
        int u, v;
        cin>>u>>v;
        u++;
        v++;
        // if (answer[u][v]==INT_MAX)
        //     cout<<-1<<endl;
        // else
        //     cout<<answer[u][v]<<endl;
        long long INF = 1e18;
        long long d1 = INF, d2 = INF;

        if (answer2[u][Y] != INT_MAX && answer2[Y][v] != INT_MAX)
            d1 = (long long)answer2[u][Y] + answer2[Y][v];
        d2=answer[u][v];
        long long dist = min(d1, d2);

        if (dist == INF) cout << -1 << endl;
        else cout << dist << endl;
    }
}
