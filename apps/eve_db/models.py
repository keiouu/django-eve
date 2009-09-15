from xml.dom import minidom
from django.db import models
from eve_proxy.models import CachedDocument
from apps.eve_db.managers import EVEPlayerCorporationManager, EVEPlayerAllianceManager, EVEPlayerCharacterManager
    
class EVEGraphic(models.Model):
    """
    Stored graphic model.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    # Name of the file, should be two numbers separated by underscore, no extension.
    icon_filename = models.CharField(max_length=50)
    is_published = models.BooleanField(default=True)
    is_obsolete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Graphic'
        verbose_name_plural = 'Graphics'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEName(models.Model):
    """
    This appears to be something used to search everything at once. Most of
    the stuff in this table have models with a 'name' field on them. The CCP
    dump doesn't use the eveNames table directly many times.
    
    Things covered by this model include space objects, corporations, and
    people.
    """
    name = models.CharField(max_length=255)
    category = models.ForeignKey('EVEInventoryCategory', blank=True, null=True)
    group = models.ForeignKey('EVEInventoryGroup', blank=True, null=True)
    type = models.ForeignKey('EVEInventoryType', blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Name'
        verbose_name_plural = 'Names'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEUnit(models.Model):
    name = models.CharField(max_length=75)
    display_name = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class EVERace(models.Model):
    """
    An EVE race.
    """
    name = models.CharField(max_length=30)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Race'
        verbose_name_plural = 'Races'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEMarketGroup(models.Model):
    """
    Market groups are used to group items together in the market browser.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    parent = models.ForeignKey('EVEMarketGroup', blank=True, null=True)
    has_items = models.BooleanField(default=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Market Group'
        verbose_name_plural = 'Market Groups'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryCategory(models.Model):
    """
    Inventory categories are the top level classification for all items, be
    it planets, moons, modules, ships, or any other entity within the game
    that physically exists.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Category'
        verbose_name_plural = 'Inventory Categories'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryGroup(models.Model):
    """
    Inventory groups are a further sub-classification within an 
    EVEInventoryCategory. For example, the 'Region' inventory group's
    category is 'Celestial'.
    """
    category = models.ForeignKey(EVEInventoryCategory, blank=True, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    use_base_price = models.BooleanField(default=False)
    allow_manufacture = models.BooleanField(default=True)
    allow_recycle = models.BooleanField(default=True)
    allow_anchoring = models.BooleanField(default=False)
    is_anchored = models.BooleanField(default=False)
    is_fittable_non_singleton = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Group'
        verbose_name_plural = 'Inventory Groups'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryMetaGroup(models.Model):
    """
    Names of variants of items. 
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Meta Group'
        verbose_name_plural = 'Inventory Meta Groups'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryType(models.Model):
    """
    Inventory types are generally objects that can be carried in your
    inventory (with the exception of suns, moons, planets, etc.) These are mostly
    market items, along with some basic attributes of each that are common
    to all items. 
    """
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    group = models.ForeignKey(EVEInventoryGroup, blank=True, null=True)
    market_group = models.ForeignKey(EVEMarketGroup, blank=True, null=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    portion_size = models.IntegerField(blank=True, null=True)
    race = models.ForeignKey('EVERace', blank=True, null=True)
    base_price = models.FloatField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    chance_of_duplicating = models.FloatField(blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Type'
        verbose_name_plural = 'Inventory Types'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryMetaType(models.Model):
    """
    Relation between different variants of item (i.e. Tech-I, Faction, Tech-II). 
    These are not "meta-levels" of items used for calculate invention success. 
    For that information see Attribute metaLevel (attributeID=633) in table 
    dgmTypeAttributes linked with type in question. 
    """
    type = models.ForeignKey(EVEInventoryType, related_name='eveinventorymetatype_type_set')
    parent_type = models.ForeignKey(EVEInventoryType, related_name='eveinventorymetatype_parent_type_set')
    meta_group = models.ForeignKey(EVEInventoryMetaGroup) 
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Meta Type'
        verbose_name_plural = 'Inventory Meta Types'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryFlag(models.Model):
    """
    The invFlags table is used to identify the location and/or status of an 
    item within an office, station, ship, module or other container for the 
    API calls APIv2 Char AssetList XML and APIv2 Corp AssetList XML. 
    """
    # Short name for the flag.
    name = models.CharField(max_length=255)
    # Full, descriptive name for the flag.
    text = models.CharField(max_length=255, blank=True)
    # Very inconsistently used.
    type_text = models.CharField(max_length=255, blank=True)
    # Have no idea what this is.
    order = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Flag'
        verbose_name_plural = 'Inventory Flags'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryAttributeCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Attribute Category'
        verbose_name_plural = 'Inventory Attribute Categories'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class EVEInventoryAttributeType(models.Model):
    name = models.CharField(max_length=75)
    category = models.ForeignKey(EVEInventoryAttributeCategory, blank=True, null=True)
    description = models.TextField(blank=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    defaultvalue = models.IntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    display_name = models.CharField(max_length=100, blank=True)
    unit = models.ForeignKey(EVEUnit, blank=True, null=True)
    is_stackable = models.BooleanField(default=False)
    high_is_good = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Attribute Type'
        verbose_name_plural = 'Inventory Attribute Types'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class EVEInventoryTypeAttributes(models.Model):
    inventory_type = models.ForeignKey(EVEInventoryType)
    attribute = models.ForeignKey(EVEInventoryAttributeType)
    value_int = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Type Attribute'
        verbose_name_plural = 'Inventory Type Attributes'

    def __unicode__(self):
        return self.inventory_type.name + ' - ' + self.attribute.name

    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryBlueprintType(models.Model):
    """
    Stores info about each kind of blueprint.
    """
    blueprint_type = models.ForeignKey(EVEInventoryType,
                                       related_name='blueprint_type_set')
    product_type = models.ForeignKey(EVEInventoryType,
                                     related_name='blueprint_product_type_set')
    # This is used for T2. Not always populated.
    parent_blueprint_type = models.ForeignKey(EVEInventoryType, blank=True,
                                              null=True,
                                              related_name='parent_blueprint_type_set')
    tech_level = models.IntegerField(blank=True, null=True)
    research_productivity_time = models.IntegerField(blank=True, null=True)
    research_material_time = models.IntegerField(blank=True, null=True)
    research_copy_time = models.IntegerField(blank=True, null=True)
    research_tech_time = models.IntegerField(blank=True, null=True)
    productivity_modifier = models.IntegerField(blank=True, null=True)
    material_modifier = models.IntegerField(blank=True, null=True)
    waste_factor = models.IntegerField(blank=True, null=True)
    max_production_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Blueprint Type'
        verbose_name_plural = 'Inventory Blueprint Types'
        
    def __unicode__(self):
        return "BP: %s" % self.product_type
    
    def __str__(self):
        return self.__unicode__()
    
class EVEInventoryEffect(models.Model):
    """
    Name and descriptions of effects.
    """
    name = models.CharField(max_length=150)
    # Not sure what this is. Internal category of effect.
    category = models.IntegerField(blank=True, null=True)
    # Unknown
    pre_expression = models.IntegerField(blank=True, null=True)
    # Unknown
    post_expression = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    # Unknown
    guid = models.CharField(max_length=255, blank=True)
    graphic = models.ForeignKey(EVEGraphic, blank=True, null=True)
    # If True, applied to enemy.
    is_offensive = models.BooleanField(default=False)
    # If True, applied to ally.
    is_assistance = models.BooleanField(default=False)
    duration_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                           blank=True, null=True,
                                           related_name='eveinventoryeffectdurationeattribute')
    tracking_speed_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                                 blank=True, null=True,
                                                 related_name='eveinventoryeffecttrackingspeedattribute')
    discharge_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                            blank=True, null=True,
                                            related_name='eveinventoryeffectdischargeattribute')
    range_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                        blank=True, null=True,
                                        related_name='eveinventoryeffectrangeattribute')
    falloff_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                          blank=True, null=True,
                                          related_name='eveinventoryeffectfalloffattribute')
    disallow_auto_repeat = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    # Name of effect as displayed in game.
    display_name = models.CharField(max_length=255, blank=True)
    is_warp_safe = models.BooleanField(default=False)
    has_range_chance = models.BooleanField(default=False)
    has_electronic_chance = models.BooleanField(default=False)
    has_propulsion_chance = models.BooleanField(default=False)
    distribution = models.IntegerField(blank=True, null=True)
    sfx_name = models.CharField(max_length=100, blank=True)
    npc_usage_chance_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                                   blank=True, null=True,
                                                   related_name='eveinventoryeffectnpcusagechanceattribute')
    npc_activation_chance_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                                        blank=True, null=True,
                                                        related_name='eveinventoryeffectnpcactivationchanceattribute')
    fitting_usage_chance_attribute = models.ForeignKey(EVEInventoryAttributeType, 
                                                       blank=True, null=True,
                                                       related_name='eveinventoryeffectfittingusagechanceattribute')
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Effect'
        verbose_name_plural = 'Inventory Effects'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()

