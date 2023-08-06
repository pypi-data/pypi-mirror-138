from django.db import models
from djangoldp.models import Model

# Our main contact class
class Contact (Model):
    name = models.CharField(max_length=50, verbose_name="Nom du contact")
    firstname = models.CharField(max_length=50, verbose_name="Prénom du contact")
    mail = models.CharField(max_length=50, verbose_name="Email du contact")
    phone = models.CharField(blank=True, null=True, max_length=50, verbose_name="Numéro de téléphone du contact")
    visibility = models.BooleanField(verbose_name="Visible sur la plate-forme", default=False)

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']

    def __str__(self):
        return self.name 

# Our Keyword class
class Keyword (Model):
    name = models.CharField(max_length=50, verbose_name="Mot clé")
    
    class Meta :
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Thematique (Model):
    name = models.CharField(max_length=50, verbose_name="Thématique")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Associatedlink (Model):
    associatedlink = models.URLField(verbose_name="Lien associé", null=True)
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.associatedlink

class Associateddoc (Model):
    associateddoc = models.CharField(max_length=50, verbose_name="Document associé")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.associateddoc

class Pedagogictool (Model):
    name = models.CharField(max_length=150, verbose_name="Nom de l'outil pédagogique")
    desc = models.CharField(max_length=250, blank=True, null=True, verbose_name="Description courte de l'outil pédagogique")
    doc = models.URLField(max_length=250, blank=True, null=True, verbose_name="lien vers l'outil pédagogique")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Illustration (Model):
    illustrationlink = models.URLField(verbose_name="Illustration de l'exposition")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.illustrationlink

class Presslink (Model):
    presslink = models.URLField(verbose_name="Lien vers la revue de presse")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.presslink

class Condition (Model):
    name = models.CharField(max_length=50, verbose_name="Condition de prêt")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Matoscondition (Model):
    name = models.CharField(max_length=50, verbose_name="Condition de prêt")
    
    class Meta : 
        anonymous_perms = ['view']
 
    def __str__(self):
        return self.name

class Public (Model):
    name = models.CharField(max_length=50, verbose_name="Public concerné")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Promoteddoc (Model):
    name = models.CharField(max_length=50, verbose_name="Nom du document mis en avant")
    doc = models.URLField(blank=True, null=True, verbose_name="Document mis en avant")
    img = models.URLField(blank=True, null=True, verbose_name="Ilustration du document")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name


class Promotedlink (Model):
    name = models.CharField(max_length=50, verbose_name="Nom du lien mis en avant")
    link = models.URLField(blank=True, null=True, verbose_name="Lien mis en avant")
    img = models.URLField(blank=True, null=True, verbose_name="Ilustration du lien")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Promotedvideo (Model):
    name = models.CharField(max_length=50, verbose_name="Nom de la vidéo mise en avant")
    video = models.URLField(blank=True, null=True, verbose_name="Lien de la vidéo  mise en avant")
    
    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Structureexpo (Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Nom de la structure")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Structuremateriel (Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Nom de la structure")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']
 
    def __str__(self):
        return self.name

