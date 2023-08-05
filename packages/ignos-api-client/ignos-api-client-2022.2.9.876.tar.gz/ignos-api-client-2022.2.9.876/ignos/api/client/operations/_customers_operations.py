# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import functools
from typing import TYPE_CHECKING
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from msrest import Serializer

from .. import models as _models
from .._vendor import _convert_request, _format_url_section

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False
# fmt: off

def build_list_customers_request(
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    page_size = kwargs.pop('page_size', 100)  # type: Optional[int]
    continuation_token_parameter = kwargs.pop('continuation_token_parameter', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers')

    # Construct parameters
    query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    if page_size is not None:
        query_parameters['pageSize'] = _SERIALIZER.query("page_size", page_size, 'int')
    if continuation_token_parameter is not None:
        query_parameters['continuationToken'] = _SERIALIZER.query("continuation_token_parameter", continuation_token_parameter, 'str')

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        params=query_parameters,
        headers=header_parameters,
        **kwargs
    )


def build_create_customer_request(
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers')

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="POST",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_get_customer_request(
    id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_update_customer_request(
    id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="PUT",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_list_customer_tenants_request(
    id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/tenants')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_create_tenant_request(
    id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/tenants')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="POST",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_update_tenant_request(
    id,  # type: str
    tenant_id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    content_type = kwargs.pop('content_type', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/tenants/{tenantId}')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
        "tenantId": _SERIALIZER.url("tenant_id", tenant_id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    if content_type is not None:
        header_parameters['Content-Type'] = _SERIALIZER.header("content_type", content_type, 'str')
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="PUT",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_list_customer_apps_request(
    id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/apps')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        headers=header_parameters,
        **kwargs
    )


def build_list_tenants_details_request(
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    tenant_id_prefix = kwargs.pop('tenant_id_prefix', None)  # type: Optional[str]
    app_id = kwargs.pop('app_id', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/tenants/details')

    # Construct parameters
    query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    if tenant_id_prefix is not None:
        query_parameters['tenantIdPrefix'] = _SERIALIZER.query("tenant_id_prefix", tenant_id_prefix, 'str')
    if app_id is not None:
        query_parameters['appId'] = _SERIALIZER.query("app_id", app_id, 'str')

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        params=query_parameters,
        headers=header_parameters,
        **kwargs
    )


def build_add_customer_app_request(
    id,  # type: str
    app_id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/apps/{appId}')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
        "appId": _SERIALIZER.url("app_id", app_id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    return HttpRequest(
        method="POST",
        url=url,
        **kwargs
    )


def build_remove_customer_app_request(
    id,  # type: str
    app_id,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/{id}/apps/{appId}')
    path_format_arguments = {
        "id": _SERIALIZER.url("id", id, 'str'),
        "appId": _SERIALIZER.url("app_id", app_id, 'str'),
    }

    url = _format_url_section(url, **path_format_arguments)

    return HttpRequest(
        method="DELETE",
        url=url,
        **kwargs
    )


def build_list_tenant_keys_request(
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    accept = "application/json"
    # Construct URL
    url = kwargs.pop("template_url", '/admin/customers/tenantkeys')

    # Construct headers
    header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=url,
        headers=header_parameters,
        **kwargs
    )

# fmt: on
class CustomersOperations(object):
    """CustomersOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~ignos.api.client.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    @distributed_trace
    def list_customers(
        self,
        page_size=100,  # type: Optional[int]
        continuation_token_parameter=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> List["_models.IgnosCustomerDto"]
        """Internal Ignos api for listing customers.

        Internal Ignos api for listing customers.

        :param page_size:
        :type page_size: int
        :param continuation_token_parameter:
        :type continuation_token_parameter: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of IgnosCustomerDto, or the result of cls(response)
        :rtype: list[~ignos.api.client.models.IgnosCustomerDto]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["_models.IgnosCustomerDto"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_customers_request(
            page_size=page_size,
            continuation_token_parameter=continuation_token_parameter,
            template_url=self.list_customers.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('[IgnosCustomerDto]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_customers.metadata = {'url': '/admin/customers'}  # type: ignore


    @distributed_trace
    def create_customer(
        self,
        body=None,  # type: Optional["_models.CreateIgnosCustomer"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.IgnosCustomerDto"
        """Internal Ignos api for creating a customer.

        Internal Ignos api for creating a customer.

        :param body:
        :type body: ~ignos.api.client.models.CreateIgnosCustomer
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: IgnosCustomerDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.IgnosCustomerDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.IgnosCustomerDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'CreateIgnosCustomer')
        else:
            _json = None

        request = build_create_customer_request(
            content_type=content_type,
            json=_json,
            template_url=self.create_customer.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('IgnosCustomerDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_customer.metadata = {'url': '/admin/customers'}  # type: ignore


    @distributed_trace
    def get_customer(
        self,
        id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.IgnosCustomerDto"
        """Internal Ignos api for getting a customer.

        Internal Ignos api for getting a customer.

        :param id:
        :type id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: IgnosCustomerDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.IgnosCustomerDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.IgnosCustomerDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_get_customer_request(
            id=id,
            template_url=self.get_customer.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('IgnosCustomerDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_customer.metadata = {'url': '/admin/customers/{id}'}  # type: ignore


    @distributed_trace
    def update_customer(
        self,
        id,  # type: str
        body=None,  # type: Optional["_models.UpdateCustomerRequest"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.IgnosCustomerDto"
        """Internal Ignos api for updating a customer.

        Internal Ignos api for updating a customer.

        :param id:
        :type id: str
        :param body:
        :type body: ~ignos.api.client.models.UpdateCustomerRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: IgnosCustomerDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.IgnosCustomerDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.IgnosCustomerDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'UpdateCustomerRequest')
        else:
            _json = None

        request = build_update_customer_request(
            id=id,
            content_type=content_type,
            json=_json,
            template_url=self.update_customer.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('IgnosCustomerDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update_customer.metadata = {'url': '/admin/customers/{id}'}  # type: ignore


    @distributed_trace
    def list_customer_tenants(
        self,
        id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> List["_models.TenantDto"]
        """Internal Ignos api for a customer's tenants.

        Internal Ignos api for a customer's tenants.

        :param id:
        :type id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of TenantDto, or the result of cls(response)
        :rtype: list[~ignos.api.client.models.TenantDto]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["_models.TenantDto"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_customer_tenants_request(
            id=id,
            template_url=self.list_customer_tenants.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('[TenantDto]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_customer_tenants.metadata = {'url': '/admin/customers/{id}/tenants'}  # type: ignore


    @distributed_trace
    def create_tenant(
        self,
        id,  # type: str
        body=None,  # type: Optional["_models.CreateTenantRequest"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.TenantDto"
        """Internal Ignos api for creating a customer tenant.

        Internal Ignos api for creating a customer tenant.

        :param id:
        :type id: str
        :param body:
        :type body: ~ignos.api.client.models.CreateTenantRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: TenantDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.TenantDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.TenantDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'CreateTenantRequest')
        else:
            _json = None

        request = build_create_tenant_request(
            id=id,
            content_type=content_type,
            json=_json,
            template_url=self.create_tenant.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('TenantDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_tenant.metadata = {'url': '/admin/customers/{id}/tenants'}  # type: ignore


    @distributed_trace
    def update_tenant(
        self,
        id,  # type: str
        tenant_id,  # type: str
        body=None,  # type: Optional["_models.UpdateTenantRequest"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.TenantDto"
        """Internal Ignos api for updating a customer tenant.

        Internal Ignos api for updating a customer tenant.

        :param id:
        :type id: str
        :param tenant_id:
        :type tenant_id: str
        :param body:
        :type body: ~ignos.api.client.models.UpdateTenantRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: TenantDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.TenantDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.TenantDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'UpdateTenantRequest')
        else:
            _json = None

        request = build_update_tenant_request(
            id=id,
            tenant_id=tenant_id,
            content_type=content_type,
            json=_json,
            template_url=self.update_tenant.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('TenantDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update_tenant.metadata = {'url': '/admin/customers/{id}/tenants/{tenantId}'}  # type: ignore


    @distributed_trace
    def list_customer_apps(
        self,
        id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> List["_models.CustomerAppDto"]
        """Internal Ignos api for listing customer apps.

        Internal Ignos api for listing customer apps.

        :param id:
        :type id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of CustomerAppDto, or the result of cls(response)
        :rtype: list[~ignos.api.client.models.CustomerAppDto]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["_models.CustomerAppDto"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_customer_apps_request(
            id=id,
            template_url=self.list_customer_apps.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('[CustomerAppDto]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_customer_apps.metadata = {'url': '/admin/customers/{id}/apps'}  # type: ignore


    @distributed_trace
    def list_tenants_details(
        self,
        tenant_id_prefix=None,  # type: Optional[str]
        app_id=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> List["_models.TenantDetailDto"]
        """Internal Ignos api for listing tenants.

        Internal Ignos api for listing tenants.

        :param tenant_id_prefix:
        :type tenant_id_prefix: str
        :param app_id:
        :type app_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of TenantDetailDto, or the result of cls(response)
        :rtype: list[~ignos.api.client.models.TenantDetailDto]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["_models.TenantDetailDto"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_tenants_details_request(
            tenant_id_prefix=tenant_id_prefix,
            app_id=app_id,
            template_url=self.list_tenants_details.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('[TenantDetailDto]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_tenants_details.metadata = {'url': '/admin/customers/tenants/details'}  # type: ignore


    @distributed_trace
    def add_customer_app(
        self,
        id,  # type: str
        app_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Internal Ignos api for adding an app to a customer.

        Internal Ignos api for adding an app to a customer.

        :param id:
        :type id: str
        :param app_id:
        :type app_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_add_customer_app_request(
            id=id,
            app_id=app_id,
            template_url=self.add_customer_app.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if cls:
            return cls(pipeline_response, None, {})

    add_customer_app.metadata = {'url': '/admin/customers/{id}/apps/{appId}'}  # type: ignore


    @distributed_trace
    def remove_customer_app(
        self,
        id,  # type: str
        app_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Internal Ignos api for removing an app from a customer.

        Internal Ignos api for removing an app from a customer.

        :param id:
        :type id: str
        :param app_id:
        :type app_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_remove_customer_app_request(
            id=id,
            app_id=app_id,
            template_url=self.remove_customer_app.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if cls:
            return cls(pipeline_response, None, {})

    remove_customer_app.metadata = {'url': '/admin/customers/{id}/apps/{appId}'}  # type: ignore


    @distributed_trace
    def list_tenant_keys(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> List["_models.TenantKeyDto"]
        """list_tenant_keys.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of TenantKeyDto, or the result of cls(response)
        :rtype: list[~ignos.api.client.models.TenantKeyDto]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["_models.TenantKeyDto"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_tenant_keys_request(
            template_url=self.list_tenant_keys.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('[TenantKeyDto]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_tenant_keys.metadata = {'url': '/admin/customers/tenantkeys'}  # type: ignore

