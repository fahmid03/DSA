#include<iostream>
#include <vector>
#include<queue>
#include<climits>

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
        adj.resize(V+1);
        for (int i=0;i<E;i++)
        {
            int first,second,weight;
            cin>>first>>second>>weight;
            adj[first].push_back({second,weight});
        }
    }
    
    void printGraph()
    {
        for (int i=1;i<V+1;i++)
        {
            cout<<i<<"->";
            for (auto j:adj[i])
            {
                cout<<j.first<<" "<<j.second<<" ";
            }
            cout<<endl;
        }
    }

    int djikstra(int src)
    {
        vector<int> dist(V+1, INT_MAX);
        dist[src]=0;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
        pq.push({0, src});
        
        while (!pq.empty())
        {
            auto [d, u] = pq.top();
            pq.pop();
            
            if (d != dist[u]) continue;
            
            for (auto &edge : adj[u])
            {
                int v = edge.first;
                int w = edge.second;

                if (dist[u] + w < dist[v])
                {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }
        return dist[V];
    }
    
    int halfEdgeDjikstra(int src)
    {
        int minCost = djikstra(src); // Try without halving any edge first

        // Try halving each edge in the graph
        for (int u = 1; u <= V; u++)
        {
            for (int j = 0; j < adj[u].size(); j++)
            {
                int puran = adj[u][j].second;
                adj[u][j].second = puran / 2;

                int notun = djikstra(src);
                minCost = min(minCost, notun);

                adj[u][j].second = puran; // Restore original weight
            }
        }

        return minCost;
    }
};

