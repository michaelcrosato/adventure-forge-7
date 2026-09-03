from adventure_forge.verification.crawler import crawl_world_graph


def test_graph_reachability_and_solvability():
    passed, msg, stats = crawl_world_graph()
    assert passed, f"{msg}: {stats}"
    assert stats["visited_scenes"] >= 14
    assert len(stats["unvisited_scenes"]) == 0
