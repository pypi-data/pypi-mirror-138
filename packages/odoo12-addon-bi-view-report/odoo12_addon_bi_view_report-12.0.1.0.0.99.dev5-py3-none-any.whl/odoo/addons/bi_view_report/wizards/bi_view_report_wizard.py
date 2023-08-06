from odoo import models, fields, api
import base64
from odoo.addons.web.controllers.main import ExcelExport
from xml.dom.minidom import parseString


class BiViewReportWizard(models.TransientModel):
    _name = 'bi.view.report.wizard'
    partner_id = fields.Many2one('res.partner')
    name = fields.Char()
    bve_view_name = fields.Char()
    nextcall = fields.Datetime(string='Next Execution Date', required=True,
                               default=fields.Datetime.now,
                               help="Next planned execution date for this job.")

    interval_number = fields.Integer(default=1, help="Repeat every x.")
    interval_type = fields.Selection(
        [('minutes', 'Minutes'),
         ('hours', 'Hours'),
         ('days', 'Days'),
         ('weeks', 'Weeks'),
         ('months', 'Months')], string='Interval Unit', default='months')
    filter_id = fields.Many2one('ir.filters')

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self.env.context['active_id']
        act_window = self.env['report.async'].browse(active_id).action_id
        defaults['bve_view_name'] = act_window.res_model
        return defaults

    @api.model
    def send_email(self, name, partner_id, bve_view_name, domain):
        email_template = self.env.ref('bi_view_report.email_template')
        file_name = name+".xls"
        model = self.env[bve_view_name]
        fields_get = model.fields_get()
        arch_db = self.env['ir.ui.view'].search(
            [('model', '=', bve_view_name), ('type', '=', 'tree')]
        ).arch_db
        field_names = [
            e.getAttribute('name')
            for e in parseString(arch_db).getElementsByTagName("field")
        ]
        names = [fields_get[f]['string'] for f in field_names]
        domain = domain or []
        export_data = model.search(domain).export_data(field_names, False)
        bin_excel = ExcelExport().from_data(names, export_data['datas'])
        datas = base64.encodebytes(bin_excel)
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'datas': datas,
            'datas_fname': file_name
        })
        id = attachment.id
        email_template.attachment_ids = [(6, 0, [id])]
        email_template.with_context(name=name).send_mail(partner_id, raise_exception=False, force_send=True)

    @api.multi
    def create_cron_job(self):
        code = "model.send_email('{name}',{partner_id},'{bve_view_name}', {domain})".format(
            name=self.name, partner_id=self.partner_id.id,
            bve_view_name=self.bve_view_name, domain=self.filter_id.domain
        )
        self.env['ir.cron'].create({
            'model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
            'user_id': self.sudo().env.user.id,
            'name': self.name,
            'nextcall': self.nextcall,
            'numbercall': -1,
            'code': code
        })
