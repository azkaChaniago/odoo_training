import time
from openerp.report import report_sxw

class print_training(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(print_training, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.laporan.course',
                        'member.course',
                        '~/.local/share/Odoo/addons/10.0/exp_default/report/print_course.rml',
                        parser=print_training,
                        header=False)