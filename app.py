from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
import json

app = FastAPI()

LAVIS_TOKEN = "replace_me_lavis"
GEOM_TOKEN = "replace_me_geom"

def check_bearer(auth_header: str | None, expected: str):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth_header.split(" ", 1)[1].strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/lavis")
async def lavis(
    image: UploadFile = File(...),
    payload: str = Form(...),
    authorization: str | None = Header(default=None),
):
    check_bearer(authorization, LAVIS_TOKEN)
    data = json.loads(payload)
    # TODO: replace with real model logic
    return {
        "backend": "lavis_service",
        "caption": data.get("caption_hint", ""),
        "vqa": {
            "required_entities_present": True,
            "required_labels_present": True
        },
        "scores": {
            "lavis_required_entity_support": 1.0,
            "lavis_required_label_support": 1.0,
            "lavis_caption_alignment": 0.9
        }
    }

@app.post("/geometry")
async def geometry(
    image: UploadFile = File(...),
    payload: str = Form(...),
    authorization: str | None = Header(default=None),
):
    check_bearer(authorization, GEOM_TOKEN)
    data = json.loads(payload)
    # TODO: replace with real model logic
    return {
        "backend": "geometry_service",
        "detected_entities": data.get("required_entities", []),
        "masks": [],
        "metrics": {
            "entity_detect_recall": 1.0,
            "mask_overlap_rate": 0.05,
            "boundary_clarity_score": 0.85,
            "layout_spacing_violations": 0
        }
    }
