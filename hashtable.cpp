#include <bits/stdc++.h>

using namespace std;

const int INITIAL=13;
const double MAXF=0.5;
const double MINF=0.25;
const int C1=1;
const int C2=3;
const int CHAIN=1;
const int DOUBHASH=2;
const int CUSPROB=3;

int nextprime(int n) {
    for (int i=n+1;;i++) {
        bool isprime=true;
        for (int j=2;j*j<=i;j++)
            if (i%j==0) {
                isprime=false;
                break;
            }
        if (isprime) return i;
    }
}

int prevprime(int n) {
    for (int i=n-1;i>=2;i--) {
        bool isprime=true;
        for (int j=2;j*j<=i;j++)
            if (i%j==0) {
                isprime=false;
                break;
            }
        if (isprime) return i;
    }
    return INITIAL;
}

template <typename K,typename V>
struct Entry {
    K key;
    V value;
};

static int hash1(const string& key) {
    int hash=0;
    int base=47;
    for (char c:key)
        hash=hash*base+(c-'a'+1);
    if(hash < 0) hash=-hash;
    return hash;
}

static int hash2(const string& key) {
    int hash=5381;
    for (char c:key)
        hash=((hash << 5)+hash)+c;
    if (hash<0) hash=-hash;
    return hash;
}

static int sechash(const string& key, int size) {
    int hash=0;
    for (char c:key)
        hash+=c;
    return hash%(size-1)+1;
}

template <typename T>
static int hash1(const T& key) {
    char* chararr=reinterpret_cast<char*>(&key);
    int len=sizeof(T);
    long long hash=0;
    int base=47;
    for (int i=0;i<len;i++)
        hash=hash*base+chararr[i];
    if (hash<0) hash=-hash;
    return hash;
}

template <typename T>
static int hash2(const T& key) {
    char* chararr=reinterpret_cast<char*>(&key);
    int len=sizeof(T);
    long long hash=5381;
    for (int i=0;i<len;i++)
        hash=((hash<<5)+hash)+chararr[i];
    if (hash<0) hash=-hash;
    return hash;
}

template <typename T>
static int sechash(const T& key,int size) {
    char* chararr=reinterpret_cast<char*>(&key);
    int len=sizeof(T);
    int sum=0;
    for (int i=0;i<len;i++)
        sum+=chararr[i];
    return sum%(size-1)+1;
}

template <typename K,typename V>
class HashTable {
private:
    int size;
    int count;
    int hashtype;
    int hash;
    vector<list<Entry<K,V>>> table;
    vector<optional<Entry<K,V>>> opentable;
    long long collisionnum=0;
    long long totalhit=0;
    int inscount=0;
    int delcount=0;

private:
    int primaryhash(const K& key) {
        if (hash==1) return hash1(key);
        return hash2(key);
    }

    int probe(const K& key,int i) {
        int h=primaryhash(key);
        int aux=sechash(key,size);
        if (hashtype==DOUBHASH)
            return (h+i*aux)%size;
        if (hashtype==CUSPROB)
            return (h+C1*i*aux+C2*i*i)%size;
        return h%size;
    }

    void resize(int newsize) {
        vector<Entry<K,V>> rupalibank;
        if (hashtype==CHAIN) {
            for (auto& group:table)
                for (auto& entry:group)
                    rupalibank.push_back(entry);
            table.clear();
        } else {
            for (auto& entry:opentable)
                if (entry.has_value())
                    rupalibank.push_back(entry.value());
            opentable.clear();
        }
        size=newsize;
        count=0;
        inscount=0;
        delcount=0;

        if (hashtype==CHAIN)
            table.resize(size);
        else
            opentable.resize(size);
        for (auto& entry:rupalibank) {
            if (hashtype==CHAIN) {
                int idx=primaryhash(entry.key)%size;
                if (!table[idx].empty())
                    collisionnum++;
                table[idx].push_back({entry.key, entry.value});
                count++;
            }
            else {
                bool inserted=false;
                for (int i=0;i<size;i++) {
                    int idx=probe(entry.key,i);
                    if (!opentable[idx].has_value()) {
                        opentable[idx]=Entry<K,V>{entry.key,entry.value};
                        inserted=true;
                        break;
                    }
                    collisionnum++;
                }
                if (inserted) count++;
            }
        }
    }

    void check() {
        double load=(double)count/size;
        if (load>MAXF&&(inscount>=count/2||count==0)) {
            resize(nextprime(size*2));
        } else if (load<MINF&&size>INITIAL&&(delcount>=count/2||count==0)) {
            resize(prevprime(size/2));
        }
    }

