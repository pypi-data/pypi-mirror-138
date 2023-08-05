from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class DomainConfigTag(EmbeddedDocument):
    key = StringField(max_length=255)
    value = StringField(max_length=255)


class DomainConfig(MongoModel):
    name = StringField(max_length=255, unique_with='domain_id')
    data = DictField()
    tags = ListField(EmbeddedDocumentField(DomainConfigTag))
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)

    meta = {
        'updatable_fields': [
            'name',
            'data',
            'tags'
        ],
        'minimal_fields': [
            'name'
        ],
        'ordering': [
            'name'
        ],
        'indexes': [
            'name',
            'domain_id',
            ('tags.key', 'tags.value')
        ]
    }
