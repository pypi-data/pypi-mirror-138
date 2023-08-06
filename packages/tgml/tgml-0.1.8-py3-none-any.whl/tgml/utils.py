from .data import TigerGraph

__all__ = ["split_vertices"]


def split_vertices(graph: TigerGraph, timeout: int = 16000, **split_ratios) -> None:
    """Split vertices into a training, a validation, and a test set. 

    Particularly, it creates 3 boolean attributes with each attribute indicating whether 
    the vertex is in the corresponding set. For example, if you want to split the vertices 
    into 80% train, 10% validation and 10% test, you can provide as arguments to the function 
    train_mask=0.8, val_mask=0.1, test_mask=0.1. This will create 3 attributes train_mask, 
    val_mask, test_mask in the graph, if they don't already exist. 80% of vertices will be set 
    to train_mask=1, 10% to val_mask=1, and 10% to test_mask=1 at random. There will be no overlap 
    between the partitions. You can name the attributes however you like as long as you follow the 
    format, such as yesterday=0.8, today=0.1, tomorrow=0.1, but we recommend something meaningful.

    Args:
        graph (TigerGraph): Connection to the TigerGraph database.
        timeout (int, optional): Timeout for the request. Defaults to 16000.
        split_ratios: Three key-values pairs for parition names and ratios, such as train_mask=0.8, 
            val_mask=0.1, test_mask=0.1. The keys can be any strings satisfying python variable name 
            requirements. The values must sum up to 1.
    """
    assert len(split_ratios) == 3, "Need all train, validation and test ratios"
    assert sum(
        split_ratios.values()) == 1, "Train, validation and test ratios have to sum up to 1"
    endpoint = "{}:8000/split/vertices".format(graph.host)
    _payload = {"graph": graph.graph_name, "timeout": timeout}
    for key, attr, ratio in zip(split_ratios,
                                ("train_mask", "val_mask", "test_mask"),
                                ("train_ratio", "val_ratio", "test_ratio")):
        _payload[attr] = key
        _payload[ratio] = split_ratios[key]
    print("Installing and optimizing queries. It might take a minute if this is the first time you run it.")
    resp = graph._mixed_session.get(
        endpoint+"/init", params=_payload)
    resp.raise_for_status()
    resp = graph._rest_session.get(
        endpoint+"/run", params=_payload)
    resp.raise_for_status()
