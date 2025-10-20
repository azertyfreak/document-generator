
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
from docxtpl import DocxTemplate
from datetime import date
import io, json, os
from jsonschema import Draft202012Validator

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(BASE_DIR, "overeenkomst_jinja.docx")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.json")

app = FastAPI(title="Verkoopovereenkomst API", version="1.0.0")

# CORS (pas origins aan naar je frontend-domein indien gewenst)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load schema & validator
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = json.load(f)
VALIDATOR = Draft202012Validator(SCHEMA)

class Dossier(BaseModel):
    context: dict

@app.get("/", response_class=HTMLResponse)
def root():
    return """
<h2>Verkoopovereenkomst API</h2>
<ul>
  <li><a href="/docs">Interactieve documentatie</a></li>
  <li><a href="/schema">JSON Schema</a></li>
  <li><a href="/health">Health</a></li>
</ul>
"""

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.get("/schema")
def get_schema():
    return SCHEMA

@app.post("/validate")
def validate_only(d: Dossier):
    errors = sorted(VALIDATOR.iter_errors(d.context), key=lambda e: e.path)
    if errors:
        details = [{
            "path": "/".join([str(p) for p in err.path]),
            "message": err.message
        } for err in errors]
        raise HTTPException(status_code=422, detail=details)
    return {"ok": True}

@app.post("/genereer/docx")
def genereer_docx(d: Dossier):
    errors = sorted(VALIDATOR.iter_errors(d.context), key=lambda e: e.path)
    if errors:
        details = [{
            "path": "/".join([str(p) for p in err.path]),
            "message": err.message
        } for err in errors]
        raise HTTPException(status_code=422, detail=details)

    tpl = DocxTemplate(TEMPLATE_PATH)
    ctx = dict(d.context)
    meta = ctx.get("meta") or {}
    meta.setdefault("datum_vandaag", date.today().isoformat())
    ctx["meta"] = meta

    tpl.render(ctx)
    out_buf = io.BytesIO()
    tpl.save(out_buf)
    return Response(content=out_buf.getvalue(),
                    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": "attachment; filename=overeenkomst_out.docx"})