class EVEInventoryTypeEffect(models.Model):
    """
    Effects related to items. Effects are like boolean flags - if an item has
    an effect listed, it's subject to this effect with the specified
    parameters, listed as per the EveInventoryEffect.
    
    dgmTypeEffects
    """
    type = models.ForeignKey(EVEInventoryType)
    effect = models.ForeignKey(EVEInventoryEffect)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Type Effect'
        verbose_name_plural = 'Inventory Type Effect'
        
    def __unicode__(self):
        return self.type
    
    def __str__(self):
        return self.__unicode__()
    
class EVEPOSResourcePurpose(models.Model):
    """
    Types of tasks for which POS need resources, i.e. Online, Reinforced. 
    
    invControlTowerResourcePurposes
    """
    purpose = models.CharField(max_length=75, blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory POS Resource Purpose'
        verbose_name_plural = 'Inventory POS Resource Purposes'
        
    def __unicode__(self):
        return self.purpose
    
    def __str__(self):
        return self.__unicode__()

"""
class EVEPOSResource(models.Model):
    Fuel needed to support POSes. 
    
    invControlTowerResources

    control_tower_type = models.ForeignKey(EVEInventoryType)
    resource_type = models.ForeignKey(EVEInventoryType, blank=True, null=True)
    purpose = models.ForeignKey(EVEPosResourcePurpose, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    min_security_level = models.IntegerField(blank=True, null=True)
    faction = models.ForeignKey(EVEFaction, blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'POS Resource'
        verbose_name_plural = 'POS Resources'
        
    def __unicode__(self):
        return self.resource_type
    
    def __str__(self):
        return self.__unicode__()
"""
    
class EVEInventoryTypeReactions(models.Model):
    """
    Reaction recipes for POSes.
    
    invTypeReactions
    """
    INPUT_TYPES = ((0, 'Result of reaction'), 
                   (1, 'Reaction material'))
    
    reaction_type = models.ForeignKey(EVEInventoryType,
                    related_name='eveinventorytypereactions_reaction_type_set')
    input = models.IntegerField(choices=INPUT_TYPES, blank=True, null=True)
    type = models.ForeignKey(EVEInventoryType,
                    related_name='eveinventorytypereactions_type_set', 
                    help_text="Reaction result or material.")
    quantity = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Type Reaction'
        verbose_name_plural = 'Inventory Type Reactions'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()

class EVEResearchMfgActivities(models.Model):
    """
    Research and Manufacturing activities.
    """
    name = models.CharField(max_length=75, blank=True)
    description = models.CharField(max_length=100, blank=True)
    # Name of the file, should be two numbers separated by underscore, no extension.
    icon_filename = models.CharField(max_length=50, blank=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Research and Mfg activity'
        verbose_name_plural = 'Research and Mfg activities'
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.__unicode__()
    
class EVETypeActivityMaterials(models.Model):
    """
    Stores materials and skills required for Blueprints and Artifacts
    """
    blueprint_type = models.ForeignKey(EVEInventoryType, blank=False,
                                       null=False,
                                       related_name='blueprint_materials_set')
    activity = models.ForeignKey(EVEResearchMfgActivities, blank=False,
                                 null=False,
                                 related_name='activity_materials_set')
    required_type = models.ForeignKey(EVEInventoryType, blank=False,
                                      null=False,
                                      related_name='required_materials_set')
    quantity = models.IntegerField(blank=True, null=True)
    damage_per_job = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Activity Material'
        verbose_name_plural = 'Activity Materials'

    def __unicode__(self):
        return self.blueprint_type.name

    def __str__(self):
        return self.__unicode__()

class EVEPlayerCharacter(models.Model):
    """
    Represents an individual player character within the game. Not to be
    confused with an account.
    """
    name = models.CharField(max_length=255, blank=True, null=False)
    corporation = models.ForeignKey('EVEPlayerCorporation', blank=True, null=True)
    # TODO: Choices field
    race = models.IntegerField(blank=True, null=True)
    # TODO: Choices field
    gender = models.IntegerField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    attrib_intelligence = models.IntegerField(blank=True, null=True)
    attrib_memory = models.IntegerField(blank=True, null=True)
    attrib_charisma = models.IntegerField(blank=True, null=True)
    attrib_perception = models.IntegerField(blank=True, null=True)
    attrib_willpower = models.IntegerField(blank=True, null=True)
    
    objects = EVEPlayerCharacterManager()
    
    class Meta:
        verbose_name = 'Member Corporation'
        verbose_name_plural = 'Member Corporations'

class EVEPlayerAlliance(models.Model):
    """
    Represents a player-controlled alliance. Updated from the alliance
    EVE XML API puller at intervals.
    """
    name = models.CharField(max_length=255, blank=True, null=False)
    ticker = models.CharField(max_length=15, blank=True, null=False)
    #executor_character = models.ForeignKey(EVECharacter, blank=True, null=False)
    member_count = models.IntegerField(blank=True, null=True)
    date_founded = models.DateField(blank=True, null=True)
    
    objects = EVEPlayerAllianceManager()
    
    class Meta:
        ordering = ['date_founded']
        verbose_name = 'Player Alliance'
        verbose_name_plural = 'Player Alliances'
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return "Alliance #%d" % self.id
        
    def __str__(self):
        return self.__unicode__()

class EVEPlayerCorporation(models.Model):
    """
    Represents a player-controlled corporation. Updated from a mixture of
    the alliance and corporation API pullers.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    ticker = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    ceo_character = models.ForeignKey(EVEPlayerCharacter, blank=True, null=True)
    #home_station = models.ForeignKey(EVEStation, blank=True, null=False)
    alliance = models.ForeignKey(EVEPlayerAlliance, blank=True, null=True)
    alliance_join_date = models.DateField(blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    member_count = models.IntegerField(blank=True, null=True)
    shares = models.IntegerField(blank=True, null=True)
    
    # Logo generation stuff
    logo_graphic_id = models.IntegerField(blank=True, null=True)
    logo_shape1 = models.IntegerField(blank=True, null=True)
    logo_shape2 = models.IntegerField(blank=True, null=True)
    logo_shape3 = models.IntegerField(blank=True, null=True)
    logo_color1 = models.IntegerField(blank=True, null=True)
    logo_color2 = models.IntegerField(blank=True, null=True)
    logo_color3 = models.IntegerField(blank=True, null=True)
    
    objects = EVEPlayerCorporationManager()
    
    class Meta:
        verbose_name = 'Player Corporation'
        verbose_name_plural = 'Player Corporations'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Corp #%d" % self.id
        
    def query_and_update_corp(self):
        """
        Takes an EVEPlayerCorporation object and updates it from the 
        EVE API service.
        """
        # Pull XML from the EVE API via eve_proxy.
        dom = EVEPlayerCorporation.objects.api_corp_sheet_xml(self.id)
        
        # Tuples of pairings of tag names and the attribute on the Corporation
        # object to set the data to.
        tag_mappings = (
            ('corporationName', 'name'),
            ('ticker', 'ticker'),
            ('url', 'url'),
            ('description', 'description'),
            ('memberCount', 'member_count'),
            ('graphicID', 'logo_graphic_id'),
            ('shape1', 'logo_shape1'),
            ('shape2', 'logo_shape2'),
            ('shape3', 'logo_shape3'),
            ('color1', 'logo_color1'),
            ('color2', 'logo_color2'),
            ('color3', 'logo_color3'),
        )
        
        # Iterate through the tag mappings, setting the values of the tag names
        # (first member of the tuple) to the attribute named in the second member
        # of the tuple on the EVEPlayerCorporation object.
        for tag_map in tag_mappings:
            try:
                setattr(self, tag_map[1], 
                        dom.getElementsByTagName(tag_map[0])[0].firstChild.nodeValue)
            except AttributeError:
                # This tag has no value, skip it.
                continue
            except IndexError:
                # Something weird has happened
                print " * Index Error:", tag_map[0]
                continue

        print "Updating", self.id, self.name
        self.save()
