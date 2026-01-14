#include<iostream>
#include<vector>
#include<queue>
#include <unordered_map>

using namespace std;

class Graph
{
public:
    int V;
    int E;
    vector<vector<pair<int,double>>> adj;
    Graph(int v,int e)
    {
        V=v;E=e;
        // int first,second,weight;
        adj.resize(V+1);
        // for (int i=0;i<E;i++)
        // {
        //     cin>>first>>second>>weight;
        //     adj[first].push_back({second,weight});
        //     adj[second].push_back({first,weight});
        // }
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
    vector<vector<double>> floyd()
    {
        vector<vector<double>> dist(V+1,vector<double>(V+1,0.0));
        for (int i=1;i<V+1;i++)
        {
            dist[i][i]=1.0;
            for (auto j:adj[i])
            {
                dist[i][j.first]=j.second;
            }
        }
        for (int k=1;k<V+1;k++)
        {
            for (int i=1;i<V+1;i++)
            {
                for (int j=1;j<V+1;j++)
                {
                    if(dist[i][k]!=0.0&&dist[k][j]!=0.0)
                        dist[i][j] = max(dist[i][j],dist[i][k]*dist[k][j]);
                }
            }
        }
        return dist;
    }
};
int main()
{
    int c;
    cin>>c;
    unordered_map<string,int> s;
    for (int i=0;i<c;i++)
    {
        string name;
        cin>>name;
        s[name]=i+1;
    }
    int conv;
    cin>>conv;
    Graph g(c,conv);
    for (int i=0;i<conv;i++)
    {
        double w;
        string u,v;
        cin>>u>>w>>v;
        g.adj[s[u]].push_back({s[v],w});
    }
    vector<vector<double>> dist=g.floyd();
    for (int i=1;i<c+1;i++)
    {
        if (dist[i][i]>1.0)
        {
            cout<<"YES";
            return 0;
        }
    }
    cout<<"NO";
    return 0;
}
