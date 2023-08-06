from erp_sync.Resources.resource import Resource


class Payments(Resource):

    urls = {}

    def set_client_id(self, client_id):
        super().set_client_id(client_id)
        self._set_urls()
        return self

    def set_company_id(self, company_id):
        super().set_company_id(company_id)
        self._set_urls()
        return self

    def _set_urls(self):

        self.urls = {
            "new": f"/companies/{super().get_company_id()}/payments",
            "edit": f"/companies/{super().get_company_id()}/payments",
            "delete": f"/companies/{super().get_company_id()}/payments",
            "read": f"/companies/{super().get_company_id()}/payments",
            "import": f"/companies/{super().get_company_id()}/import_payments"
        }

        super().set_urls(self.urls)

        return self

    def read(self, payment_id=None, payload=None, method='GET', endpoint=None):

        self._set_urls()

        if payment_id is not None:
            self.urls["read"] = f'{self.urls["read"]}/{payment_id}'
            super().set_urls(self.urls)

        return super().read(payload, method, endpoint)

    def edit(self, ledger_id=None, payload=None, method='PUT', endpoint=None):

        self._set_urls()

        self.urls["edit"] = f'{self.urls["edit"]}/{ledger_id}'

        super().set_urls(self.urls)

        return super().edit(payload, method, endpoint)

    def delete(self, ledger_id=None, payload=None, method='DELETE', endpoint=None):

        payload = {"type": "SalesPayment"}

        self._set_urls()

        self.urls["delete"] = f'{self.urls["delete"]}/{ledger_id}'

        super().set_urls(self.urls)

        return super().delete(payload, method, endpoint)

    def import_data(self, ledger_id=None, payload=None, method='GET', endpoint=None):

        self._set_urls()

        if ledger_id is not None:
            self.urls["import"] = f'{self.urls["import"]}/{ledger_id}'
            super().set_urls(self.urls)

        return super().import_data(payload, method, endpoint)

    def payload(self):

        data = {
            "amount": "<Enter amount>",
            "customer_id": "<Enter customer id>",
            "reference": "<Enter unique reference>",
            "description": "<Enter description>",
            "date": "<Enter date (yyyy-mm-dd) e.g. 2021-11-22>"
        }

        # If client type is ZOHO
        if super().get_client_type() == super().XERO:
            data["customer_id"] = "<Chart of Account ID>"
            data["invoice_id"] = "<Enter invoice id>"

        return data

    def serialize(self, payload=None, operation=None):

        data = {}

        if operation is None:
            return "Specify the operation: Resource.READ, Resource.NEW or Resource.UPDATE"

        if operation == super().NEW or operation == super().UPDATE:

            additional_properties = payload.get("additional_properties", {})

            # If client type is Quickbooks Online
            if super().get_client_type() == super().QBO:

                data = {"type": "SalesPayment"}

                if 'type' in additional_properties.keys():
                    data.update({
                        "type": additional_properties.get("type", "SalesPayment")
                    })

                    additional_properties.pop("type")

                if 'amount' in payload.keys():
                    data.update({
                        "TotalAmt": payload.get("amount", "")
                    })

                if 'customer_id' in payload.keys():
                    data.update({
                        "CustomerRef": {
                            "value": payload.get("customer_id", "")
                        }
                    })

                if 'reference' in payload.keys():
                    data.update({
                        "PaymentRefNum": payload.get("reference", "")
                    })

            # If client type is ZOHO
            elif super().get_client_type() == super().ZOHO:

                data = {"type": "SalesPayment"}

                if 'type' in additional_properties.keys():
                    data.update({
                        "type": additional_properties.get("type", "SalesPayment")
                    })

                    additional_properties.pop("type")

                payment = {}

                if 'customer_id' in payload.keys():
                    payment.update({
                        "customer_id": payload.get("customer_id", "")
                    })

                if 'amount' in payload.keys():
                    payment.update({
                        "amount": payload.get("amount", "")
                    })

                if 'reference' in payload.keys():
                    payment.update({
                        "reference": payload.get("reference", "")
                    })

                if 'description' in payload.keys():
                    payment.update({
                        "description": payload.get("description", "")
                    })

                if 'date' in payload.keys():
                    payment.update({
                        "date": payload.get("date", "")
                    })

                if bool(payment):
                    data.update({
                        "payment": payment
                    })

            # If client type is ZOHO
            elif super().get_client_type() == super().XERO:

                data = {}

                payment = {}

                if 'date' in payload.keys():
                    payment.update({
                        "Date": payload.get("date", "")
                    })

                if 'amount' in payload.keys():
                    payment.update({
                        "Amount": payload.get("amount", "")
                    })

                if 'reference' in payload.keys():
                    payment.update({
                        "Reference": payload.get("reference", "")
                    })

                if 'customer_id' in payload.keys():
                    payment.update({
                        "Account": {
                            "AccountID": payload.get("customer_id", "")
                        }
                    })

                if 'invoice' in additional_properties.keys():
                    payment.update({
                        "Invoice": additional_properties.get("invoice", {})
                    })
                    
                    additional_properties.pop("invoice")

                if bool(payment):
                    data.update({
                        "Payments": [payment]
                    })

            data.update(additional_properties)

            return data

        elif operation == super().READ:

            payload = super().response()

            if 'data' in payload.keys():
                payload = payload.get("data", [])

            elif 'resource' in payload.keys():
                payload = payload.get("resource", [])

            # confirms if a single object was read from the database
            if isinstance(payload, dict):
                payload = [payload]

            if payload is not None:
                
                if len(payload) > 0:
                    for i in range(len(payload)):
                        if 'chart_of_account_id' in payload[i].keys():
                            payload[i]['customer_id'] = payload[i].pop(
                                'chart_of_account_id')
                        if 'reference_number' in payload[i].keys():
                            payload[i]['reference'] = payload[i].pop(
                                'reference_number')
                        if 'total_amount' in payload[i].keys():
                            payload[i]['amount'] = payload[i].pop('total_amount')
                
            else:
                payload = super().response()

            super().set_response(payload)

            return self
