from abc import ABCMeta, abstractmethod
from typing import Any, Optional, TYPE_CHECKING, Type, Union

from django.core import checks
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field, Model
from django_jsonfield_backport.models import JSONField

if TYPE_CHECKING:
    from .json_model import JSONModel


class BaseJSONModelField(JSONField, metaclass=ABCMeta):
    """
    A subclass of JSONField that allows defining a specific model for the data stored in a JSON field.
    """

    def get_formfield_kwargs(self, **kwargs):
        return kwargs

    def formfield(self, **kwargs):
        from django_json_model_field import forms

        kwargs = self.get_formfield_kwargs(
            form_class=kwargs.pop("form_class", forms.NestedModelFormField),
            **kwargs,
        )

        # don't use super().formfield because the form field doesn't need the same things as the base JSONField
        return Field.formfield(self, **kwargs)

    @abstractmethod
    def get_json_model_class(self, host: Union[Model, dict]) -> Optional[Type["JSONModel"]]:
        """
        Returns the `JSONModel` class to be used to represent the field data
        """

        raise NotImplementedError()

    def from_db_value(self, value, expression, connection):
        # overridden method from Field and JSONField used to convert the DB's JSON (string) value to a dict, and then
        # from the dict to an instance of the JSONModel defined for the field
        data: dict = super().from_db_value(value, expression, connection) or {}

        # FIXME: what's _selector for?
        #  json_model = self.get_json_model_class(host=data.pop("_selector", {}))
        json_model = self.get_json_model_class(host=data.pop("_selector", {}))
        return json_model(_has_input=data is not None, **(data or {}), _skip_clean=True) if json_model else None

    def clean(self, value: Optional[Union[dict, "JSONModel"]], model_instance: Optional[Model]):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        value = self.to_python(value, model_instance)
        self.validate(value, model_instance)
        self.run_validators(value)
        return value

    def to_python(self, value: Optional[Union[dict, "JSONModel"]], model_instance: Model = None) -> Optional["JSONModel"]:
        from django_json_model_field.db.models import JSONModel

        # note: signature is overridden from the base Field signature to include the model instance. This is possible
        #       since the `clean` method is also overridden to pass its model_instance argument along.

        # the value must either already be a JSONModel instance, or a dict that can then be converted to JSONModel
        # instance so that the field validation for that model can be checked before saving
        if isinstance(value, JSONModel):
            return value

        if isinstance(value, dict):
            # Use model initialization to ensure the data is valid and any values are correctly prepped for
            # serialization
            json_model_class = self.get_json_model_class(model_instance)

            if json_model_class is None:
                return None

            return json_model_class(**value)

        return None

    def validate(self, value: Optional["JSONModel"], model_instance: Optional[Model]):
        if value is not None:
            value.full_clean()

        # the JSONField superclass validates whether the value is valid JSON, so it needs the data in dict form
        super().validate(value.get_prep_value() if value else None, model_instance)

    def get_prep_value(self, value):
        if value is None or value == {}:
            return None

        if isinstance(value, dict):
            # already prepped (e.g. from get_db_prep_value), just pass it through
            return super().get_prep_value(value)

        from django_json_model_field.db.models import JSONModel

        if isinstance(value, JSONModel):
            data = self._get_prep_value_from_model(value)
            return super().get_prep_value(data)

        raise TypeError("Cannot prep values that are not instances of JSONModel")

    def _get_prep_value_from_model(self, instance: "JSONModel") -> dict:
        return instance.get_prep_value()

    def get_db_prep_value(self, value, connection, prepared=False):
        if prepared:
            raise NotImplementedError()

        if value is None or value == {}:
            return None

        from django_json_model_field.db.models import JSONModel

        if isinstance(value, JSONModel):
            data = self._get_db_prep_value_from_model(value, connection)
            return super().get_db_prep_value(data, connection, prepared)

        return super().get_db_prep_value(value, connection, prepared)

    def _get_db_prep_value_from_model(self, instance: "JSONModel", connection) -> dict:
        return instance.get_db_prep_value(connection)

    def check(self, **kwargs):
        """
        Extends the base field checks to also include model checks for the JSONModel class

        Checks are run once during the Django app startup - running the JSONModel checks from here allows the checks
        to be evaluated for JSONModel classes that are used by fields without having to also implement an additional
        registry for JSONModel classes to integrate with Django's checks system (see check_all_models in
        django/core/checks/model_checks.py). If a use case for using JSONModel classes outside a BaseJSONModelField emerges,
        this approach will need to be reconsidered.
        """

        errors = super().check(**kwargs)
        errors.extend(self._check_null())
        errors.extend(self._check_json_model_arguments())

        return errors

    def _check_null(self):
        """
        Checks the `null` and `blank` arguments to make sure they are both True. To prevent duplicate errors from being
        surfaced to the end user, JSONModelFields are always nullable. Since the actual JSONModel class used to store
        data may vary, all data validation enforcement is deferred to the JSONModel's fields and derived forms.
        """

        errors = []
        if self.null is not True:
            errors.append(checks.Critical("JSONModelFields must set null=True", obj=self))
        if self.blank is not True:
            errors.append(checks.Critical("JSONModelFields must set blank=True", obj=self))

        return errors

    def _check_json_model_arguments(self, **kwargs):
        """
        Checks arguments related to specifying the JSONModel for the field to ensure the right combination of arguments
        was provided, and that the arguments are of valid types.
        """
        return []

    def _check_model_argument(self, model: Any, arg_name: str):
        """
        Verifies that any types provided to be used as JSONModel classes are types that subclass JSONModel
        """

        if not isinstance(model, type):
            return [
                checks.Critical(
                    "Expected a type",
                    obj=model,
                    hint=f"{arg_name} must be a class"
                )
            ]

        from django_json_model_field.db.models import JSONModel

        if not issubclass(model, JSONModel):
            return [
                checks.Critical(
                    "Expected a subclass of JSONModel",
                    obj=model,
                    hint=f"{arg_name} must be a subclass of JSONModel"
                )
            ]

        return []

    def _check_json_models(self, **kwargs):
        """
        Runs model checks on any JSONModel types specified for use in the field.
        """

        return []
