import rdflib
from rdflib.namespace import XSD
from vaip.utilities.rdf_helper import is_valid_uri
from uuid import uuid4


class Oaisrm:
    """
    Class use to build knowgledge graph using OAIS Reference Model an VAIP ontology.
    """
    def __init__(self):
        """
        Initialize class by constructing a base knowledge graph.
        """
        self.namespaces = {
            "rdf": rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
            "rdfs": rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
            "vaip": rdflib.Namespace("https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#"),
            "entity": rdflib.Namespace("https://ncei.noaa.gov/ontologies/vaip/core/0.3.1/entities/")
        }
        self.kg = self.build_vaip_knowledge_graph()
        self.base_uri = "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#"

        # Member attributes used in build_granule
        self.label = None
        self.content = None
        self.fixity = None
        self.pkg = None

    def build_vaip_knowledge_graph(self):
        kg = rdflib.Graph()
        for prefix, ns in self.namespaces.items():
            kg.namespace_manager.bind(prefix, ns)

        return kg

    def save_rdf(self, path, format="application/rdf+xml"):
        self.kg.serialize(destination=path, format=format, base=self.base_uri, encoding="utf-8")

    def save_rdf_text(self, format="application/rdf+xml"):
        return self.kg.serialize(destination=None, format=format, base=self.base_uri, encoding="utf-8").decode("utf-8")

    def load_rdf(self, path, format="application/rdf+xml"):
        self.kg.parse(path, format=format, publicID=self.base_uri)
        return self.kg

    def load_rdf_text(self, data, format="application/rdf+xml"):
        self.kg.parse(data=data, format=format, publicID=self.base_uri)
        return self.kg

    def add(self, s, p, o):
        obj = None
        if not is_valid_uri(o):
            obj = rdflib.Literal(o)
        else:
            obj = rdflib.URIRef(o)
        self.kg.add((rdflib.URIRef(s), rdflib.URIRef(p), obj))
        return self

    def get_sub_graph_sparql(self, iri):
        print("\n============================== Get SubGraph Graph ==============================")
        sparql_prefix = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX core: <https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#>
            """
        sparql_construct = "SELECT ?s ?p ?o \n"
        constraint = "WHERE { ?s ?p ?o .\n"
        constraint = constraint + "FILTER(?s = " + f"<{iri}>) " + "}"
        sparql = sparql_prefix + sparql_construct + constraint

        return sparql

    def build_packaging_bucket(self, template_graph, bucket):
        # DigitalObject - FileLink
        lbl = "Packaging Bucket"
        vaip_ns = self.namespaces["vaip"]
        entity_ns = self.namespaces["entity"]
        rdf_ns = self.namespaces["rdf"]
        rdfs_ns = self.namespaces["rdfs"]
        bucket_node = rdflib.URIRef(entity_ns + str(uuid4()))

        template_graph.add((bucket_node, rdf_ns.type, vaip_ns.DigitalObject))
        template_graph.add((bucket_node, rdfs_ns.label, rdflib.Literal(lbl, datatype=XSD.string)))
        template_graph.add((bucket_node, vaip_ns.hasBits, rdflib.Literal(bucket, datatype=XSD.string)))

        return bucket_node

    def build_packaging_prefix(self, template_graph, prefix):
        # DigitalObject - FileLink
        lbl = "Packaging Prefix"
        vaip_ns = self.namespaces["vaip"]
        entity_ns = self.namespaces["entity"]
        rdf_ns = self.namespaces["rdf"]
        rdfs_ns = self.namespaces["rdfs"]
        prefix_node = rdflib.URIRef(entity_ns + str(uuid4()))

        template_graph.add((prefix_node, rdf_ns.type, vaip_ns.DigitalObject))
        template_graph.add((prefix_node, rdfs_ns.label, rdflib.Literal(lbl, datatype=XSD.string)))
        template_graph.add((prefix_node, vaip_ns.hasBits, rdflib.Literal(prefix, datatype=XSD.string)))

        return prefix_node

    def build_file_link(self, template_graph, s3_uri):
        # DigitalObject - FileLink
        lbl = "File Link"
        vaip_ns = self.namespaces["vaip"]
        entity_ns = self.namespaces["entity"]
        rdf_ns = self.namespaces["rdf"]
        rdfs_ns = self.namespaces["rdfs"]
        file_lnk_node = rdflib.URIRef(entity_ns + str(uuid4()))

        template_graph.add((file_lnk_node, rdf_ns.type, vaip_ns.DigitalObject))
        template_graph.add((file_lnk_node, rdfs_ns.label, rdflib.Literal(lbl, datatype=XSD.string)))
        template_graph.add((file_lnk_node, vaip_ns.hasBits, rdflib.URIRef(s3_uri)))

        return file_lnk_node

    def build_checksum_value(self, template_graph, checksum):
        # DigitalObject - Checksum Value
        lbl = "Checksum Value"
        vaip_ns = self.namespaces["vaip"]
        entity_ns = self.namespaces["entity"]
        rdf_ns = self.namespaces["rdf"]
        rdfs_ns = self.namespaces["rdfs"]
        checksum_value_node = rdflib.URIRef(entity_ns + str(uuid4()))

        template_graph.add((checksum_value_node, rdf_ns.type, vaip_ns.DigitalObject))
        template_graph.add((checksum_value_node, rdfs_ns.label, rdflib.Literal(lbl, datatype=XSD.string)))
        template_graph.add((checksum_value_node, vaip_ns.hasBits, rdflib.Literal(checksum, datatype=XSD.string)))

        return checksum_value_node

    def build_lbl(self):
        self.label = rdflib.Literal("Granule Entity")

    def build_ci(self, sparql_client, content_iri):

        sparql = self.get_sub_graph_sparql(content_iri)
        content_rows = sparql_client.query(sparql)['content']
        self.content = rdflib.URIRef(self.namespaces["entity"] + str(uuid4()))
        return content_rows

    def build_fixity(self, sparql_client, fixity_iri):

        sparql = self.get_sub_graph_sparql(fixity_iri)
        fixity_rows = sparql_client.query(sparql)['content']
        self.fixity = rdflib.URIRef(self.namespaces["entity"] + str(uuid4()))
        return fixity_rows


    def build_pkg(self, sparql_client, pkg_iri):
        sparql = self.get_sub_graph_sparql(pkg_iri)
        pkg_rows = sparql_client.query(sparql)['content']
        self.pkg = rdflib.URIRef(self.namespaces["entity"] + str(uuid4()))
        return pkg_rows

    def default(self):
        return None

    def switch(self, predicate, default):
        switcher = {
            'http://www.w3.org/2000/01/rdf-schema#label': self.label,
            'https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasContentInformation': self.content,
            'https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasFixity': self.fixity,
            'https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#packagedBy': self.pkg
        }

        obj = switcher.get(predicate)
        if obj is None:
            obj = default
        return obj

    def build_granule(self, sparql_client, storage_template_iri, uuid, bucket, key, s3_uri, checksum):
        sparql = self.get_sub_graph_sparql(storage_template_iri)
        response = sparql_client.query(sparql)
        template_rows = response['content']

        # Clone it
        vaip_ns = self.namespaces["vaip"]
        entity_ns = self.namespaces["entity"]
        self.kg = self.build_vaip_knowledge_graph()
        granule = rdflib.URIRef(entity_ns + uuid)
        file_link_node = self.build_file_link(self.kg, s3_uri)
        checksum_value_node = self.build_checksum_value(self.kg, checksum)
        bucket_node = self.build_packaging_bucket(self.kg, bucket)
        prefix_node = self.build_packaging_prefix(self.kg, key)

        for g_row in template_rows:
            if f"{g_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasContentInformation":
                content_iri = f"{g_row.o}"
                content_rows = self.build_ci(sparql_client, content_iri)

                for c_row in content_rows:
                    if f"{c_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasDataObject":
                        self.kg.set((self.content, c_row.p, file_link_node))
                    else:
                        self.kg.add((self.content, c_row.p, c_row.o))

            if f"{g_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasFixity":
                fixity_iri = f"{g_row.o}"
                fixity_rows = self.build_fixity(sparql_client, fixity_iri)

                for f_row in fixity_rows:
                    if f"{f_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasDataObject":
                        self.kg.set((self.fixity, f_row.p, checksum_value_node))
                    else:
                        self.kg.add((self.fixity, f_row.p, f_row.o))

            if f"{g_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#packagedBy":
                pkg_iri = f"{g_row.o}"
                pkg_rows = self.build_pkg(sparql_client, pkg_iri)

                pkg_list = [bucket_node, prefix_node]
                pkg_data_index = 0
                for p_row in pkg_rows:
                    if f"{p_row.p}" == "https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#hasDataObject":
                        self.kg.add((self.pkg, p_row.p, pkg_list[pkg_data_index]))
                        pkg_data_index = pkg_data_index + 1
                    else:
                        self.kg.add((self.pkg, p_row.p, p_row.o))

        self.build_lbl()
        for row in template_rows:
            predicate = str(row.p)
            default = row.o
            obj = self.switch(predicate, default)
            self.kg.set((granule, row.p, obj))

        return granule.toPython() # This just converts the URIRef object to a string

    # Todo - refactor to take static values from retrieve template after sparql query
    def retrieve_template(self, incoming_iri, owl_iri):
        rdf_ns = self.namespaces["rdf"]
        rdfs_ns = self.namespaces["rdfs"]
        vaip_ns = self.namespaces["vaip"]

        # Load vaip owl from endpoint
        self.load_rdf(owl_iri)

        # Retrieve process_template_node
        # constraint = f"<{policy_uri}> ?p ?o . "
        # constraint = constraint + "?o rdfs:label ?label ."
        # filter = "FILTER (?label = \"Storage Template OISST\")"
        constraint = f"<{incoming_iri}> vaip:hasDataObject ?o . "
        filter = ""
        sparql = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vaip: <https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#>
            SELECT ?s ?p ?o ?data ?bits ?label
            WHERE { """
        sparql = sparql + constraint + filter + " }"

        print("\n============================== Retrieve Template Results ==============================")

        row_cnt = 0
        template_iri = None
        for row in self.kg.query(sparql):
            row_cnt = row_cnt + 1
            template_iri = row["o"]

        return template_iri


