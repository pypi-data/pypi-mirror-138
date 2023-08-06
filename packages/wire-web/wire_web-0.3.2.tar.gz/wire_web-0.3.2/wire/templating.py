from fuchs import FuchsTemplate
from wire.response import HTMLResponse

class FoxTemplates(FuchsTemplate):
    def __init__(self, dirname: str):
        super().__init__(dirname=dirname)

    def render(self, template_name: str, **kwargs) -> bytes:
        html = super().render(template_name, **kwargs)
        return HTMLResponse(html) 