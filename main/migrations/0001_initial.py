# Generated by Django 4.0.3 on 2022-04-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('uploadedFile', models.FileField(upload_to='UploadedFiles/')),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='packet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pack', models.IntegerField()),
                ('time', models.CharField(default='', max_length=50)),
                ('source_ip', models.CharField(default='', max_length=200)),
                ('destination_ip', models.CharField(default='', max_length=200)),
                ('info', models.CharField(default='', max_length=200)),
                ('src_mac', models.CharField(default='', max_length=20)),
                ('dst_mac', models.CharField(default='', max_length=20)),
                ('ext_info', models.CharField(default='', max_length=200)),
                ('src_port', models.CharField(default='', max_length=10)),
                ('dst_port', models.CharField(default='', max_length=10)),
                ('ttl', models.IntegerField(default=0)),
                ('ip_type', models.CharField(default='', max_length=5)),
                ('protocol', models.CharField(default='', max_length=10)),
                ('packet_length', models.IntegerField(default=0)),
                ('country1', models.CharField(default='', max_length=50)),
                ('city1', models.CharField(max_length=50)),
                ('long1', models.CharField(default='', max_length=50)),
                ('lat1', models.CharField(default='', max_length=50)),
                ('country2', models.CharField(default='', max_length=50)),
                ('city2', models.CharField(max_length=50)),
                ('long2', models.CharField(default='', max_length=50)),
                ('lat2', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
