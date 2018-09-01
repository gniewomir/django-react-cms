import uuid

from django.db import models


class AbstractComponentType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    react_name = models.CharField(max_length=120)
    allowed_children_types = models.ManyToManyField('self', blank=True,
                                                    symmetrical=False,
                                                    help_text='Component types that are allowed to be children of this component')

    class Meta:
        abstract = True


class ComponentType(AbstractComponentType):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Component type'
        verbose_name_plural = 'Component type'


class AbstractComponentInstance(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    children = models.ManyToManyField('self', blank=True,
                                      symmetrical=False,
                                      help_text='Component types that are allowed to be children of this component.')

    class Meta:
        abstract = True


class ComponentInstance(AbstractComponentInstance):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Component instance'
        verbose_name_plural = 'Component instances'


class AbstractScene(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    root_component = models.ForeignKey(ComponentInstance, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Scene(AbstractScene):
    class Meta:
        verbose_name = 'Scene'
        verbose_name_plural = 'Scenes'
