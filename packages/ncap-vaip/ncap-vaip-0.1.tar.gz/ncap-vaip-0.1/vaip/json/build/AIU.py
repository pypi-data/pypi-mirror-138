# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = aiu_from_dict(json.loads(json_string))

from dataclasses import dataclass
from uuid import UUID
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class DataObject:
    uri: str
    uuid: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'DataObject':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("URI"))
        uuid = UUID(obj.get("UUID"))
        return DataObject(uri, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["URI"] = from_str(self.uri)
        result["UUID"] = str(self.uuid)
        return result


@dataclass
class ContentDataObject:
    data_object: List[DataObject]

    @staticmethod
    def from_dict(obj: Any) -> 'ContentDataObject':
        assert isinstance(obj, dict)
        data_object = from_list(DataObject.from_dict, obj.get("data_object"))
        return ContentDataObject(data_object)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data_object"] = from_list(lambda x: to_class(DataObject, x), self.data_object)
        return result


@dataclass
class Information:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'Information':
        assert isinstance(obj, dict)
        return Information()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class RepresentationInformation:
    structure_information: Information
    semantic_information: Information
    other_information: Information

    @staticmethod
    def from_dict(obj: Any) -> 'RepresentationInformation':
        assert isinstance(obj, dict)
        structure_information = Information.from_dict(obj.get("structure_information"))
        semantic_information = Information.from_dict(obj.get("semantic_information"))
        other_information = Information.from_dict(obj.get("other_information"))
        return RepresentationInformation(structure_information, semantic_information, other_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["structure_information"] = to_class(Information, self.structure_information)
        result["semantic_information"] = to_class(Information, self.semantic_information)
        result["other_information"] = to_class(Information, self.other_information)
        return result


@dataclass
class ContentInformation:
    content_data_object: ContentDataObject
    representation_information: RepresentationInformation

    @staticmethod
    def from_dict(obj: Any) -> 'ContentInformation':
        assert isinstance(obj, dict)
        content_data_object = ContentDataObject.from_dict(obj.get("content_data_object"))
        representation_information = RepresentationInformation.from_dict(obj.get("representation_information"))
        return ContentInformation(content_data_object, representation_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content_data_object"] = to_class(ContentDataObject, self.content_data_object)
        result["representation_information"] = to_class(RepresentationInformation, self.representation_information)
        return result


@dataclass
class AssociatedDescription:
    key: str
    bucket: str
    uri: str
    vaip_uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'AssociatedDescription':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        bucket = from_str(obj.get("bucket"))
        uri = from_str(obj.get("uri"))
        vaip_uri = from_str(obj.get("vaip_uri"))
        return AssociatedDescription(key, bucket, uri, vaip_uri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["bucket"] = from_str(self.bucket)
        result["uri"] = from_str(self.uri)
        result["vaip_uri"] = from_str(self.vaip_uri)
        return result


@dataclass
class PackageDescription:
    type: str
    associated_description: AssociatedDescription

    @staticmethod
    def from_dict(obj: Any) -> 'PackageDescription':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        associated_description = AssociatedDescription.from_dict(obj.get("associated_description"))
        return PackageDescription(type, associated_description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["associated_description"] = to_class(AssociatedDescription, self.associated_description)
        return result


@dataclass
class Object:
    uuid: UUID
    checksum: str
    algorithm: str
    size: int
    date: datetime

    @staticmethod
    def from_dict(obj: Any) -> 'Object':
        assert isinstance(obj, dict)
        uuid = UUID(obj.get("UUID"))
        checksum = from_str(obj.get("checksum"))
        algorithm = from_str(obj.get("algorithm"))
        size = from_int(obj.get("size"))
        date = from_datetime(obj.get("date"))
        return Object(uuid, checksum, algorithm, size, date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["UUID"] = str(self.uuid)
        result["checksum"] = from_str(self.checksum)
        result["algorithm"] = from_str(self.algorithm)
        result["size"] = from_int(self.size)
        result["date"] = self.date.isoformat()
        return result


@dataclass
class DataObjects:
    object: Object

    @staticmethod
    def from_dict(obj: Any) -> 'DataObjects':
        assert isinstance(obj, dict)
        object = Object.from_dict(obj.get("object"))
        return DataObjects(object)

    def to_dict(self) -> dict:
        result: dict = {}
        result["object"] = to_class(Object, self.object)
        return result


@dataclass
class Fixity:
    data_objects: DataObjects

    @staticmethod
    def from_dict(obj: Any) -> 'Fixity':
        assert isinstance(obj, dict)
        data_objects = DataObjects.from_dict(obj.get("data_objects"))
        return Fixity(data_objects)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data_objects"] = to_class(DataObjects, self.data_objects)
        return result


@dataclass
class Version:
    id: str
    folder: str
    checksum: str
    algorithm: str
    size: int
    date: datetime
    retention: int
    version: int

    @staticmethod
    def from_dict(obj: Any) -> 'Version':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        folder = from_str(obj.get("folder"))
        checksum = from_str(obj.get("checksum"))
        algorithm = from_str(obj.get("algorithm"))
        size = from_int(obj.get("size"))
        date = from_datetime(obj.get("date"))
        retention = from_int(obj.get("retention"))
        version = from_int(obj.get("version"))
        return Version(id, folder, checksum, algorithm, size, date, retention, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["folder"] = from_str(self.folder)
        result["checksum"] = from_str(self.checksum)
        result["algorithm"] = from_str(self.algorithm)
        result["size"] = from_int(self.size)
        result["date"] = self.date.isoformat()
        result["retention"] = from_int(self.retention)
        result["version"] = from_int(self.version)
        return result


@dataclass
class Provenance:
    versions: List[Version]

    @staticmethod
    def from_dict(obj: Any) -> 'Provenance':
        assert isinstance(obj, dict)
        versions = from_list(Version.from_dict, obj.get("versions"))
        return Provenance(versions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["versions"] = from_list(lambda x: to_class(Version, x), self.versions)
        return result


@dataclass
class PreservationDescriptionInformation:
    reference_information: Information
    provenance: Provenance
    context_information: Information
    fixity: Fixity
    access_rights_information: Information

    @staticmethod
    def from_dict(obj: Any) -> 'PreservationDescriptionInformation':
        assert isinstance(obj, dict)
        reference_information = Information.from_dict(obj.get("reference_information"))
        provenance = Provenance.from_dict(obj.get("provenance"))
        context_information = Information.from_dict(obj.get("context_information"))
        fixity = Fixity.from_dict(obj.get("fixity"))
        access_rights_information = Information.from_dict(obj.get("access_rights_information"))
        return PreservationDescriptionInformation(reference_information, provenance, context_information, fixity, access_rights_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference_information"] = to_class(Information, self.reference_information)
        result["provenance"] = to_class(Provenance, self.provenance)
        result["context_information"] = to_class(Information, self.context_information)
        result["fixity"] = to_class(Fixity, self.fixity)
        result["access_rights_information"] = to_class(Information, self.access_rights_information)
        return result


@dataclass
class Aiu:
    aiu_class: str
    type: str
    package_description: PackageDescription
    packaging_information: Information
    content_information: ContentInformation
    preservation_description_information: PreservationDescriptionInformation

    @staticmethod
    def from_dict(obj: Any) -> 'Aiu':
        assert isinstance(obj, dict)
        aiu_class = from_str(obj.get("class"))
        type = from_str(obj.get("type"))
        package_description = PackageDescription.from_dict(obj.get("package_description"))
        packaging_information = Information.from_dict(obj.get("packaging_information"))
        content_information = ContentInformation.from_dict(obj.get("content_information"))
        preservation_description_information = PreservationDescriptionInformation.from_dict(obj.get("preservation_description_information"))
        return Aiu(aiu_class, type, package_description, packaging_information, content_information, preservation_description_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["class"] = from_str(self.aiu_class)
        result["type"] = from_str(self.type)
        result["package_description"] = to_class(PackageDescription, self.package_description)
        result["packaging_information"] = to_class(Information, self.packaging_information)
        result["content_information"] = to_class(ContentInformation, self.content_information)
        result["preservation_description_information"] = to_class(PreservationDescriptionInformation, self.preservation_description_information)
        return result


def aiu_from_dict(s: Any) -> Aiu:
    return Aiu.from_dict(s)
