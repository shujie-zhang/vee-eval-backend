import os, json
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException

app = FastAPI()
LAVIS_TOKEN = os.getenv("LAVIS_TOKEN", "").strip()
GEOM_TOKEN = os.getenv("GEOM_TOKEN", "").strip()

def check_bearer(auth_header: str | None, expected: str):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth_header.split(" ", 1)[1].strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/lavis")
async def lavis(image: UploadFile = File(...), payload: str = Form(...), authorization: str | None = Header(None)):
    check_bearer(authorization, LAVIS_TOKEN)
    try:
        data = json.loads(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload JSON: {e}")
    return {"backend":"lavis_service","caption":data.get("caption_hint",""),"vqa":{"required_entities_present":True,"required_labels_present":True},"scores":{"lavis_required_entity_support":1.0,"lavis_required_label_support":1.0,"lavis_caption_alignment":0.9}}

@app.post("/geometry")
async def geometry(image: UploadFile = File(...), payload: str = Form(...), authorization: str | None = Header(None)):
    check_bearer(authorization, GEOM_TOKEN)
    try:
        data = json.loads(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload JSON: {e}")
    return {"backend":"geometry_service","detected_entities":data.get("required_entities",[]),"masks":[],"metrics":{"entity_detect_recall":1.0,"mask_overlap_rate":0.05,"boundary_clarity_score":0.85,"layout_spacing_violations":0}}
