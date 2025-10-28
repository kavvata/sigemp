import json
import uuid
from django.forms.widgets import Widget
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe


class ModelAutocompleteWidget(Widget):
    """
    Generic autocomplete widget for forms.ModelChoiceField.

    Args:
      model: a Django model class (not a string).
      field: the model field name to search against (string).
      attrs: standard widget attrs.

    Renders:
      - a visible text input for searching/label display
      - a hidden input that stores the model PK (the actual field value)
      - a results container updated via HTMX
      - AlpineJS state to set both inputs when selecting an item
    """

    template_name = "widgets/autocomplete_widget.html"

    def __init__(
        self,
        model,
        field="__str__",
        attrs=None,
        placeholder="",
        endpoint_name="model_autocomplete",
        min_chars=2,
        limit=10,
        debounce=250,
    ):
        super().__init__(attrs)
        self.model = model
        self.field = field
        self.placeholder = placeholder or f"Buscar {model._meta.verbose_name}"
        self.endpoint_name = endpoint_name
        self.min_chars = min_chars
        self.limit = limit
        self.debounce = debounce

    def get_config(self, name, value, attrs):
        # name: form field name. value: current value (PK).
        uid = uuid.uuid4().hex[:8]
        visible_id = f"ac-visible-{uid}"
        hidden_id = f"ac-hidden-{uid}"
        results_id = f"ac-results-{uid}"
        try:
            initial_label = ""
            if value:
                # try to look up initial label from model
                obj = self.model.objects.filter(pk=value).first()
                if obj:
                    if self.field == "__str__":
                        initial_label = str(obj)
                    else:
                        initial_label = getattr(obj, self.field, "") or ""
        except Exception:
            initial_label = ""
        config = {
            "endpoint": reverse_lazy(self.endpoint_name),
            "app_label": self.model._meta.app_label,
            "model_name": self.model._meta.model_name,
            "field": self.field,
            "min_chars": self.min_chars,
            "limit": self.limit,
            "debounce": self.debounce,
            "hidden_id": hidden_id,
            "results_id": results_id,
            "visible_id": visible_id,
            "initial_value": str(value) if value else "",
            "initial_label": initial_label or "",
        }
        return config, visible_id, hidden_id, results_id

    def render(self, name, value, attrs=None, renderer=None):
        config, visible_id, hidden_id, results_id = self.get_config(name, value, attrs)
        context = {
            "config": config,  # Pass the config object directly
            "visible_id": visible_id,
            "hidden_id": hidden_id,
            "results_id": results_id,
            "name": name,
            "placeholder": self.placeholder,
        }
        html = render_to_string(self.template_name, context)
        return mark_safe(html)
