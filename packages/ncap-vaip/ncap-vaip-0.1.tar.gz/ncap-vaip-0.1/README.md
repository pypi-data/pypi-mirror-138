# VAIP (Virtual Archive Information Package) Models Overview
This is a central repository for VAIP CRUD (create, read, update, and delete) operations for the various types of AIPs
we manage. This includes AIUs (Archival Information Units), which are generally associated with granules, and 
AICs (Archival Information Collections), which are generally associated with collections and higher level groupings. 
We can use AICs to represent collections of collections or subsets thereof. This is a many-to-many 
system of relationships. 

## Package Description
The package entails general metadata parsing for building VAIPs as well as VAIP generation located in the 
build_vaip and buld_kgvaip directory. 

### build_vaip
build_vaip is a JSON schema based implementation which leverages Quicktype to build a strongly-typed, object-oriented 
representation of the JSON schema we use to define AIPs.

### build_kgvaip
build_kgvaip is a rdflib based implementation which connects to a AWS Neptune knowledge graph store to run SPARQL queries in order to perform CRUD operations on the vAIP.

## Installation
While under the `vaip-models` directory,

* `python setup.py install` or `pip install .\vaip-models\`
* `pip install -r requirements.txt`

##### Local s3 Testing
* `export AWS_TEST_LOCAL="true"` # sets url for local vs VPC
* `export AWS_TEST_PROFILE="your-aws-profile"` # only if not running in VPC (locally)

## Important 
Modifications to vaip-models can be published to the lambda layer

* `python updatelayer.py updatelib`

Updates to vaip are handled by sam deploy of the system.

## Documentation to update ontology .owl file 
The ontology is located in the data subfolder.

- Download the latest ontology file from webprotege (RDF/XML)
- Make a copy with a new version increasing bugfix, minor, and then major version number-
- Upload the file into webprotege 
- Upload .owl file to Amazon S3 **"ncap-archive-dev-pub/vaip"**
	 - **S3 url https://s3.console.aws.amazon.com/s3/buckets/ncap-archive-dev-pub?region=us-east-1&prefix=vaip/&showversions=false**








last updated 01-18-2022