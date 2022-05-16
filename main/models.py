from django.db import models

from zigota.settings import STATIC_URL

from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=STATIC_URL)

class MainPCAP(models.Model):
    name = models.CharField(max_length = 200)

class Document(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "UploadedFiles/",storage=fs, null=True, blank=True)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)



class packet(models.Model):
    id_pack = models.IntegerField()
    time = models.CharField(max_length=50, default='')
    source_ip = models.CharField(max_length=200, default='')
    destination_ip = models.CharField(max_length=200, default='')
    info = models.CharField(max_length=200, default='')
    src_mac = models.CharField(max_length=20, default='')
    dst_mac = models.CharField(max_length=20, default='')
    ext_info = models.CharField(max_length=200, default='')
    src_port = models.CharField(max_length=10, default='')
    dst_port = models.CharField(max_length=10, default='')
    ttl = models.IntegerField(default=0)
    ip_type = models.CharField(max_length=5, default='')
    protocol = models.CharField(max_length=10, default='')
    packet_length = models.IntegerField(default=0)

    country1 = models.CharField(max_length=50, default='')
    city1 = models.CharField(max_length=50)

    long1 = models.CharField(max_length=50, default='')
    lat1 = models.CharField(max_length=50, default='')

    country2 = models.CharField(max_length=50, default='')
    city2 = models.CharField(max_length=50)

    long2 = models.CharField(max_length=50, default='')
    lat2 = models.CharField(max_length=50, default='')

    def to_dict(self):
        return {
            'id_pack': self.id_pack,
            'time': self.time,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip ,
            'info': self.info ,
            'country1': self.country1 ,
            'city1': self.city1,
            'long1': self.long1,
            'lat1': self.lat1 ,
            'country2': self.country2, 
            'city2': self.city2,
            'long2': self.long2,
            'lat2': self.lat2
        }
    def to_dict_pcap(self):
        return {
            'id_pack': self.id_pack,
            'time': self.time,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'country1': self.country1,
            'country2': self.country2
        }

    def to_dict_for_map(self):
            return {
                'id_pack': self.id_pack,
                'source_ip': self.source_ip,
                'destination_ip': self.destination_ip ,
                'country1': self.country1 ,
                'city1': self.city1,
                'long1': self.long1,
                'lat1': self.lat1 ,
                'country2': self.country2, 
                'city2': self.city2,
                'long2': self.long2,
                'lat2': self.lat2
            }


 