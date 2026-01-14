#include <iostream>
#include<vector>
#include<algorithm>
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
            cout<<i<<"->";
            for (auto j:adj[i])
            {
                cout<<j.first<<" "<<j.second<<" ";
            }
            cout<<endl;
        }
    }
    vector<int> bellmanFord()
    {
        //vector<int> dist(V+1,INT_MAX);
        vector<int> dist(V+1,0);
        vector<int> parent(V+1,-1);
        int destiny=-1;
        for (int i=0;i<V-1;i++)
        {
            for (int j=1;j<V+1;j++)
            {
                for (auto edge:adj[j])
                {
                    int u=j;
                    int v=edge.first;
                    int w=edge.second;
                    if (dist[u]+w<dist[v])
                    {
                        dist[v]=dist[u]+w;
                        parent[v]=u;
                    }
                }
            }
        }
        for (int j=1;j<V+1;j++)
        {
            for (auto edge:adj[j])
            {
                int u=j;
                int v=edge.first;
                int w=edge.second;
                if (dist[u]+w<dist[v])
                {
                    destiny=v;
                    parent[v]=u;
                }
            }
        }
        if (destiny==-1) return {-1};
        for (int i=0;i<V;i++)
        {
            destiny=parent[destiny];
        }
        vector<int> answer;
        int present=destiny;
        bool firsttime=true;
        while (present!=destiny||firsttime)
        {
            answer.push_back(present);
            present=parent[present];
            firsttime=false;
        }
        reverse(answer.begin(),answer.end());
        return answer;
    }
};

int main()
{
    int v,e;
    cin>>v>>e;
    Graph g(v,e);
    // g.printGraph();
    vector<int> answer=g.bellmanFord();
    for (int vertex:answer)
    {
        cout<<vertex<<" ";
    }
    cout<<endl;
    return 0;
}