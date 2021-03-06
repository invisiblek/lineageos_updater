from __future__ import absolute_import

from mongoengine import Document, BooleanField, DateTimeField, StringField, IntField

from datetime import datetime, timedelta

def default_time():
    return datetime.now() - timedelta(minutes=60)

class Rom(Document):
    filename = StringField(required=True)
    datetime = DateTimeField(required=True, default=default_time)
    device = StringField(required=True)
    version = StringField(required=True)
    romtype = StringField(required=True)
    md5sum = StringField(required=True)
    url = StringField()
    romsize = IntField()
    hasbootimg = BooleanField(default=False)
    sticky = BooleanField(default=False)

    @classmethod
    def get_roms(cls, device, romtype=None, before=3600):
        args = {
            'device': device,
            'romtype': romtype,
            'datetime__lt': datetime.now()-timedelta(seconds=before)
        }
        if before == 0:
            del args['datetime__lt']
        if not romtype:
            del args['romtype']
        return cls.objects(**args).order_by('-datetime')

    @classmethod
    def get_devices(cls):
        #TODO change this to an aggregate
        return cls.objects().distinct(field="device")

    @classmethod
    def get_types(cls, device):
        return cls.objects().distinct(field="romtype")

    @classmethod
    def get_current_devices_by_version(cls):
        # db.rom.aggregate({'$group': {'_id': '$version', 'device': {'$push': '$device'}}})
        versions = {}
        for version in cls.objects().aggregate({'$group': {'_id': '$version', 'devices': {'$push': '$device'}}}):
            versions[version['_id']] = version['devices']
        return versions

    @classmethod
    def get_device_version(cls, device):
        if not device:
            return None
        return cls.objects(device=device).first()['version']

class Incremental(Document):
    filename = StringField(required=True)
    datetime = DateTimeField(required=True, default=default_time)
    device = StringField(required=True)
    version = StringField(required=True)
    romtype = StringField(required=True)
    md5sum = StringField(required=True)
    url = StringField()
    romsize = IntField()
    from_incremental = StringField(required=True)
    to_incremental = StringField(required=True)

    @classmethod
    def get_incrementals(cls, device, romtype=None, before=3600, incremental=None):
        args = {
            'device': device,
            'romtype': romtype,
            'datetime__lt': datetime.now()-timedelta(seconds=before),
            'from_incremental': incremental
        }
        if before == 0:
            del args['datetime__lt']
        if not romtype:
            del args['romtype']
        return cls.objects(**args).order_by('-datetime')

    @classmethod
    def get_devices(cls):
        #TODO change this to an aggregate
        return cls.objects().distinct(field="device")

    @classmethod
    def get_types(cls, device):
        return cls.objects().distinct(field="romtype")

    @classmethod
    def get_current_devices_by_version(cls):
        # db.rom.aggregate({'$group': {'_id': '$version', 'device': {'$push': '$device'}}})
        versions = {}
        for version in cls.objects().aggregate({'$group': {'_id': '$version', 'devices': {'$push': '$device'}}}):
            versions[version['_id']] = version['devices']
        return versions

    @classmethod
    def get_device_version(cls, device):
        if not device:
            return None
        return cls.objects(device=device).first()['version']

class Device(Document):
    model = StringField(required=True, unique=True)
    oem = StringField(required=True)
    name = StringField(required=True)
    has_recovery = BooleanField(required=False, default=True)
    meta = {'strict': False}

    @classmethod
    def get_devices(cls):
        return cls.objects()

class ApiKey(Document):
    apikey = StringField(required=True)
    comment = StringField(required=False)
