# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from copy import deepcopy
from typing import TYPE_CHECKING

from azure.core import PipelineClient
from msrest import Deserializer, Serializer

from . import models
from ._configuration import IgnosPortalConfiguration
from .operations import AppsOperations, AssetsOperations, AzureRegionsOperations, CdfClustersOperations, CdfOperations, CountriesOperations, CustomerOrdersOperations, CustomersOperations, DatabasesOperations, ElectricalOperations, ExternalAccessOperations, ExternalOperations, MachineAlarmsOperations, MachineUtilizationOperations, MeOperations, MeasurementFormSchemasOperations, MeasurementFormsInstancesOperations, MeasuringToolsOperations, PowerOperations, SuppliersOperations, SustainabilityOperations, UploadOperations, UserOperations, WeldingOperations, WorkordersOperations

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Optional

    from azure.core.credentials import TokenCredential
    from azure.core.rest import HttpRequest, HttpResponse

class IgnosPortal(object):
    """IgnosPortal.

    :ivar apps: AppsOperations operations
    :vartype apps: ignos.api.client.operations.AppsOperations
    :ivar assets: AssetsOperations operations
    :vartype assets: ignos.api.client.operations.AssetsOperations
    :ivar azure_regions: AzureRegionsOperations operations
    :vartype azure_regions: ignos.api.client.operations.AzureRegionsOperations
    :ivar cdf: CdfOperations operations
    :vartype cdf: ignos.api.client.operations.CdfOperations
    :ivar cdf_clusters: CdfClustersOperations operations
    :vartype cdf_clusters: ignos.api.client.operations.CdfClustersOperations
    :ivar countries: CountriesOperations operations
    :vartype countries: ignos.api.client.operations.CountriesOperations
    :ivar customers: CustomersOperations operations
    :vartype customers: ignos.api.client.operations.CustomersOperations
    :ivar databases: DatabasesOperations operations
    :vartype databases: ignos.api.client.operations.DatabasesOperations
    :ivar customer_orders: CustomerOrdersOperations operations
    :vartype customer_orders: ignos.api.client.operations.CustomerOrdersOperations
    :ivar workorders: WorkordersOperations operations
    :vartype workorders: ignos.api.client.operations.WorkordersOperations
    :ivar external: ExternalOperations operations
    :vartype external: ignos.api.client.operations.ExternalOperations
    :ivar external_access: ExternalAccessOperations operations
    :vartype external_access: ignos.api.client.operations.ExternalAccessOperations
    :ivar electrical: ElectricalOperations operations
    :vartype electrical: ignos.api.client.operations.ElectricalOperations
    :ivar welding: WeldingOperations operations
    :vartype welding: ignos.api.client.operations.WeldingOperations
    :ivar machine_alarms: MachineAlarmsOperations operations
    :vartype machine_alarms: ignos.api.client.operations.MachineAlarmsOperations
    :ivar machine_utilization: MachineUtilizationOperations operations
    :vartype machine_utilization: ignos.api.client.operations.MachineUtilizationOperations
    :ivar me: MeOperations operations
    :vartype me: ignos.api.client.operations.MeOperations
    :ivar measurement_form_schemas: MeasurementFormSchemasOperations operations
    :vartype measurement_form_schemas: ignos.api.client.operations.MeasurementFormSchemasOperations
    :ivar measurement_forms_instances: MeasurementFormsInstancesOperations operations
    :vartype measurement_forms_instances:
     ignos.api.client.operations.MeasurementFormsInstancesOperations
    :ivar measuring_tools: MeasuringToolsOperations operations
    :vartype measuring_tools: ignos.api.client.operations.MeasuringToolsOperations
    :ivar power: PowerOperations operations
    :vartype power: ignos.api.client.operations.PowerOperations
    :ivar suppliers: SuppliersOperations operations
    :vartype suppliers: ignos.api.client.operations.SuppliersOperations
    :ivar sustainability: SustainabilityOperations operations
    :vartype sustainability: ignos.api.client.operations.SustainabilityOperations
    :ivar upload: UploadOperations operations
    :vartype upload: ignos.api.client.operations.UploadOperations
    :ivar user: UserOperations operations
    :vartype user: ignos.api.client.operations.UserOperations
    :param credential: Credential needed for the client to connect to Azure.
    :type credential: ~azure.core.credentials.TokenCredential
    :param base_url: Service URL. Default value is ''.
    :type base_url: str
    """

    def __init__(
        self,
        credential,  # type: "TokenCredential"
        base_url="",  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        self._config = IgnosPortalConfiguration(credential=credential, **kwargs)
        self._client = PipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._serialize.client_side_validation = False
        self.apps = AppsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.assets = AssetsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.azure_regions = AzureRegionsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.cdf = CdfOperations(self._client, self._config, self._serialize, self._deserialize)
        self.cdf_clusters = CdfClustersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.countries = CountriesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.customers = CustomersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.databases = DatabasesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.customer_orders = CustomerOrdersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.workorders = WorkordersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.external = ExternalOperations(self._client, self._config, self._serialize, self._deserialize)
        self.external_access = ExternalAccessOperations(self._client, self._config, self._serialize, self._deserialize)
        self.electrical = ElectricalOperations(self._client, self._config, self._serialize, self._deserialize)
        self.welding = WeldingOperations(self._client, self._config, self._serialize, self._deserialize)
        self.machine_alarms = MachineAlarmsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.machine_utilization = MachineUtilizationOperations(self._client, self._config, self._serialize, self._deserialize)
        self.me = MeOperations(self._client, self._config, self._serialize, self._deserialize)
        self.measurement_form_schemas = MeasurementFormSchemasOperations(self._client, self._config, self._serialize, self._deserialize)
        self.measurement_forms_instances = MeasurementFormsInstancesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.measuring_tools = MeasuringToolsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.power = PowerOperations(self._client, self._config, self._serialize, self._deserialize)
        self.suppliers = SuppliersOperations(self._client, self._config, self._serialize, self._deserialize)
        self.sustainability = SustainabilityOperations(self._client, self._config, self._serialize, self._deserialize)
        self.upload = UploadOperations(self._client, self._config, self._serialize, self._deserialize)
        self.user = UserOperations(self._client, self._config, self._serialize, self._deserialize)


    def _send_request(
        self,
        request,  # type: HttpRequest
        **kwargs  # type: Any
    ):
        # type: (...) -> HttpResponse
        """Runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = client._send_request(request)
        <HttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/python/protocol/quickstart

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.HttpResponse
        """

        request_copy = deepcopy(request)
        request_copy.url = self._client.format_url(request_copy.url)
        return self._client.send_request(request_copy, **kwargs)

    def close(self):
        # type: () -> None
        self._client.close()

    def __enter__(self):
        # type: () -> IgnosPortal
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details):
        # type: (Any) -> None
        self._client.__exit__(*exc_details)
