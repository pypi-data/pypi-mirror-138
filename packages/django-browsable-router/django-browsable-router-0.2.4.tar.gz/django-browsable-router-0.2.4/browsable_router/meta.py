import logging

from django.utils.encoding import force_str
from rest_framework.fields import DictField, Field, SerializerMethodField
from rest_framework.metadata import SimpleMetadata
from rest_framework.request import Request, clone_request
from rest_framework.serializers import (
    HiddenField,
    ListSerializer,
    ManyRelatedField,
    ReadOnlyField,
    RelatedField,
    Serializer,
)

from .typing import DictOrListOfDicts, List, Optional, Set, Type, Union, ViewProtocol


__all__ = ["APIMetadata", "SerializerAsOutputMetadata"]


logger = logging.getLogger(__name__)


class APIMetadata(SimpleMetadata):
    """Metadata class that adds input and output info for
    each of the attached views methods based on
    the serializer for that method.
    """

    recognized_methods: Set[str] = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    skip_fields: Set[Type[Field]] = {ReadOnlyField, HiddenField, SerializerMethodField}
    used_attrs: List[str] = ["label", "help_text", "min_length", "max_length", "min_value", "max_value"]

    @staticmethod
    def get_input_serializer(view: ViewProtocol) -> Serializer:
        return view.get_serializer()

    @staticmethod
    def get_output_serializer(view: ViewProtocol) -> Optional[Serializer]:
        try:
            return view.get_serializer(output=True)
        except TypeError:
            logger.info(
                "To get access to output metadata, define view.get_serializer() so that it takes a "
                "boolean argument 'output', and return an output serializer when output=True."
            )
            return None

    def determine_actions(self, request: Request, view: ViewProtocol):
        """Return information about the fields that are accepted for methods in self.recognized_methods."""
        actions = {}
        for method in self.recognized_methods & set(view.allowed_methods):
            view.request = clone_request(request, method)

            input_serializer = self.get_input_serializer(view)
            output_serializer = self.get_output_serializer(view)

            exceptions = getattr(input_serializer, "error_codes", {})
            if output_serializer is not None:
                exceptions.update(getattr(output_serializer, "error_codes", {}))

            actions[method] = {
                "input": self.get_serializer_info(input_serializer),
                "exceptions": exceptions,
            }
            if output_serializer is not None:
                actions[method]["output"] = self.get_serializer_info(output_serializer)

            view.request = request

        return actions

    def get_serializer_info(self, serializer: Serializer) -> DictOrListOfDicts:
        """Given an instance of a serializer, return a dictionary of metadata about its fields."""
        data_serializer = getattr(serializer, "child", serializer)

        output_metadata = getattr(data_serializer, "output_metadata", None)
        if output_metadata is not None:
            return output_metadata

        input_data = {
            field_name: self.get_field_info(field)
            for field_name, field in data_serializer.fields.items()
            if not any(isinstance(field, field_type) for field_type in self.skip_fields)
        }

        if isinstance(serializer, ListSerializer):
            input_data = [input_data]

        return input_data

    def get_field_info(self, field: Union[Field, Serializer, ListSerializer]) -> DictOrListOfDicts:
        if getattr(field, "child", False):
            if isinstance(field, DictField):
                return {"<key>": self.get_field_info(field.child)}
            return [self.get_field_info(field.child)]
        if getattr(field, "fields", False):
            return self.get_serializer_info(field)

        field_info = {
            "type": self.label_lookup[field],
            "required": getattr(field, "required", False),
        }

        for attr in self.used_attrs:
            value = getattr(field, attr, None)
            if value is not None and value != "":
                info = force_str(value, strings_only=True)
                if attr == "label" and info.lower() == field.field_name.lower().replace("_", " "):
                    continue
                field_info[attr] = info

        if (
            not getattr(field, "read_only", False)
            and hasattr(field, "choices")
            and not isinstance(field, (RelatedField, ManyRelatedField))
        ):
            field_info["choices"] = list(field.choices)

        return field_info


class SerializerAsOutputMetadata(APIMetadata):
    """Metadata class that presumes that view serializer is used as response data with no request data."""

    def determine_actions(self, request: Request, view: ViewProtocol) -> DictOrListOfDicts:
        """Return information about the fields that are accepted for methods in self.recognized_methods."""
        actions = {}
        for method in self.recognized_methods & set(view.allowed_methods):
            view.request = clone_request(request, method)

            input_serializer = self.get_input_serializer(view)

            actions[method] = {
                "input": {},
                "output": self.get_serializer_info(input_serializer),
                "exceptions": getattr(input_serializer, "error_codes", {}),
            }
            view.request = request

        return actions
