import dateutil.parser

#  AIU Package Description
from .AIU import PackageDescription
from .AIU import AssociatedDescription

# Provenance
from .AIU import Version
from .AIU import Provenance

# Preservation Description Information
from .AIU import Object
from .AIU import DataObjects
from .AIU import Fixity
from .AIU import PreservationDescriptionInformation

# Content Information
from .AIU import Information
from .AIU import ContentInformation
from .AIU import RepresentationInformation
from .AIU import ContentDataObject
from .AIU import DataObject

from .AIU import Aiu


def build_associated_description(key, bucket, uri, vaip_uri):
    """

    :param key: Object filename in s3 bucket
    :param bucket: Name of the s3 bucket
    :param uri: s3 link to object in ingest bucket
    :param vaip_uri: s3 link to the object in vaip bucket
    :return: AssocaitedDescription Object
    """
    return AssociatedDescription(key, bucket, uri, vaip_uri)


def build_content_data_object(dataobject):
    """
    :param dataobject: List of DataObject
    :return: ContentDataObject
    """
    return ContentDataObject(dataobject)


def build_content_information(content_data_obj, representation_information):
    """
    :param content_data_obj: List of ContentDataObject Object
    :param representation_information: Representation Object
    :return: Content Information Object
    """
    return ContentInformation(
        content_data_obj, representation_information
    )


def build_data_object(uri, uuid):
    """
    :param uri: s3 link to object in ingest bucket
    :param uuid: UUID of the object in s
    :return: DataObject Object
    """
    return DataObject(uri, uuid)


def build_data_objects(obj):
    """
    :param obj: Type Object
    :return: DataObjects Object
    """
    return DataObjects(obj)


def build_fixity(data_objects):
    """
    :param data_objects: DataObjects Object
    :return: Fixity Object
    """
    return Fixity(data_objects)


def build_object(uuid, checksum, algorithm, size, date):
    """

    :param uuid: UUID of the object in s3
    :param checksum: The checksum
    :param algorithm: Checksum algorithm that was used
    :param size: Size of file
    :param date: datetime str
    :return: Object object
    """
    datetime = dateutil.parser.parse(date)
    return Object(uuid, checksum, algorithm, size, datetime)


def build_package_description(type, associated_description):
    """

    :param associated_description: AssociatedDescription Object
    :param type: Type of package
    :return: PackageDescription Object
    """
    return PackageDescription(type, associated_description)


def build_version(id, checksum, algorithm, size,
                  date, retention, version):
    """

    :param id: ID of the object version in s3
    :param checksum: The checksum
    :param algorithm: Checksum Algorithm that was used
    :param size: Size of file
    :param date: datetime str
    :param retention: Retention period of the obj in s3
    :param version: Version number
    :return: Version Object
    """
    datetime = dateutil.parser.parse(date)
    return Version(id, f"version-{version}", checksum,
                   algorithm, size, datetime, retention, version)


def build_provenance(versions):
    """

    :param versions: List of Version Objects
    :return: Provenance Object
    """
    return Provenance(versions)


def build_preservation_description_information(provenance, fixity):
    """
    :param provenance: Provenance Object
    :param fixity: Fixity Object
    :return: PreservationDescriptionInformation Object
    """
    #TODO Work In Progress Change Later
    # Works under the assumption that ReferenceInformation, ContextInformation, and AccesRightsInformation is Empty
    reference_information_obj = Information()
    access_rights_information_obj = Information()
    context_information_obj =  Information()

    return PreservationDescriptionInformation(
        reference_information_obj, provenance,
        context_information_obj, fixity, access_rights_information_obj
    )


# TODO fix if we add information to this field. Currently will return empty objects as we have defined in the model
def build_representation_information():
    """
    :return: Representation Information Object
    """
    structure_information_obj = Information()
    semantic_information_obj = Information()
    other_information_obj = Information()

    return RepresentationInformation(
        structure_information_obj,
        semantic_information_obj,
        other_information_obj
    )


def build_aiu(aiu_class, aip_type, uuid, package_description_type,
               key, bucket, ingest_uri, vaip_uri, checksum,
               algorithm, size, date, retention, version, versionid):
    """

    :param aiu_class:
    :param aip_type:
    :param uuid: UUID of the object in s3
    :param package_description_type:
    :param key: Object filename in s3 bucket
    :param bucket: Name of ingest bucket
    :param ingest_uri: S3 link to object in ingest bucket
    :param vaip_uri: S3 link to object in vaip bucket
    :param checksum: The checksum
    :param algorithm: Checksum algorithm that was used
    :param size: The size of the file
    :param date: DateTime obj
    :param retention: Retention period of the obj in s3
    :param version: Version number
    :param versionid: Version ID (x-amz-...) from the archive bucket.
    :return:
    """
    associated_description_obj = \
        build_associated_description(key, bucket, ingest_uri, vaip_uri)
    package_description_obj = \
        build_package_description(package_description_type,
                                  associated_description_obj)

    # TODO PackagingInformation Empty
    packaging_information_obj = Information()

    obj = build_object(uuid, checksum, algorithm, size, date)
    data_objects = build_data_objects(obj)
    fixity_obj = build_fixity(data_objects)

    version_obj = build_version(versionid, checksum, algorithm, size,
                                date, retention, version)
    provenance_obj = build_provenance([version_obj])

    preservation_description_information_obj = \
        build_preservation_description_information(provenance_obj, fixity_obj)

    data_obj = build_data_object(ingest_uri, uuid)
    content_data_obj = build_content_data_object([data_obj])
    representation_information_obj = build_representation_information()
    content_information_obj = build_content_information(
        content_data_obj, representation_information_obj
    )
    aiu_obj = Aiu(aiu_class, aip_type, package_description_obj,
                    packaging_information_obj, content_information_obj,
                    preservation_description_information_obj)

    return aiu_obj
