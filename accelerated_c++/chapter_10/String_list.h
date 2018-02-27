class String_list {
public:
    String_list(size_t sz): N(sz) {}
    size_t size() { return N; }
private:
    size_t N;
    string[N] strings;
}
