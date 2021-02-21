# Copyright 2015 Oihane Crucelaegui - AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2016 ACSONE SA/NV
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import _, api, exceptions, models
from odoo.tools import config


class ProductProduct(models.Model):
    _inherit = ["product.product", "product.configurator"]
    _name = "product.product"

    def _get_product_attributes_values_dict(self):
        # Retrieve first the attributes from template to preserve order
        res = self.product_tmpl_id._get_product_attributes_dict()
        for val in res:
            value = self.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.id == val["attribute_id"]
            )
            val["value_id"] = value.product_attribute_value_id.id
        return res

    def _get_product_attributes_values_text(self):
        description = self.product_template_attribute_value_ids.mapped(
            lambda x: "{}: {}".format(x.attribute_id.name, x.name)
        )
        if description:
            return "{}\n{}".format(self.product_tmpl_id.name, "\n".join(description))
        else:
            return self.product_tmpl_id.name

    @api.model
    def _build_attributes_domain(self, product_template, product_attributes):
        domain = []
        cont = 0
        if product_template:
            domain.append(("product_tmpl_id", "=", product_template.id))
            for attr_line in product_attributes:
                if isinstance(attr_line, dict):
                    value_id = attr_line.get("value_id")
                else:
                    value_id = attr_line.value_id.id
                if value_id:
                    ptav = self.env["product.template.attribute.value"].search(
                        [
                            ("product_tmpl_id", "=", product_template.id),
                            (
                                "attribute_id",
                                "in",
                                [x.attribute_id.id for x in product_attributes],
                            ),
                            ("product_attribute_value_id", "=", value_id),
                        ]
                    )
                    if ptav:
                        domain.append(
                            ("product_template_attribute_value_ids", "=", ptav.id)
                        )
                        cont += 1
        return domain, cont

    @api.model
    def _product_find(self, product_template, product_attributes):
        if product_template:
            domain, cont = self._build_attributes_domain(
                product_template, product_attributes
            )
            products = self.search(domain)
            # Filter the product with the exact number of attributes values
            for product in products:
                if len(product.product_template_attribute_value_ids) == cont:
                    return product
        return False

    @api.constrains("product_tmpl_id", "product_template_attribute_value_ids")
    def _check_duplicity(self):
        if not config["test_enable"] or not self.env.context.get(
            "test_check_duplicity"
        ):
            return
        for product in self:
            domain = [("product_tmpl_id", "=", product.product_tmpl_id.id)]
            for value in product.product_template_attribute_value_ids:
                domain.append(("product_template_attribute_value_ids", "=", value.id))
            other_products = self.with_context(active_test=False).search(domain)
            # Filter the product with the exact number of attributes values
            cont = len(product.product_template_attribute_value_ids)
            for other_product in other_products:
                if (
                    len(other_product.product_template_attribute_value_ids) == cont
                    and other_product != product
                ):
                    raise exceptions.ValidationError(
                        _("There's another product with the same attributes.")
                    )

    @api.constrains("product_tmpl_id", "product_template_attribute_value_ids")
    def _check_configuration_validity(self):
        """The method checks that the current selection values are correct.

        As default, the validity means that all the attributes
        with the required flag are set.

        This can be overridden to set another rules.

        :raises: exceptions.ValidationError: If the check is not valid.
        """
        # Creating from template variants attributes are not created at once so
        # we avoid to check the constrain here.
        if self.env.context.get("creating_variants"):
            return
        for product in self:
            req_attrs = product.product_tmpl_id.attribute_line_ids.filtered(
                lambda a: a.required
            ).mapped("attribute_id")
            errors = req_attrs - product.product_template_attribute_value_ids.mapped(
                "attribute_id"
            )
            if errors:
                raise exceptions.ValidationError(
                    _("You have to fill the following attributes:\n%s")
                    % "\n".join(errors.mapped("name"))
                )

    def name_get(self):
        """We need to add this for avoiding an odoo.exceptions.AccessError due
        to some refactoring done upstream on read method + variant name_get
        in Odoo. With this, we avoid to call super on the specific case of
        virtual records, providing simply the name, which is acceptable.
        """
        res = []
        for product in self:
            if isinstance(product.id, models.NewId):
                res.append((product.id, product.name))
            else:
                res.append(super(ProductProduct, product).name_get()[0])
        return res

    @api.model
    def create(self, vals):
        print(vals)
        product_attribute_obj = self.env["product.attribute"]
        product_attribute_value_obj = self.env["product.attribute.value"]
        product_obj = self.env["product.product"]
        product_brand_obj = self.env["product.brand"]
        product_model_obj = self.env["product.model"]
        product_size_obj = self.env["product.size"]
        product_attachments_obj = self.env["product.attachments"]
        product_status_obj = self.env["product.status"]
        product_gender_obj = self.env["product.gender"]
        manufacturing_year = ''
        product_brand_id = ''
        product_model_id = ''
        product_size_id = ''
        product_gender_id = ''
        product_attachments_id = ''
        product_status_id = ''

        if vals.get("product_attribute_ids"):
            ptav = (
                self.env["product.template.attribute.value"]
                .search(
                    [
                        (
                            "product_tmpl_id",
                            "in",
                            [
                                x[2]["product_tmpl_id"]
                                for x in vals["product_attribute_ids"]
                            ],
                        ),
                        (
                            "attribute_id",
                            "in",
                            [
                                x[2]["attribute_id"]
                                for x in vals["product_attribute_ids"]
                            ],
                        ),
                        (
                            "product_attribute_value_id",
                            "in",
                            [
                                x[2]["value_id"]
                                for x in vals["product_attribute_ids"]
                                if x[2]["value_id"]
                            ],
                        ),
                    ]
                )
                .ids
            )
            for x in vals["product_attribute_ids"]:
                product_attribute_b = product_attribute_obj.browse(x[2]["attribute_id"])
                product_attribute_value_b = product_attribute_value_obj.browse(x[2]["value_id"])
                if product_attribute_b.name == "Manufacturing Year":
                    manufacturing_year = product_attribute_value_b.name
                if product_attribute_b.name == "Brand":
                    product_brand = product_brand_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_brand:
                        product_brand = product_brand_obj.create({"name": product_attribute_value_b.name})
                    product_brand_id = product_brand.id
                if product_attribute_b.name == "Model":
                    product_model = product_model_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_model:
                        product_model = product_model_obj.create({"name": product_attribute_value_b.name})
                    product_model_id = product_model.id
                if product_attribute_b.name == "Size":
                    product_size = product_size_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_size:
                        product_size = product_size_obj.create({"name": product_attribute_value_b.name})
                    product_size_id = product_size.id
                if product_attribute_b.name == "Gender":
                    product_gender = product_gender_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_gender:
                        product_gender = product_gender_obj.create({"name": product_attribute_value_b.name})
                    product_gender_id = product_gender.id
                if product_attribute_b.name == "Attachments":
                    product_attachments = product_attachments_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_attachments:
                        product_attachments = product_attachments_obj.create({"name": product_attribute_value_b.name})
                    product_attachments_id = product_attachments.id
                if product_attribute_b.name == "Status":
                    product_status = product_status_obj.search([['name', '=', product_attribute_value_b.name]])
                    if not product_status:
                        product_status = product_status_obj.create({"name": product_attribute_value_b.name})
                    product_status_id = product_status.id
                # print(manufacturing_year)
            vals.pop("product_attribute_ids")
            vals["product_template_attribute_value_ids"] = [(4, x) for x in ptav]
            vals["manufacturing_year"] = manufacturing_year
            vals["product_brand"] = product_brand_id
            vals["model_number"] = product_model_id
            vals["product_size"] = product_size_id
            vals["gender"] = product_gender_id
            vals["attachments"] = product_attachments_id
            vals["status"] = product_status_id


        obj = self.with_context(product_name=vals.get("name", ""))
        return super(ProductProduct, obj).create(vals)