class Expo (Model):
    username = models.CharField(max_length=50, blank=True, null=True,verbose_name="Login de l'utilisateur")
    structure =  models.ForeignKey(Structureexpo, max_length=50,  blank=True, null=True, on_delete=models.CASCADE,verbose_name="Structure")
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Adresse")
    postcode  = models.CharField(max_length=6, blank=True, null=True, verbose_name="Code postal")
    city  = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ville")
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Lattitude")
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Longitude") 
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="Titre de l'exposition")
    contact = models.ManyToManyField(Contact,max_length=50, blank=True, verbose_name="Contact")
    keyword = models.ManyToManyField(Keyword, blank=True, verbose_name="mot clé")
    thematique = models.ManyToManyField(Thematique, blank=True, verbose_name="Thématique")
    description = models.TextField(blank=True, null=True, verbose_name="Description succinte de l'exposition")
    link= models.URLField(blank=True, null=True, verbose_name="Lien internet")
    descriptive = models.TextField(blank=True, null=True, verbose_name="Descriptif du contenu de l'exposition")
    dimension = models.IntegerField(blank=True, null=True, verbose_name="Dimension")
    productiondate = models.IntegerField(blank=True, null=True, verbose_name="Date de production")
    associatedlink = models.ManyToManyField(Associatedlink,max_length=150, blank=True, verbose_name="Lien associé")
    associateddoc = models.ManyToManyField(Associateddoc,max_length=50, blank=True, verbose_name="Doc associé")
    pedagogictool = models.ManyToManyField(Pedagogictool,max_length=150, blank=True, verbose_name="Outil pédagogique")
    illustration = models.ManyToManyField(Illustration,max_length=150, blank=True, verbose_name="Illustration de l'exposition")
    condition = models.ManyToManyField(Condition,max_length=50, blank=True, verbose_name="Condition de prêt")
    price = models.CharField(max_length=15, blank=True, null=True, verbose_name="Tarif")
    public = models.ManyToManyField(Public,max_length=150, blank=True, verbose_name="Public concerné")
    publicprecision = models.CharField(max_length=150, blank=True, null=True, verbose_name="Précision sur le public")
    presslink = models.ManyToManyField(Presslink,max_length=50, blank=True, verbose_name="Revue de presse")
    promoteddoc = models.ManyToManyField(Promoteddoc,max_length=50, blank=True, verbose_name="Document mis en avant")
    promotedlink = models.ManyToManyField(Promotedlink,max_length=50, blank=True, verbose_name="Lien mis en avant")
    promotedvideo = models.ManyToManyField(Promotedvideo,max_length=50, blank=True, verbose_name="Vidéo mise en avant")
    archived = models.BooleanField(verbose_name="exposition archivée", blank=True, null=True, default=False)

    class Meta : 
        anonymous_perms = ['view', 'add', 'change', 'delete']
        authenticated_perms = ['view', 'add', 'change', 'control', 'delete']

    def __str__(self):
        return self.title 


class Materiel (Model):
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name="Login de l'utilisateur")
    structure =  models.ForeignKey(Structuremateriel,max_length=50,  blank=True, null=True, on_delete=models.CASCADE,verbose_name="Structure")
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name="Adresse")
    postcode  = models.CharField(max_length=6, blank=True, null=True, verbose_name="Code postal")
    city  = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ville")
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Lattitude")
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Longitude") 
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom du matériel")
    contact = models.ManyToManyField(Contact,max_length=50, blank=True, verbose_name="Contact")
    illustration = models.ManyToManyField(Illustration,max_length=150, blank=True, verbose_name="Illustration du matériel")
    description = models.TextField(blank=True, null=True, verbose_name="Description des éléments")
    keyword = models.ManyToManyField(Keyword, blank=True)
    withdrawaldate = models.DateField(blank=True, null=True, verbose_name="Date limite de retrait")
    availabilitydate = models.DateField(blank=True, null=True, verbose_name="Date de mise à disposition")
    location = models.CharField(max_length=150, blank=True, null=True, verbose_name="Lieu de retrait")
    modalite = models.TextField(blank=True, null=True, verbose_name="Modalités")
    condition = models.ForeignKey(Matoscondition,max_length=50, blank=True, null=True, on_delete=models.CASCADE,verbose_name="Condition de prêt")
    promotedvideo = models.ManyToManyField(Promotedvideo,max_length=50, blank=True, verbose_name="Vidéo mise en avant")
    archived = models.BooleanField(verbose_name="matériel archivé", blank=True, null=True, default=False)

    class Meta : 
        nested_fields=['condition']
        anonymous_perms = ['view', 'add', 'change', 'control', 'delete']
        authenticated_perms = ['view', 'add', 'change', 'control', 'delete']

    def __str__(self):
        return self.title