    bool keyexist(const K& key) {
        if (hashtype==CHAIN) {
            int idx=primaryhash(key)%size;
            for (auto& entry:table[idx])
                if (entry.key==key) return true;
        } else {
            for (int i=0;i<size;i++) {
                int idx=probe(key,i);
                if (!opentable[idx].has_value()) break;
                if (opentable[idx]->key==key) return true;
            }
        }
        return false;
    }

public:
    HashTable(int s,int h) {
        size=INITIAL;
        count=0;
        hashtype=s;
        hash=h;
        if (hashtype==CHAIN)
            table.resize(size);
        else
            opentable.resize(size);
    }

    void reset() {
        totalhit = 0;
    }

    bool insert(const K& key,const V& value) {
        if (keyexist(key)) {
            return false;
        }
        if (hashtype==CHAIN) {
            int idx=primaryhash(key)%size;
            for (auto &entry:table[idx])
                if (entry.key==key)
                    return false;
            if (!table[idx].empty())
                collisionnum++;
            table[idx].push_back({key,value});
            count++;
        } else {
            bool inserted=false;
            for (int i=0;i<size;i++) {
                int idx=probe(key,i);
                if (!opentable[idx].has_value()) {
                    opentable[idx]=Entry<K,V>{key,value};
                    inserted=true;
                    count++;
                    break;
                }
                collisionnum++;
            }

            if (!inserted) {
                resize(nextprime(size*2));
                return insert(key,value);
            }
        }
        inscount++;
        check();
        return true;
    }

    bool search(const K& key) {
        int hits=0;
        if (hashtype==CHAIN) {
            int idx=primaryhash(key)%size;
            for (auto& entry:table[idx]) {
                hits++;
                if (entry.key==key) {
                    totalhit+=hits;
                    return true;
                }
            }
        } else {
            for (int i=0;i<size;i++) {
                hits++;
                int idx=probe(key,i);
                if (!opentable[idx].has_value())
                    break;
                if (opentable[idx]->key==key) {
                    totalhit+=hits;
                    return true;
                }
            }
        }
        totalhit+=hits;
        return false;
    }

    bool remove(const K& key) {
        if (!keyexist(key)) return false;
        if (hashtype==CHAIN) {
            int idx=primaryhash(key)%size;
            auto& group=table[idx];
            for (auto it=group.begin();it!=group.end();it++)
            {
                if (it->key==key) {
                    group.erase(it);
                    count--;
                    delcount++;
                    check();
                    return true;
                }
            }
        } else {
            for (int i=0;i<size;i++) {
                int idx=probe(key,i);
                if (!opentable[idx].has_value()) break;
                if (opentable[idx]->key==key) {
                    opentable[idx].reset();
                    count--;
                    delcount++;
                    check();
                    return true;
                }
            }
        }
        return false;
    }

    int getcollisions() {return collisionnum;}
    double getaveragehit(int n) {
        if (n==0) return 0.0;
        return (double)totalhit/n;
    }
};

string generateword(int len) {
    string word;
    for (int i=0;i<len;i++) {
        int r=rand()%26;
        char c='a'+r;
        word+=c;
    }
    return word;
}

int main() {
    srand(time(0));
    int totalwords=10000;
    int searches=1000;
    int length=10;
    vector<string> words;
    unordered_set<string> puranwords;

    while (words.size()<totalwords) {
        string w=generateword(length);
        if (puranwords.insert(w).second)
            words.push_back(w);
    }
    cout<<"\t\thash1\t\t\t\thash2\n";
    cout<<"\t\tcollisions\tavg hits\tcollisions\tavg hits\n";
    int hashsystems[3]={CHAIN,DOUBHASH,CUSPROB};
    char* names[3]={"chaining method","double hashing","custom probing"};
    for (int i=0;i<3;i++) {
        HashTable<string,int> ht1(hashsystems[i],1);
        for (int j=0;j<totalwords;j++)
            ht1.insert(words[j],j+1);
        int collisions1=ht1.getcollisions();
        ht1.reset();
        vector<string> searchwords=words;
        for (int j=0;j<searches;j++)
            ht1.search(searchwords[j]);
        HashTable<string,int> ht2(hashsystems[i],2);
        for (int j=0;j<totalwords;j++)
            ht2.insert(words[j],j+1);
        int collisions2=ht2.getcollisions();
        ht2.reset();
        for (int j=0;j<searches;j++)
            ht2.search(searchwords[j]);
        cout<<names[i];
        cout<<"\t"<<collisions1<<"\t\t"<<ht1.getaveragehit(searches)<<"\t\t"<<collisions2<<"\t\t"<<ht2.getaveragehit(searches)<<"\n";
    }
    return 0;
}
