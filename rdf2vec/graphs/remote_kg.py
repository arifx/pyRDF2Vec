from SPARQLWrapper import SPARQLWrapper, JSON


class RemoteKnowledgeGraph(object):
    def __init__(self, location):
        self.location = location
        self.endpoint = SPARQLWrapper(self.location)

    def get_hops(self, vertex):
        print(vertex)
        if not vertex.startswith('http://'):
            return []

        query = """
            SELECT ?p ?o WHERE {
                <"""+vertex+"""> ?p ?o .
            }
        """
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        hops = []
        for result in results['results']['bindings']:
            hops.append((result['p']['value'], result['o']['value']))
        return hops