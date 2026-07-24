# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import app.db.base_class  # noqa: F401 — registers all models with SQLAlchemy mapper
from app.api.v1.auth.refresh import router as refresh_router
from app.api.v1.auth.google import router as google_auth_router
from app.api.v1.auth.logout import router as logout_router
from app.api.v1.events.router import router as events_router
from app.api.v1.admin.users import router as admin_users_router
from app.api.v1.users import router as users_router
from app.api.v1.projects.router import router as projects_router
from app.api.v1.blogposts.router import router as blogposts_router
from app.api.v1.admin.blogposts.router import router as admin_blogposts_router
from app.api.v1.comments.router import router as comments_router
from app.api.v1.admin.comments import router as admin_comments_router
from app.api.v1.admin.projects import router as admin_projects_router
from app.api.v1.admin.events import router as admin_events_router
from app.api.v1.admin.stats import router as admin_stats_router
from app.api.v1.community import router as community_router
from app.api.v1.team import router as team_router
from app.api.v1.public_forms import router as public_forms_router
from app.api.v1.media.upload import router as media_router

app = FastAPI(title="Google Developer Group on Campus, UNN Community API")

# ── Middleware ────────────────────────────────────────────────────────────
# Auth is stateless bearer tokens — no session middleware and no cookies, so
# allow_credentials stays off and the Authorization header carries the session.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Include API routes
app.include_router(refresh_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(logout_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(google_auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(events_router, prefix="/api/v1/events", tags=["events"])
app.include_router(admin_users_router, prefix="/api/v1/admin/users", tags=["admin users"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(blogposts_router, prefix="/api/v1/blogposts", tags=["blogposts"])
app.include_router(admin_blogposts_router, prefix="/api/v1/admin/blogposts", tags=["admin blogposts"])
app.include_router(admin_comments_router, prefix="/api/v1/admin/comments", tags=["admin comments"])
app.include_router(admin_projects_router, prefix="/api/v1/admin/projects", tags=["admin projects"])
app.include_router(admin_events_router, prefix="/api/v1/admin/events", tags=["admin events"])
app.include_router(admin_stats_router, prefix="/api/v1", tags=["admin stats"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(community_router, prefix="/api/v1/community", tags=["community"])
app.include_router(team_router, prefix="/api/v1", tags=["team"])
from app.api.v1.hackathon.router import router as hackathon_router

app.include_router(public_forms_router, prefix="/api/v1/public/forms", tags=["public forms"])
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])
app.include_router(hackathon_router, prefix="/api/v1/hackathon", tags=["hackathon"])
@app.get("/")
async def root():
    return {"message": "Welcome to the GDGoC, UNN Community API!"}
