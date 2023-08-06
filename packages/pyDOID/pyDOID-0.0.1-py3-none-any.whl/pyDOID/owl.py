"""RDF/OWL file utilities."""

from rdflib import Graph
from os.path import exists
import pandas as pd
import re


class functional:
    """OWL functional format class"""
    def __init__(self, path):
        self._path = path

    def extract_class_axioms(self):
        axiom = []
        id_label = {}
        with open(self._path, "r") as file:
            for line in file:
                eq = re.search("EquivalentClasses\(([^ ]+) (.+)", line)
                if eq:
                    axiom.append({
                        "id": eq.group(1),
                        "type": "equivalentClass",
                        "axiom": eq.group(2)
                    })

                sc = re.search("SubClassOf\(([^ ]+) (Object.+)", line)
                if sc:
                    axiom.append({
                        "id": sc.group(1),
                        "type": "subClassOf",
                        "axiom": sc.group(2)
                    })

                il = re.search(
                    'AnnotationAssertion\(rdfs:label ([^ ]+) [\'"]([^\'"]+)',
                    line
                )
                if il: id_label[il.group(1)] = il.group(2)

        for a in axiom:
            if a["id"] in id_label.keys(): a["label"] = id_label[a["id"]]

        col_order = [ "id", "label", "type", "axiom" ]
        df = pd.DataFrame.from_dict(axiom).reindex(columns = col_order)

        return df


class xml(Graph):
    """OWL XML format class"""

    def load(self, path, **kwargs):
        """
        Read RDF/OWL files into Python for querying/manipulation.

        Keyword arguments:
        path -- the path to the RDF/OWL file
        """
        self.path = path
        return self.parse(source = path, format="application/rdf+xml", **kwargs)

    def query(self, query):
        """
        Query a loaded RDF graph with SPARQL.

        Keyword arguments:
        query -- the SPARQL query, as a string or the path to a sparql file
        """
        if not isinstance(query, str):
            raise TypeError('query must be a string/path.')

        if exists(query):
            with open(query) as f:
                q = f.read()
        else:
            q = query

        res = Graph.query(self, query_object = q)

        # SPARQLResult to DataFrame solution from Daniel Himmelstein:
        #   https://github.com/RDFLib/sparqlwrapper/issues/125#issuecomment-704291308
        # see also https://github.com/RDFLib/rdflib/issues/1179
        df = pd.DataFrame(
            data=([None if x is None else x.toPython() for x in row] for row in res),
            columns=[str(x) for x in res.vars],
        )

        return df
