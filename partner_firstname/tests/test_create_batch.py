# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestCreateBatch(TransactionCase):
    def _create(self, vals_list, **context):
        return self.env["res.partner"].with_context(**context).create(vals_list)

    def test_partners_created_together(self):
        partners = self._create(
            [
                {
                    "firstname": "Quilmar",
                    "lastname": "Zendro",
                    "name": "Quilmar Zendro",
                },
                {"name": "Varek Onsby"},
                {"lastname": "Tolvane"},
                {"name": "Brixel Test Company", "is_company": True},
            ]
        )
        self.assertEqual(
            partners.mapped("name"),
            ["Quilmar Zendro", "Varek Onsby", "Tolvane", "Brixel Test Company"],
        )
        self.assertEqual(
            partners.mapped("firstname"), ["Quilmar", "Varek", False, False]
        )
        self.assertEqual(
            partners.mapped("lastname"),
            ["Zendro", "Onsby", "Tolvane", "Brixel Test Company"],
        )

    def test_default_name_dropped_for_all_partners(self):
        partners = self._create(
            [
                {
                    "firstname": "Quilmar",
                    "lastname": "Zendro",
                    "name": "Quilmar Zendro",
                },
                {"name": "Varek Onsby"},
                {"lastname": "Tolvane"},
            ],
            default_name="Default Name",
        )
        # without a name, the first name comes from the default name
        self.assertEqual(
            partners.mapped("name"),
            ["Quilmar Zendro", "Varek Onsby", "Default Tolvane"],
        )

    def test_default_name_kept_for_some_partners(self):
        company = self.env["res.partner"].create(
            {"name": "Brixel Test Company", "is_company": True}
        )
        partners = self._create(
            [
                {
                    "firstname": "Quilmar",
                    "lastname": "Zendro",
                    "name": "Quilmar Zendro",
                },
                # no name to split, so this address keeps the default name
                {"name": None, "type": "invoice", "parent_id": company.id},
                {"lastname": "Tolvane"},
            ],
            default_name="Default Name",
        )
        self.assertEqual(partners.mapped("type"), ["contact", "invoice", "contact"])
        self.assertEqual(
            [partner.name for partner in partners],
            ["Quilmar Zendro", False, "Default Tolvane"],
        )
