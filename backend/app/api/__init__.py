from .endpoints import jobs as jobs_endpoint

router = APIRouter()

include_router(jobs_endpoint.router, prefix="/jobs")
