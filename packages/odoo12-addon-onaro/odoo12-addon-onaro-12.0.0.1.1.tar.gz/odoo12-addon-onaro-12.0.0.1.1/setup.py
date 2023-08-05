import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'depends_override': {
            'auth_api_key': 'odoo12-addon-auth-api-key==12.0.2.1.0.99.dev2',
            'base_rest': 'odoo12-addon-base-rest==12.0.3.0.6',
            'crm_lead_product': 'odoo12-addon-crm-lead-product==12.0.1.0.0.99.dev12',
            'telecom': 'odoo12-addon-telecom==12.0.0.1.0',
            'partner_firstname': 'odoo12-addon-partner-firstname==12.0.1.1.0.99.dev2',
            'remove_dup_acc_num_constraint': 'odoo12-addon-remove-dup-acc-num-constraint==12.0.1.0.1',
        },
        'external_dependencies_override': {
            'python': {
                'pycastiphone_client': 'pycastiphone-client==0.1.0',
            },
        },
    },
)
