import json
import requests
from io import BytesIO
from rdflib.query import Result


class NeptuneClient:
    def __init__(self, sparql_endpoint="https://ncap-archive-neptune."
                                       "cluster-c4xlxig1zmvp.us-east-1.neptune.amazonaws.com:8182/sparql"):
        self.endpoint = sparql_endpoint

    def bulk_load_neptune(self, obj_url, graph_name):
        headers = {'Content-Type': 'application/json'}
        params = {'update': f'LOAD <{obj_url}> INTO GRAPH <{graph_name}>'}
        r = requests.post(self.endpoint, params=params, headers=headers)
        return {'code': r.status_code, 'content': r.json()}

    def query(self, query):
        r = requests.post(self.endpoint, data={'query': query})
        return {'code': r.status_code, 'content': Result.parse(BytesIO(r.content), format="json")}

    def update(self, statement):
        r = requests.post(self.endpoint, data={'update': statement})
        return {'code': r.status_code, 'content': r.json()}

    def create_graph(self, graph_name):
        update = f'CREATE GRAPH <{graph_name}>'
        return self.update(update)

    def drop_graph(self, graph_name):
        update = f'DROP GRAPH <{graph_name}>'
        return self.update(update)

    def insert_from_oaisrm(self, oaisrm, graph_name):
        nt = oaisrm.save_rdf_text(format="application/n-triples")
        update = f'INSERT DATA {{ GRAPH <{graph_name}> {{ {nt} }} }}'
        return self.update(update)

    def delete_from_oaisrm(self, oaisrm, graph_name):
        nt = oaisrm.save_rdf_text(format="application/n-triples")
        update = f'DELETE DATA {{ GRAPH <{graph_name}> {{ {nt} }} }}'
        return self.update(update)

    def load_into_oaisrm(self, oaisrm, query):
        response = self.query(query)
        results = response['content']
        for result in results:
            oaisrm.add(result[0], result[1], result[2])
        return oaisrm

    def compose_process_template_config_sparql(self, process_template_iri):
        sparql = """
            PREFIX vaip: <https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#>
            SELECT ?config
            FROM <http://ncei.noaa.gov/vaip/0.3.1>
            WHERE {{
                <{iri}> vaip:hasContentInformation ?o .
                ?o vaip:hasDataObject ?config_iri .
                ?config_iri vaip:hasBits ?config
            }}""".format(iri=process_template_iri)

        return sparql

    def retrieve_process_template_config(self, process_template_iri):
        sparql = self.compose_process_template_config_sparql(process_template_iri)

        process_template_config = None
        response = self.query(sparql)
        for rows in response['content']:
            process_template_config = rows[0]
            break

        process_template_config_object = {}
        if (process_template_config):
            # If we store the JSON as a string in the graph, then we can load it as an object and return it
            process_template_config_object = json.loads(process_template_config)

        return process_template_config_object

    def compose_aic_process_templates_sparql(self, aiu_process_template_iri):
        sparql = """
            PREFIX vaip: <https://ncei.noaa.gov/ontologies/vaip/core/0.3.1#>
            SELECT ?ctx
            FROM <http://ncei.noaa.gov/vaip/0.3.1>
            WHERE {{
                <https://ncei.noaa.gov/ontologies/vaip/core/0.3.1/entities/RCnL53mixVunkaLjLmWKYgO> vaip:hasContext ?ctx .
                ?ctx rdfs:label ?label.
                FILTER regex(str(?label), "AIC Membership Granule Process Template*")
            }}
            """.format(iri=aiu_process_template_iri)

        return sparql

    def retrieve_aic_process_templates(self, aiu_process_template_iri):
        sparql = self.compose_aic_process_templates_sparql(aiu_process_template_iri)

        process_templates = []
        response = self.query(sparql)

        for rows in response['content']:
            process_templates.append(rows[0])

        print(process_templates)
        return process_templates
