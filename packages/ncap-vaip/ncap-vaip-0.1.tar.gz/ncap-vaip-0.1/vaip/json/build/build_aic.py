import dateutil.parser

# Content Information
from .AIC import DataObject, ContentDataObject, ContentInformation
# Provenance
from .AIC import Granule, Provenance
# Preservation Description Information
from .AIC import PreservationDescriptionInformation, ReferenceInformation
# AIC
from .AIC import Aic


def build_data_object(type, arn, IRI):
    """
    :param type: Type of DataObject. Either 'physical_object' or 'digital_object'
    :param arn: ARN of the collection object in S3
    :param IRI: IRI
    :return: DataObject
    """

    data_obj = DataObject(type, arn , IRI)
    return data_obj


def build_content_data_object(data_obj):
    """
    :param data_object:  DataObject
    :return:  ContentDataObject
    """

    content_data_obj = ContentDataObject(data_obj)
    return content_data_obj


def build_content_information(content_data_obj):
    """
    :param content_data_obj: ContentDataObject
    :return: ContentInformation Object
    """

    content_information_obj = ContentInformation(content_data_obj)
    return content_information_obj


def build_granule(uuid, uri, vaip_uri):
    """
    :param uuid: UUID of the granule in S3
    :param uri: S3 link to granule in ingest bucket
    :param vaip_uri: S3 link to the granule in vaip bucket
    :return: Granule Object
    """

    granule_obj = Granule(uuid, uri, vaip_uri)
    return granule_obj


def build_provenance(granules):
    """
    :param granules: List of Granule Objects
    :return: Provenance Object
    """

    provenance_obj = Provenance(granules)
    return provenance_obj


def build_reference_information(shortname, version, updated):
    """
    :param shortname: Collection Shortname
    :param version: Collection Version
    :param updated: DateTime object
    :return:
    """
    datetime = dateutil.parser.parse(updated)
    reference_information_obj = ReferenceInformation(shortname, version, datetime)
    return reference_information_obj


def build_preservation_description_information(reference_information, provenance):
    """
    :param reference_information: ReferenceInformation Object
    :param provenance: Provenance Object
    :return: PreservationDescriptionInformation Object
    """

    preservation_description_information_obj = \
        PreservationDescriptionInformation(reference_information, provenance)
    return preservation_description_information_obj


def build_aic(aic_class, aic_type, poc, data_obj_type, arn, IRI, uuid, uri, vaip_uri, shortname, version, updated):
    """
    :param aic_class: AIC Class (AIP)
    :param aic_type: Type of AIP (AIC in this case)
    :param poc: Person of Contact
    :param data_object_type: Type of DataObject. Either 'physical_object' or 'digital_object'
    :param arn: ARN of the collection object in S3
    :param IRI: IRI
    :param uuid: UUID of the granule in S3
    :param uri: S3 link to granule in ingest bucket
    :param vaip_uri: S3 link to the granule in vaip bucket
    :param shortname: Collection Shortname
    :param version: Collection Version
    :param updated: DateTime object
    :return:
    """

    data_obj = build_data_object(data_obj_type,arn, IRI)
    content_data_obj = build_content_data_object(data_obj)
    content_information_obj = build_content_information(content_data_obj)

    granule_obj = build_granule(uuid, uri, vaip_uri)
    provenance_obj = build_provenance([granule_obj])

    reference_information_obj = \
        build_reference_information(shortname, version, updated)
    preservation_description_information_obj = \
        build_preservation_description_information(
            reference_information_obj, provenance_obj)

    aic_obj = Aic(
        poc, aic_class, aic_type,
        preservation_description_information_obj,
        content_information_obj
    )

    return aic_obj


def build_aic_empty_granule(aic_class, aic_type, data_obj_type, arn, IRI, shortname, version, updated):
    """
    :param aic_class: AIC Class (AIP)
    :param aic_type: Type of AIP (AIC in this case)
    :param data_obj_type: Type of AIP (AIC in this case)
    :param arn: ARN of the collection object in S3
    :param IRI: IRI
    :param shortname: Collection Shortname
    :param version: Collection Version
    :param updated: DateTime object
    :return:
    """

    data_obj = build_data_object(data_obj_type, arn, IRI)
    content_data_obj = build_content_data_object(data_obj)
    content_information_obj = build_content_information(content_data_obj)

    provenance_obj = build_provenance([])

    reference_information_obj = \
        build_reference_information(shortname, version, updated)
    preservation_description_information_obj = \
        build_preservation_description_information(
            reference_information_obj, provenance_obj)

    aic_obj = Aic(
        poc=None,
        aic_class=aic_class,
        type=aic_type,
        preservation_description_information=preservation_description_information_obj,
        content_information=content_information_obj
    )

    return aic_obj

