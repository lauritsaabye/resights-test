import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from networkx.exception import NodeNotFound, NetworkXNoPath
from lib.graph import bootstrap_graph, fetch_target_share

with open('data/CasaAS.json', 'r') as f:
    network = json.load(f)

# Bootstrap
graph = bootstrap_graph(network)
app = FastAPI()


# Validation
class ShareRangeRequest(BaseModel):
    source: str
    target: str


# Endpoint
@app.get("/share-range")
def read_share_range(request: ShareRangeRequest):
    try:
        target_share = fetch_target_share(source=request.source, target=request.target, data=graph)
    except NodeNotFound:
        # TODO: increase 404 specificity - Which node is not found?
        raise HTTPException(status_code=404, detail="Source or target node not found")
    except NetworkXNoPath:
        raise HTTPException(status_code=400, detail="Source and target have no direct path")
    return target_share
