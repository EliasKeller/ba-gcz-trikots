import json

from django.utils.safestring import mark_safe
from django import forms


class ListWidget(forms.Widget):
    """
    Verwendung:
        from trikots.widgets import ListWidget

        class MyAdminForm(forms.ModelForm):
            class Meta:
                model = MyModel
                fields = "__all__"
                widgets = {
                    "my_json_field": ListWidget(),
                    "another_json_field": ListWidget(placeholder="Eintrag hinzufügen..."),
                }
    """

    def __init__(self, placeholder="", *args, **kwargs):
        self.placeholder = placeholder
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        items = (
            value
            if isinstance(value, list)
            else (json.loads(value) if value and value != "null" else [])
        )

        rows_html = ""
        for item in items:
            safe_item = str(item).replace('"', "&quot;")
            rows_html += f"""
            <div class="list-row" style="display:flex;gap:8px;margin-bottom:6px;">
                <input type="text" value="{safe_item}" class="list-item-input vTextField"
                    style="width:400px;" placeholder="{self.placeholder}">
                <button type="button" onclick="this.parentElement.remove()"
                    style="background:#ba2121;color:white;border:none;padding:4px 10px;
                           cursor:pointer;border-radius:3px;">✕</button>
            </div>"""

        return mark_safe(f"""
            <div id="wrap-{name}">
                <div id="rows-{name}">{rows_html}</div>
                <button type="button" id="add-{name}"
                    style="background:#417690;color:white;border:none;padding:5px 12px;
                           cursor:pointer;border-radius:3px;margin-top:4px;">
                    + Eintrag hinzufügen
                </button>
                <input type="hidden" name="{name}" id="id-{name}">
            </div>
            <script>
                (function(){{
                    document.getElementById('add-{name}').addEventListener('click', function(){{
                        var d = document.createElement('div');
                        d.className = 'list-row';
                        d.style = 'display:flex;gap:8px;margin-bottom:6px;';
                        d.innerHTML = '<input type="text" class="list-item-input vTextField" '
                            + 'style="width:400px;" placeholder="{self.placeholder}">'
                            + '<button type="button" onclick="this.parentElement.remove()" '
                            + 'style="background:#ba2121;color:white;border:none;padding:4px 10px;'
                            + 'cursor:pointer;border-radius:3px;">✕</button>';
                        document.getElementById('rows-{name}').appendChild(d);
                    }});

                    document.getElementById('wrap-{name}').closest('form').addEventListener('submit', function(){{
                        var vals = Array.from(document.querySelectorAll('#rows-{name} .list-item-input'))
                            .map(function(i){{ return i.value.trim(); }})
                            .filter(function(v){{ return v !== ''; }});
                        document.getElementById('id-{name}').value = JSON.stringify(vals);
                    }});
                }})();
            </script>
        """)

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, "[]")
        try:
            return json.loads(raw)
        except Exception:
            return []