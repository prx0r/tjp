from postagi_kernel.methods.convergence import qgram_similarity, soft_dice, temporal_jaccard, topic_graph, graph_summary

def test_similarity_identity():
    assert abs(qgram_similarity("retrieval augmented generation","retrieval augmented generation")-1)<1e-12
    assert abs(soft_dice("large language model","large language model")-1)<1e-8

def test_jaccard():
    assert temporal_jaccard({"a","b"},{"b","c"})==1/3

def test_graph():
    g=topic_graph([{"subject_topic":"a","object_topic":"b"},{"subject_topic":"a","object_topic":"b"}])
    assert g["a"]["b"]["weight"]==2
    assert "eigenvector_centrality" in graph_summary(g)
