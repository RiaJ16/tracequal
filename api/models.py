# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Verdict(models.CharField):
    def db_type(self, connection):
        return 'verdict'


class Project(models.Model):
    name = models.CharField()
    date = models.DateField(default=models.functions.Now)
    description = models.CharField()

    class Meta:
        managed = False
        db_table = 'project'

    def __str__(self):
        return self.name


class ArtifactBase(models.Model):
    key = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, default='')
    date = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Artifact(ArtifactBase):

    class Meta:
        managed = False
        db_table = 'artifact'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Change(models.Model):
    artifact = models.ForeignKey(Artifact, models.DO_NOTHING, blank=True, null=True)
    changes = models.TextField(blank=True, null=True)  # This field type is a guess.
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'change'


class Code(ArtifactBase):
    document = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'code'

    def __str__(self):
        return f"Code artifact {self.id}: {self.name}"


class Comment(models.Model):
    change = models.ForeignKey(Change, models.DO_NOTHING)
    user = models.ForeignKey('Usr', models.DO_NOTHING)
    comment = models.CharField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Design(ArtifactBase):
    diagram = models.ImageField(upload_to='diagrams/')
    document = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'design'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Link(models.Model):
    from_field = models.ForeignKey(Artifact, models.DO_NOTHING, db_column='from_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to = models.ForeignKey(Artifact, models.DO_NOTHING, related_name='link_to_set', blank=True, null=True)
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link'


class Options(models.Model):
    project = models.OneToOneField('Project', models.DO_NOTHING, primary_key=True)
    prefix_us = models.CharField(blank=True, null=True, default="US")
    prefix_req = models.CharField(blank=True, null=True, default="UC")
    prefix_design = models.CharField(blank=True, null=True, default="D")
    prefix_code = models.CharField(blank=True, null=True, default="C")
    prefix_test = models.CharField(blank=True, null=True, default="TC")

    class Meta:
        managed = False
        db_table = 'options'


class Progress(models.Model):
    project = models.OneToOneField('Project', models.DO_NOTHING, primary_key=True)
    progress_requirements = models.FloatField(blank=True, null=True, default=0)
    progress_design = models.FloatField(blank=True, null=True, default=0)
    progress_code = models.FloatField(blank=True, null=True, default=0)
    progress_tests = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'progress'


class Requirement(ArtifactBase):
    preconditions = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    sequence = ArrayField(models.CharField(max_length=150), blank=True, null=True)  # This field type is a guess.
    alt_sequence = models.JSONField(blank=True, null=True)
    postcondition = models.CharField(blank=True, null=True)
    notes = models.CharField(blank=True, null=True)
    document = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requirement'


class Test(ArtifactBase):
    application_date = models.DateTimeField(blank=True, null=True)
    objective = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    verdict = Verdict(blank=True, null=True, default="not tested")
    notes = models.CharField(blank=True, null=True)
    document = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class TestApplication(models.Model):
    test = models.ForeignKey(
        Test, models.DO_NOTHING, related_name="test_applications")
    date = models.DateTimeField(default=timezone.now)
    application_date = models.DateTimeField(blank=True, null=True)
    verdict = Verdict(blank=True, null=True, default="not tested")
    data = models.JSONField(blank=True, null=True)
    notes = models.CharField(blank=True, null=True)
    document = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_application'


class UserProject(models.Model):
    user = models.ForeignKey('Usr', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    role = models.TextField(blank=True, null=True)  # This field type is a guess.
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_project'


class UserStory(ArtifactBase):
    role = models.CharField()
    actn = models.CharField()
    benefit = models.CharField()

    class Meta:
        managed = False
        db_table = 'user_story'

    def __str__(self):
        pid = 0
        if self.project:
            pid = self.project.id
        return f"User story {pid}{self.key:03d}: {self.role}, {self.actn}, {self.benefit}"


class Usr(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    lastname2 = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'usr'

