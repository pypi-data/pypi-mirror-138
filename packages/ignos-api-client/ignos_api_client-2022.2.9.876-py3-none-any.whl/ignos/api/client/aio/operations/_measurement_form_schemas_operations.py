# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import functools
from typing import Any, Callable, Dict, Generic, Optional, TypeVar
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._measurement_form_schemas_operations import build_create_measurement_form_request, build_create_measurement_form_schema_link_request, build_create_schema_element_request, build_delete_measurement_form_schema_link_request, build_get_measurement_form_schema_request, build_get_measurement_form_settings_request, build_import_measurement_form_schema_request, build_list_measurment_form_schemas_request, build_release_schema_request, build_revoke_schema_request, build_update_measurement_form_schema_request, build_update_measurement_form_settings_request, build_upload_schema_attachment_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class MeasurementFormSchemasOperations:
    """MeasurementFormSchemasOperations async operations.

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

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    @distributed_trace_async
    async def list_measurment_form_schemas(
        self,
        page_size: Optional[int] = 50,
        customer_id: Optional[str] = None,
        part_number: Optional[str] = None,
        part_revision: Optional[str] = None,
        drawing: Optional[str] = None,
        drawing_revision: Optional[str] = None,
        continuation_token_parameter: Optional[str] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormDtoPagedResult":
        """list_measurment_form_schemas.

        :param page_size:
        :type page_size: int
        :param customer_id:
        :type customer_id: str
        :param part_number:
        :type part_number: str
        :param part_revision:
        :type part_revision: str
        :param drawing:
        :type drawing: str
        :param drawing_revision:
        :type drawing_revision: str
        :param continuation_token_parameter:
        :type continuation_token_parameter: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDtoPagedResult, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDtoPagedResult
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDtoPagedResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_list_measurment_form_schemas_request(
            page_size=page_size,
            customer_id=customer_id,
            part_number=part_number,
            part_revision=part_revision,
            drawing=drawing,
            drawing_revision=drawing_revision,
            continuation_token_parameter=continuation_token_parameter,
            template_url=self.list_measurment_form_schemas.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDtoPagedResult', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list_measurment_form_schemas.metadata = {'url': '/measurementforms/schemas'}  # type: ignore


    @distributed_trace_async
    async def create_measurement_form(
        self,
        body: Optional["_models.CreateMeasurementFormSchema"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormDto":
        """create_measurement_form.

        :param body:
        :type body: ~ignos.api.client.models.CreateMeasurementFormSchema
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'CreateMeasurementFormSchema')
        else:
            _json = None

        request = build_create_measurement_form_request(
            content_type=content_type,
            json=_json,
            template_url=self.create_measurement_form.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_measurement_form.metadata = {'url': '/measurementforms/schemas'}  # type: ignore


    @distributed_trace_async
    async def get_measurement_form_schema(
        self,
        id: str,
        **kwargs: Any
    ) -> "_models.MeasurementFormSchemaDto":
        """get_measurement_form_schema.

        :param id:
        :type id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormSchemaDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormSchemaDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormSchemaDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_get_measurement_form_schema_request(
            id=id,
            template_url=self.get_measurement_form_schema.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormSchemaDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_measurement_form_schema.metadata = {'url': '/measurementforms/schemas/{id}'}  # type: ignore


    @distributed_trace_async
    async def update_measurement_form_schema(
        self,
        id: str,
        body: Optional["_models.UpdateMeasurementFormSchemaRequest"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormSchemaDto":
        """update_measurement_form_schema.

        :param id:
        :type id: str
        :param body:
        :type body: ~ignos.api.client.models.UpdateMeasurementFormSchemaRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormSchemaDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormSchemaDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormSchemaDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'UpdateMeasurementFormSchemaRequest')
        else:
            _json = None

        request = build_update_measurement_form_schema_request(
            id=id,
            content_type=content_type,
            json=_json,
            template_url=self.update_measurement_form_schema.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormSchemaDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update_measurement_form_schema.metadata = {'url': '/measurementforms/schemas/{id}'}  # type: ignore


    @distributed_trace_async
    async def upload_schema_attachment(
        self,
        id: str,
        body: Optional["_models.UploadRequest"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormSchemaDto":
        """upload_schema_attachment.

        :param id:
        :type id: str
        :param body:
        :type body: ~ignos.api.client.models.UploadRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormSchemaDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormSchemaDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormSchemaDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'UploadRequest')
        else:
            _json = None

        request = build_upload_schema_attachment_request(
            id=id,
            content_type=content_type,
            json=_json,
            template_url=self.upload_schema_attachment.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormSchemaDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    upload_schema_attachment.metadata = {'url': '/measurementforms/schemas/{id}/uploadattachment'}  # type: ignore


    @distributed_trace_async
    async def create_schema_element(
        self,
        schema_id: str,
        body: Optional["_models.CreateSchemaElement"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormElementDto":
        """create_schema_element.

        :param schema_id:
        :type schema_id: str
        :param body:
        :type body: ~ignos.api.client.models.CreateSchemaElement
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormElementDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormElementDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormElementDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'CreateSchemaElement')
        else:
            _json = None

        request = build_create_schema_element_request(
            schema_id=schema_id,
            content_type=content_type,
            json=_json,
            template_url=self.create_schema_element.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormElementDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_schema_element.metadata = {'url': '/measurementforms/schemas/{schemaId}/elements'}  # type: ignore


    @distributed_trace_async
    async def create_measurement_form_schema_link(
        self,
        schema_id: str,
        body: Optional["_models.CreateMeasurementFormSchemaLinkRequest"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormDto":
        """create_measurement_form_schema_link.

        :param schema_id:
        :type schema_id: str
        :param body:
        :type body: ~ignos.api.client.models.CreateMeasurementFormSchemaLinkRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'CreateMeasurementFormSchemaLinkRequest')
        else:
            _json = None

        request = build_create_measurement_form_schema_link_request(
            schema_id=schema_id,
            content_type=content_type,
            json=_json,
            template_url=self.create_measurement_form_schema_link.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_measurement_form_schema_link.metadata = {'url': '/measurementforms/schemas/{schemaId}/link'}  # type: ignore


    @distributed_trace_async
    async def delete_measurement_form_schema_link(
        self,
        schema_id: str,
        linked_schema_id: str,
        **kwargs: Any
    ) -> None:
        """delete_measurement_form_schema_link.

        :param schema_id:
        :type schema_id: str
        :param linked_schema_id:
        :type linked_schema_id: str
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

        
        request = build_delete_measurement_form_schema_link_request(
            schema_id=schema_id,
            linked_schema_id=linked_schema_id,
            template_url=self.delete_measurement_form_schema_link.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if cls:
            return cls(pipeline_response, None, {})

    delete_measurement_form_schema_link.metadata = {'url': '/measurementforms/schemas/{schemaId}/link/{linkedSchemaId}'}  # type: ignore


    @distributed_trace_async
    async def release_schema(
        self,
        schema_id: str,
        **kwargs: Any
    ) -> "_models.MeasurementFormDto":
        """release_schema.

        :param schema_id:
        :type schema_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_release_schema_request(
            schema_id=schema_id,
            template_url=self.release_schema.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    release_schema.metadata = {'url': '/measurementforms/schemas/{schemaId}/release'}  # type: ignore


    @distributed_trace_async
    async def revoke_schema(
        self,
        schema_id: str,
        **kwargs: Any
    ) -> "_models.MeasurementFormDto":
        """revoke_schema.

        :param schema_id:
        :type schema_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_revoke_schema_request(
            schema_id=schema_id,
            template_url=self.revoke_schema.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    revoke_schema.metadata = {'url': '/measurementforms/schemas/{schemaId}/revoke'}  # type: ignore


    @distributed_trace_async
    async def get_measurement_form_settings(
        self,
        **kwargs: Any
    ) -> "_models.MeasurementFormSettingsDto":
        """get_measurement_form_settings.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormSettingsDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormSettingsDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormSettingsDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        
        request = build_get_measurement_form_settings_request(
            template_url=self.get_measurement_form_settings.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormSettingsDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_measurement_form_settings.metadata = {'url': '/measurementforms/schemas/settings'}  # type: ignore


    @distributed_trace_async
    async def update_measurement_form_settings(
        self,
        body: Optional["_models.UpdateMeasurementFormSettings"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormSettingsDto":
        """update_measurement_form_settings.

        :param body:
        :type body: ~ignos.api.client.models.UpdateMeasurementFormSettings
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormSettingsDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormSettingsDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormSettingsDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'UpdateMeasurementFormSettings')
        else:
            _json = None

        request = build_update_measurement_form_settings_request(
            content_type=content_type,
            json=_json,
            template_url=self.update_measurement_form_settings.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormSettingsDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update_measurement_form_settings.metadata = {'url': '/measurementforms/schemas/settings'}  # type: ignore


    @distributed_trace_async
    async def import_measurement_form_schema(
        self,
        body: Optional["_models.ImportMeasurementFormSchema"] = None,
        **kwargs: Any
    ) -> "_models.MeasurementFormDto":
        """import_measurement_form_schema.

        :param body:
        :type body: ~ignos.api.client.models.ImportMeasurementFormSchema
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MeasurementFormDto, or the result of cls(response)
        :rtype: ~ignos.api.client.models.MeasurementFormDto
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.MeasurementFormDto"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        if body is not None:
            _json = self._serialize.body(body, 'ImportMeasurementFormSchema')
        else:
            _json = None

        request = build_import_measurement_form_schema_request(
            content_type=content_type,
            json=_json,
            template_url=self.import_measurement_form_schema.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        deserialized = self._deserialize('MeasurementFormDto', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    import_measurement_form_schema.metadata = {'url': '/measurementforms/schemas/import'}  # type: ignore

