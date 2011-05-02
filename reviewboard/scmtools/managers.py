from django.db.models import Manager, Q


class RepositoryManager(Manager):
    """A manager for Repository models."""
    def accessible(self, user, visible_only=True, local_site=None):
        """Returns repositories that are accessible by the given user."""
        if user.is_superuser:
            qs = self.all()
        else:
            q = Q(public=True)

            if visible_only:
                q = q & Q(visible=True)

            if user.is_authenticated():
                q = q | (Q(users__pk=user.pk) |
                         Q(review_groups__users=user.pk))

            qs = self.filter(q).distinct()

        return qs.filter(local_site=local_site)

    def can_create(self, user, local_site=None):
        return (user.has_perm('scmtools.create_repository') or
                (local_site and
                 local_site.admins.filter(pk=user.pk).exists()))


class ToolManager(Manager):
    """A manager for SCM Tool model"""
    def get_by_natural_key(self, class_name):
        """Return a scm for a given class name"""
        return self.get(class_name=class_name)
