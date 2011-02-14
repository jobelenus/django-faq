from django.db import models
from django.db.models.query import QuerySet
from multilingual import manager
import datetime
import enums


class QuestionQuerySet(QuerySet):
    """
    A basic ''QuerySet'' subclass, provides query functionality and some helper methods for an intuitive interface.
    
    """
    
    def active(self, **kwargs):
        """
        A utility method that filters results based on ''Question'' models that are only ''Active''.

        """

        group = kwargs.get('group', False)
        topic = kwargs.get('topic', False)

        qs = self.filter(status__exact=enums.STATUS_ACTIVE,)

        if kwargs.get('slug'):
            slug = kwargs['slug']
            return qs.filter(status__exact=enums.STATUS_ACTIVE, slug__exact=slug)

        if group:
            qs = self.exclude(status__exact=enums.STATUS_INACTIVE,)
        if topic:
            qs = qs.filter(status__exact=enums.STATUS_ACTIVE, topic=topic)
        return qs


class QuestionManager(manager.Manager):
    """
    A basic ''Manager'' subclass which returns a ''QuestionQuerySet''. It provides simple access to helpful utility methods.  
    """

    def get_query_set(self):
        return QuestionQuerySet(self.model)

    def active(self, slug=None, topic=False, group=False, user=None ):
        qs = self.get_query_set().active(slug=slug,topic=topic,group=group)
        if not user or not user.is_authenticated():
            return qs.exclude(protected=True)
        return qs
