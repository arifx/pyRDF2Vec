from rdf2vec.walkers import Walker
import numpy as np
from hashlib import md5


class RandomWalker(Walker):
    def __init__(self, depth, walks_per_graph):
        super(RandomWalker, self).__init__(depth, walks_per_graph)

    def extract_random_walks(self, graph, root):
        """Extract random walks of depth - 1 hops rooted in root."""
        # Initialize one walk of length 1 (the root)
        walks = {(root,)}

        for i in range(self.depth):
            # In each iteration, iterate over the walks, grab the 
            # last hop, get all its neighbors and extend the walks
            walks_copy = walks.copy()
            for walk in walks_copy:
                node = walk[-1]
                hops = graph.get_hops(node)

                if len(hops) > 0:
                    walks.remove(walk)

                for (pred, obj) in hops:
                    walks.add(walk + (pred, obj))

            # TODO: Should we prune in every iteration?
            if self.walks_per_graph is not None:
                n_walks = min(len(walks),  self.walks_per_graph)
                walks_ix = np.random.choice(range(len(walks)), replace=False, 
                                            size=n_walks)
                if len(walks_ix) > 0:
                    walks_list = list(walks)
                    walks = {walks_list[ix] for ix in walks_ix}

        # Return a numpy array of these walks
        return list(walks)

    def extract(self, graph, instances):
        canonical_walks = set()
        for instance in instances:
            walks = self.extract_random_walks(graph, str(instance))
            for walk in walks:
                canonical_walk = []
                for i, hop in enumerate(walk):
                    if i == 0 or i % 2 == 1:
                        canonical_walk.append(str(hop))
                    else:
                        digest = md5(str(hop).encode()).digest()[:8]
                        canonical_walk.append(str(digest))

                canonical_walks.add(tuple(canonical_walk))

        return canonical_walks
