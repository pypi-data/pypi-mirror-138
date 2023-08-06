from typing import Any, Dict, Optional, Type, Union, cast

from django.core import checks
from django.db.models import Model

from django_json_model_field.util import get_type_init_with_metaclass

from .base_json_model_field import BaseJSONModelField
from .json_model import JSONModel

from django.utils.text import slugify


class ConditionalJSONModelField(BaseJSONModelField):
    @classmethod
    def _make_selector_json_model_class(
        cls, selector_field: str, selector_value: Any, json_model_class: Type[JSONModel]
    ) -> Type[JSONModel]:
        """
        Subclass each mapped JSONModel class to set the _selector_value attribute - this makes it easier to look up
        later in contexts where we have a reference to the class or an instance of the model, but not the host model or
        form to determine what the selector value is.
        """

        selector_field_title = selector_field.replace("_", " ").title().replace(" ", "")
        select_value_title = (
            slugify(str(selector_value).replace(".", "-")).replace("-", " ").replace("_", " ").title().replace(" ", "")
        )

        # use a more specific name to make debugging easier
        name = f"{json_model_class.__name__}For{selector_field_title}{select_value_title}"
        return get_type_init_with_metaclass(json_model_class)(
            name,
            (json_model_class,),
            {
                "__name__": name,
                "__module__": json_model_class.__module__,
                "__classcell__": getattr(json_model_class, "__classcell__", None),
                "_selector_value": str(selector_value),
            },
        )

    def __init__(
        self,
        selector_field: str,
        model_map: Dict[Any, Type[JSONModel]],
        verbose_name: str = None,
        name: str = None,
        null: bool = True,
        blank: bool = True,
        encoder=None,
        decoder=None,
        **kwargs,
    ):
        """

        Parameters
        ----------
        selector_field The name of the field used to determine which entry from model_map will be used to work with
                       and manipulate the JSON data stored using the field. The field referenced by selector_field
                       must be on the same model as the BaseJSONModelField. Note that values accessed from selector_field
                       will be stringified before looking up the entry in model_map.
                       TODO: support using values from relations
        model_map      A map of possible values from selector_field to the JSONModel that will be used to represent
                       the data. Note that keys will be stringified before being used for lookups. Selector values
                       with missing entries are assumed to have no model and have no data requirements.
                       TODO: add an option to raise a validation or check error for missing entries?
        """
        # validation of model field arguments is handled by Django's checks system - see the `check` method below.

        self.selector_field = selector_field
        self.model_map = {
            str(key): self._make_selector_json_model_class(selector_field, key, value)
            for key, value in model_map.items()
        }

        # make a separate copy of model_map for deconstruction - the original JSONModel classes must be used here since
        # deconstruct is used to generate migrations, and the type returned by make_selector_json_model_class will not
        # get created until the field is initialized at runtime
        self._model_map = {str(key): value for key, value in model_map.items()}

        super().__init__(
            verbose_name=verbose_name,
            name=name,
            encoder=encoder,
            decoder=decoder,
            null=null,
            blank=blank,
            **kwargs,
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args = [self.selector_field, self._model_map, *args]
        return name, path, args, kwargs

    def get_formfield_kwargs(self, **kwargs):
        kwargs = super().get_formfield_kwargs(**kwargs)
        kwargs.update(
            nested_model_class=self.get_json_model_class,
            selector_field=self.selector_field,
        )
        return kwargs

    def get_selector_value(self, host: Union[Model, dict]) -> Optional[Any]:
        """
        Attempts to retrieve the value of the selector_field from the specified host model or data dictionary.
        """

        value = getattr(host, self.selector_field) if isinstance(host, Model) else host.get(self.selector_field)
        return str(value) if value is not None else None

    def get_json_model_class(self, host: Union[Model, dict]) -> Optional[Type[JSONModel]]:
        """
        Returns the `JSONModel` to be used to represent the field data, if one can be determined either from json_model
        or selector_field and model_map.
        """

        selector = self.get_selector_value(host)
        if selector is None:
            return None
        return self.model_map.get(selector)

    def _get_prep_value_from_model(self, instance: JSONModel) -> dict:
        data = super()._get_prep_value_from_model(instance)
        if instance._selector_value:
            data.update(_selector={self.selector_field: instance._selector_value})
        return data

    def _check_json_model_arguments(self, **kwargs):
        """
        Checks arguments related to specifying the JSONModel for the field to ensure the right combination of arguments
        was provided, and that the arguments are of valid types.
        """

        if self.selector_field is None and self.model_map is None:
            return [checks.Critical("Both selector_field and model_map must have a value", obj=self)]

        if self.selector_field is None:
            return [
                checks.Critical(
                    "selector_field must be set to the name of another non-relation field on the model", obj=self
                )
            ]

        if self.model_map is None:
            return [
                checks.Critical(
                    "model_map is required",
                    hint="model_map must be set to a dict mapping of possible selector values to JSONField class types",
                    obj=self,
                )
            ]

        if self.model_map == {}:
            return [
                checks.Critical(
                    "model_map must have a non-empty value",
                    hint="model_map must be set to a dict mapping of possible selector values to JSONField class types",
                    obj=self,
                )
            ]

        selector_field = next((field for field in self.model._meta.fields if field.name == self.selector_field), None)
        if selector_field is None:
            return [
                checks.Critical(
                    f"Invalid selector_field: No field named {self.selector_field}",
                    obj=self,
                )
            ]

        if selector_field.is_relation:
            return [
                checks.Critical(
                    "selector_field cannot be a relation field",
                    obj=self,
                )
            ]

        # cast to make mypy happy - previous checks have already established that model_map is not None
        model_map = cast(Dict[str, Type[JSONModel]], self.model_map)
        errors = []
        for selector_value, json_model in model_map.items():
            errors.extend(self._check_model_argument(json_model, f"model_map[{selector_value}]"))

        return errors or self._check_json_models(**kwargs)

    def _check_json_models(self, **kwargs):
        errors = []
        for json_model in self.model_map.values():
            errors.extend(json_model.check(**kwargs))

        return errors
