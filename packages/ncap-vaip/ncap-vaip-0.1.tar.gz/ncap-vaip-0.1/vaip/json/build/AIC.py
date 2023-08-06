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
#     result = aic_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class DataObject:
    type: Optional[str] = None
    arn: Optional[str] = None
    iri: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DataObject':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        arn = from_union([from_str, from_none], obj.get("arn"))
        iri = from_union([from_str, from_none], obj.get("IRI"))
        return DataObject(type, arn, iri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["arn"] = from_union([from_str, from_none], self.arn)
        result["IRI"] = from_union([from_str, from_none], self.iri)
        return result


@dataclass
class ContentDataObject:
    data_object: Optional[DataObject] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ContentDataObject':
        assert isinstance(obj, dict)
        data_object = from_union([DataObject.from_dict, from_none], obj.get("data_object"))
        return ContentDataObject(data_object)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data_object"] = from_union([lambda x: to_class(DataObject, x), from_none], self.data_object)
        return result


@dataclass
class ContentInformation:
    content_data_object: Optional[ContentDataObject] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ContentInformation':
        assert isinstance(obj, dict)
        content_data_object = from_union([ContentDataObject.from_dict, from_none], obj.get("content_data_object"))
        return ContentInformation(content_data_object)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content_data_object"] = from_union([lambda x: to_class(ContentDataObject, x), from_none], self.content_data_object)
        return result


@dataclass
class Granule:
    uuid: Optional[UUID] = None
    uri: Optional[str] = None
    vaip_uri: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Granule':
        assert isinstance(obj, dict)
        uuid = from_union([lambda x: UUID(x), from_none], obj.get("uuid"))
        uri = from_union([from_str, from_none], obj.get("uri"))
        vaip_uri = from_union([from_str, from_none], obj.get("vaip_uri"))
        return Granule(uuid, uri, vaip_uri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = from_union([lambda x: str(x), from_none], self.uuid)
        result["uri"] = from_union([from_str, from_none], self.uri)
        result["vaip_uri"] = from_union([from_str, from_none], self.vaip_uri)
        return result


@dataclass
class Provenance:
    granules: Optional[List[Granule]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Provenance':
        assert isinstance(obj, dict)
        granules = from_union([lambda x: from_list(Granule.from_dict, x), from_none], obj.get("granules"))
        return Provenance(granules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["granules"] = from_union([lambda x: from_list(lambda x: to_class(Granule, x), x), from_none], self.granules)
        return result


@dataclass
class ReferenceInformation:
    shortname: Optional[str] = None
    version: Optional[str] = None
    updated: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ReferenceInformation':
        assert isinstance(obj, dict)
        shortname = from_union([from_str, from_none], obj.get("shortname"))
        version = from_union([from_str, from_none], obj.get("version"))
        updated = from_union([from_datetime, from_none], obj.get("updated"))
        return ReferenceInformation(shortname, version, updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["shortname"] = from_union([from_str, from_none], self.shortname)
        result["version"] = from_union([from_str, from_none], self.version)
        result["updated"] = from_union([lambda x: x.isoformat(), from_none], self.updated)
        return result


@dataclass
class PreservationDescriptionInformation:
    reference_information: Optional[ReferenceInformation] = None
    provenance: Optional[Provenance] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PreservationDescriptionInformation':
        assert isinstance(obj, dict)
        reference_information = from_union([ReferenceInformation.from_dict, from_none], obj.get("reference_information"))
        provenance = from_union([Provenance.from_dict, from_none], obj.get("provenance"))
        return PreservationDescriptionInformation(reference_information, provenance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference_information"] = from_union([lambda x: to_class(ReferenceInformation, x), from_none], self.reference_information)
        result["provenance"] = from_union([lambda x: to_class(Provenance, x), from_none], self.provenance)
        return result


@dataclass
class Aic:
    poc: Optional[str] = None
    aic_class: Optional[str] = None
    type: Optional[str] = None
    preservation_description_information: Optional[PreservationDescriptionInformation] = None
    content_information: Optional[ContentInformation] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Aic':
        assert isinstance(obj, dict)
        aic_class = from_union([from_str, from_none], obj.get("class"))
        type = from_union([from_str, from_none], obj.get("type"))
        preservation_description_information = from_union([PreservationDescriptionInformation.from_dict, from_none], obj.get("preservation_description_information"))
        content_information = from_union([ContentInformation.from_dict, from_none], obj.get("content_information"))
        poc = from_union([from_str, from_none], obj.get("poc"))
        return Aic(poc, aic_class, type, preservation_description_information, content_information,poc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["class"] = from_union([from_str, from_none], self.aic_class)
        result["type"] = from_union([from_str, from_none], self.type)
        result["preservation_description_information"] = from_union([lambda x: to_class(PreservationDescriptionInformation, x), from_none], self.preservation_description_information)
        result["content_information"] = from_union([lambda x: to_class(ContentInformation, x), from_none], self.content_information)
        result["poc"] = from_union([from_str, from_none], self.poc)
        return result


def aic_from_dict(s: Any) -> Aic:
    return Aic.from_dict(s)


def aic_to_dict(x: Aic) -> Any:
    return to_class(Aic, x)
