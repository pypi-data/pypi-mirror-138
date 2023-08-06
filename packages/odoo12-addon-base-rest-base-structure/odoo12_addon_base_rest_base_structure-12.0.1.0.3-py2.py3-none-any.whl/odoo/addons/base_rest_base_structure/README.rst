========================
Base Rest Base Structure
========================

This addon aims to provide a basic service and controller structure to simplify a rest custom implemenation in other odoo modules.

Usage
=====

On our custom module. When we need to expose an specific model we'll create a service extending from the base ones.

.. code-block:: python

    from odoo.addons.component.core import Component
    from odoo.addons.base_rest_base_structure.models.api_services_utils import APIServicesUtils

    class CustomModelService(Component):
        _inherit = "base.rest.private_abstract_service"
        _name = "custom_module.custom_model.services"
        _usage = "custom-endpoint"
        _description = """
            Custom Model Service
        """

    def get(self, _id):
        record = self.env["custom_module.custom_model"].search(
            [("id", "=", _id)]
        )
        if record:
            record.ensure_one()
            utils = APIServicesUtils.get_instance()
            # Define here all fields to be passed to the response
            attributes = ["name"]
            # Define here all many2one fields to be passed to the response
            rel_attributes = {
              "rel_model_id" : "name"
            }
            return utils.generate_get_dictionary(record,attributes,rel_attributes)
        else:
          raise wrapJsonException(
            NotFound(_("No reward record for id %s") % _id)
          )

    def create(self, **params):
        utils = APIServicesUtils.get_instance()
        # define all fields that the API receive
        attributes = ["name"]
        create_dict = utils.generate_create_dictionary(params,attributes)
        record = self.env["custom_module.custom_model"].create(create_dict)
        return {"_id": record.id}

    # rest of methods defined below

Changelog
=========

12.0.1.0.0
~~~~~~~~~~

First official version.

Bug Tracker
===========

Bugs are tracked on `GitLab Issues <https://gitlab.com/coopdevs/odoo-addons/-/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Based on the initial work of Robin Keunen <robin@coopiteasy.be> for easy_my_coop_api module and on base_rest_demo from OCA rest-api.
Trying to decople this functionallity from easy_my_coop vertical-cooperative infraestructure.

Authors
~~~~~~~

* Coodpevs Treball SCCL
* Coop It Easy

Contributors
~~~~~~~~~~~~

* Dani Quilez <dani.quilez@coopdevs.org>

Maintainers
~~~~~~~~~~~

This module is maintained by Coopdevs Treball SCCL.
