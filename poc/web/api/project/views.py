from poc.db.models.todos import Project
from poc.web.api.project.schema import PartialProject, Project as ProjectSchema, PersistedProject

from poc.web.api import create_router

router = create_router(PersistedProject, ProjectSchema, Project, 'project', partial_model=PartialProject)

