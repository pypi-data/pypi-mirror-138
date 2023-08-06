import json
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.addons.community_maps.models.cm_utils import CmUtils

class CmPlace(models.Model):
  _name = 'crm.team'

  _inherit = ["crm.team","cm.slug.id.mixin"]

  _labeled_meta_formats = ['uri','progress']

  lat = fields.Float(string=_("Latitude"))
  lng = fields.Float(string=_("Longitude"))
  status = fields.Selection(selection=[
    ('draft', 'Draft'), 
    ('published', 'Published')
    ], default='draft', required=True, string=_("Status"))
  map_id = fields.Many2one('cm.map',string=_("Related map"))
  form_model_id = fields.Many2one('cm.form.model',string=_("Form"))
  place_category_id = fields.Many2one('cm.place.category',string=_("Category"))
  presenter_model_id = fields.Many2one('cm.presenter.model',string=_("Presenter"))
  place_presenter_metadata_ids = fields.One2many(
    'cm.place.presenter.metadata',
    'place_id',
    string=_("Presenter metadata"))
  team_type = fields.Selection(
    selection_add=[('map', _("Map"))])
  crowdfunding_type = fields.Selection(
    selection=CmUtils.get_system_crowdfunding_types_selection(),
    string=_("Crowdfunding type"),
    compute="_get_crowdfunding_type",
    store=False)
  form_submission_ids = fields.One2many(
    'crm.lead',
    'team_id',
    string=_("Submissions"))
  completed_percentage = fields.Integer(
    string=_("% Completed"),
    compute="_get_completed_percentage",
    store=False)
  submissions_target = fields.Integer(string=_("Submission target"))
  has_active_service = fields.Boolean(string=_("Place with active service"))
  address_txt = fields.Char(string=_("Address text"))

  # system
  @api.constrains('team_type')
  def _setup_crm_defaults_for_map_team_type(self):
    for record in self:
      if record.team_type == 'map':
        record.use_opportunities = True
        record.use_quotations = True
        record.use_leads = True
        record.dashboard_graph_model = 'crm.lead'
        # TODO: This preset doesn't get stablished
        record.dashboard_graph_period_pipeline = 'month'
        record.dashboard_graph_group_pipeline = 'stage'
        if record.crowdfunding_type == 'invoicing_amount':
          record.use_invoices = True

  @api.constrains('form_submission_ids')
  def recompute_probability(self):
    print('CONSTRAIN IN PLACE')

  @api.depends('map_id')
  def _get_crowdfunding_type(self):
    for record in self:
      if record.map_id:
        record.crowdfunding_type = record.map_id.crowdfunding_type

  @api.depends('form_submission_ids')
  def _get_completed_percentage(self):
    for record in self:
      total = 0
      record.completed_percentage = total
      if record.form_submission_ids:
        if record.crowdfunding_type == 'invoicing_amount':
          for submission in record.form_submission_ids:
            total += submission.planned_revenue
          if record.invoiced_target:
            record.completed_percentage = int(total/record.invoiced_target*100)
        if record.crowdfunding_type == 'submission_amount':
          if record.submissions_target:
            record.completed_percentage = int(len(record.form_submission_ids)/record.submissions_target*100)

  # place config preselection
  @api.onchange('map_id')
  def _get_config_relations_attrs(self):
    self.ensure_one()
    allowed_form_model_ids = self.map_id.allowed_form_model_mids 
    allowed_place_category_ids = self.map_id.allowed_place_category_mids
    allowed_presenter_model_ids = self.map_id.allowed_presenter_model_mids 
    return_dict = {
      'domain':{
        'form_model_id': [('id', 'in',allowed_form_model_ids.mapped('id'))],
        'place_category_id': [('id', 'in',allowed_place_category_ids.mapped('id'))],
        'presenter_model_id': [('id', 'in',allowed_presenter_model_ids.mapped('id'))]
      }
    } 
    if allowed_form_model_ids:
      self.form_model_id = allowed_form_model_ids[0].id
    if allowed_place_category_ids:
      self.place_category_id = allowed_place_category_ids[0].id
    if allowed_presenter_model_ids:
      self.presenter_model_id = allowed_presenter_model_ids[0].id
    return return_dict

  # place presenter
  def _get_create_place_meta(self,key,type,format,sort_order,place_id,dataschema,uischema):
    creation_data = {
      'type' : type,
      'key' : key,
      'format' : format,
      'sort_order' : sort_order,
      'place_id': place_id
    }
    # default values
    if key in dataschema.keys():
      creation_data['value'] = dataschema[key]
    # default labels
    if ".label" in key:
      for element in uischema['elements']:
        if element['type'] == 'Links':
          for sub_element in element['elements']:
            label = self._get_schema_meta_label_from_key(sub_element,key)
            if label:
              creation_data['value'] = label
        else:
          label = self._get_schema_meta_label_from_key(element,key)
          if label:
            creation_data['value'] = label
    query = [
      ('place_id', '=', place_id),
      ('key','=',key),
      ('type','=',type),
      ('format','=',format)
    ]
    return CmUtils.get_create_existing_model(
      self.env['cm.place.presenter.metadata'],
      query,
      creation_data
    )
  
  def _get_schema_meta_label_from_key(self,element,key):
    meta_key = key.replace('.label','')
    if element['scope'] == '#/properties/'+meta_key:
      if "label" in element.keys():
        return element['label']
    return False

  @api.onchange('presenter_model_id')
  def _build_presenter_metadata_ids(self):
    self.ensure_one()
    place_presenter_metadata_ids = []
    if self.presenter_model_id:
      presenter_json_schema = json.loads(self.presenter_model_id.json_schema)
      presenter_json_dataschema = json.loads(self.presenter_model_id.json_dataschema)
      presenter_json_uischema = json.loads(self.presenter_model_id.json_uischema)
      current_meta_ids = []
      sort_order = 0
      print(presenter_json_schema)
      for meta_key in presenter_json_schema['properties'].keys():
        meta_format = ''
        if 'format' in presenter_json_schema['properties'][meta_key].keys():
          meta_format = presenter_json_schema['properties'][meta_key]['format']
        if meta_format in self._labeled_meta_formats:
          place_meta = self._get_create_place_meta(
            meta_key+'.label',
            'string',
            meta_format+'.label',
            sort_order,
            self._origin.id,
            presenter_json_dataschema,
            presenter_json_uischema
          )
          current_meta_ids.append(place_meta.id)
          place_presenter_metadata_ids.append((4,place_meta.id))
          sort_order += 1
        if meta_format != 'progress':
          place_meta = self._get_create_place_meta(
            meta_key,
            presenter_json_schema['properties'][meta_key]['type'],
            meta_format,
            sort_order,
            self._origin.id,
            presenter_json_dataschema,
            presenter_json_uischema
          )
          current_meta_ids.append(place_meta.id)
          place_presenter_metadata_ids.append((4,place_meta.id))
          sort_order += 1
      # delete metas not in presenter
      for metadata in self.place_presenter_metadata_ids:
        if metadata.id not in current_meta_ids:
          place_presenter_metadata_ids.append((2,metadata.id))
    else:
      # delete all metas
      for metadata in self.place_presenter_metadata_ids:
        place_presenter_metadata_ids.append((2,metadata.id))
    # create metas
    self.place_presenter_metadata_ids = place_presenter_metadata_ids

  def _build_presenter_schemadata_json(self):
    presenter_schemadata_dict = {}
    presenter_json_schema = json.loads(self.presenter_model_id.json_schema)
    for meta_key in presenter_json_schema['properties'].keys():
      place_meta = self.place_presenter_metadata_ids.filtered(lambda r: r.key == meta_key)
      if place_meta.exists():
        if place_meta[0].value:
          presenter_schemadata_dict[meta_key] = place_meta[0].value
        else:
          presenter_schemadata_dict[meta_key] = None
    return presenter_schemadata_dict

  def _build_presenter_schema_json(self):
    return json.loads(self.presenter_model_id.json_schema)
  
  def _build_presenter_uischema_json(self):
    presenter_json_schema = json.loads(self.presenter_model_id.json_schema)
    presenter_json_uischema = json.loads(self.presenter_model_id.json_uischema)
    for element in presenter_json_uischema['elements']:
      if element['type'] == 'Links':
        for sub_element in element['elements']:
          meta_label = self._get_meta_label_from_scope(presenter_json_schema,sub_element['scope'])
          if meta_label:
            sub_element['label'] = meta_label
      else:
        meta_label = self._get_meta_label_from_scope(presenter_json_schema,element['scope'])
        if meta_label:
          element['label'] = meta_label
        
    return presenter_json_uischema

  def _get_meta_label_from_scope(self,json_schema,scope):
    meta_key = scope.replace('#/properties/','')
    meta_format = json_schema['properties'][meta_key]['format']
    if meta_format in self._labeled_meta_formats:
      place_meta = self.place_presenter_metadata_ids.filtered(lambda r: r.key == meta_key+'.label')
      if place_meta.exists():
        return place_meta[0].value
    return False

  # api datamodel
  def get_datamodel_dict(self,single_view=False):
    place_dict = {
      'name': self.name,
      'slug': self.slug_id,
      'map_slug': self.map_id.slug_id,
      'category_slug': self.place_category_id.slug_id,
      'form_slug': None,
      'lat': self.lat,
      'lng': self.lng,
      'address': None,
    }
    if self.address_txt:
      place_dict['address'] = self.address_txt
    # TODO: need to discuss how to pass this in config.
    place_dict['active'] = self.has_active_service
    if self.crowdfunding_type != 'none':
      place_dict['goalProgress'] = self.completed_percentage
    if single_view:
      place_dict['schemaData'] = self._build_presenter_schemadata_json()
      place_dict['jsonSchema'] = self._build_presenter_schema_json()
      place_dict['uiSchema'] = self._build_presenter_uischema_json()
    if self.form_model_id:
      place_dict['form_slug'] = self.form_model_id.slug_id
    return place_dict

