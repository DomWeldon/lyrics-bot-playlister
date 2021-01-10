# Create a team
resource "sentry_team" "main" {
  organization = sentry_organization.default.id
  name         = var.sentry_team
  slug         = var.sentry_team_slug
}

resource "sentry_project" "main" {
  organization = sentry_organization.default.id
  team         = sentry_team.main.id
  name         = var.project_name
  slug         = var.project_name
  platform     = "python"
  resolve_age  = 720
}

resource "sentry_organization" "default" {
  name        = var.sentry_organization
  slug        = var.sentry_organization_slug
  agree_terms = true
}

resource "sentry_key" "asgi" {
  organization = sentry_organization.default.id
  project      = sentry_project.main.id
  name         = "${var.project_name} ASGI / ${var.environment_name}"
}
