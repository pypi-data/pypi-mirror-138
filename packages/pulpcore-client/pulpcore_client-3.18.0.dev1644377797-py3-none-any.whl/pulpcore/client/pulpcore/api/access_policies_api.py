# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pulpcore.client.pulpcore.api_client import ApiClient
from pulpcore.client.pulpcore.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class AccessPoliciesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list(self, **kwargs):  # noqa: E501
        """List access policys  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool customized:
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str viewset_name: Filter results where viewset_name matches value
        :param str viewset_name__contains: Filter results where viewset_name contains value
        :param str viewset_name__icontains: Filter results where viewset_name contains value
        :param list[str] viewset_name__in: Filter results where viewset_name is in a comma-separated list of values
        :param str viewset_name__startswith: Filter results where viewset_name starts with value
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PaginatedAccessPolicyResponseList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(**kwargs)  # noqa: E501

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List access policys  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool customized:
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str ordering: Which field to use when ordering the results.
        :param str viewset_name: Filter results where viewset_name matches value
        :param str viewset_name__contains: Filter results where viewset_name contains value
        :param str viewset_name__icontains: Filter results where viewset_name contains value
        :param list[str] viewset_name__in: Filter results where viewset_name is in a comma-separated list of values
        :param str viewset_name__startswith: Filter results where viewset_name starts with value
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PaginatedAccessPolicyResponseList, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'customized',
            'limit',
            'offset',
            'ordering',
            'viewset_name',
            'viewset_name__contains',
            'viewset_name__icontains',
            'viewset_name__in',
            'viewset_name__startswith',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'customized' in local_var_params and local_var_params['customized'] is not None:  # noqa: E501
            query_params.append(('customized', local_var_params['customized']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501
        if 'viewset_name' in local_var_params and local_var_params['viewset_name'] is not None:  # noqa: E501
            query_params.append(('viewset_name', local_var_params['viewset_name']))  # noqa: E501
        if 'viewset_name__contains' in local_var_params and local_var_params['viewset_name__contains'] is not None:  # noqa: E501
            query_params.append(('viewset_name__contains', local_var_params['viewset_name__contains']))  # noqa: E501
        if 'viewset_name__icontains' in local_var_params and local_var_params['viewset_name__icontains'] is not None:  # noqa: E501
            query_params.append(('viewset_name__icontains', local_var_params['viewset_name__icontains']))  # noqa: E501
        if 'viewset_name__in' in local_var_params and local_var_params['viewset_name__in'] is not None:  # noqa: E501
            query_params.append(('viewset_name__in', local_var_params['viewset_name__in']))  # noqa: E501
            collection_formats['viewset_name__in'] = 'csv'  # noqa: E501
        if 'viewset_name__startswith' in local_var_params and local_var_params['viewset_name__startswith'] is not None:  # noqa: E501
            query_params.append(('viewset_name__startswith', local_var_params['viewset_name__startswith']))  # noqa: E501
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/access_policies/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PaginatedAccessPolicyResponseList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def partial_update(self, access_policy_href, patched_access_policy, **kwargs):  # noqa: E501
        """Update an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.partial_update(access_policy_href, patched_access_policy, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param PatchedAccessPolicy patched_access_policy: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessPolicyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.partial_update_with_http_info(access_policy_href, patched_access_policy, **kwargs)  # noqa: E501

    def partial_update_with_http_info(self, access_policy_href, patched_access_policy, **kwargs):  # noqa: E501
        """Update an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.partial_update_with_http_info(access_policy_href, patched_access_policy, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param PatchedAccessPolicy patched_access_policy: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AccessPolicyResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'access_policy_href',
            'patched_access_policy'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method partial_update" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'access_policy_href' is set
        if self.api_client.client_side_validation and ('access_policy_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_policy_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_policy_href` when calling `partial_update`")  # noqa: E501
        # verify the required parameter 'patched_access_policy' is set
        if self.api_client.client_side_validation and ('patched_access_policy' not in local_var_params or  # noqa: E501
                                                        local_var_params['patched_access_policy'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `patched_access_policy` when calling `partial_update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'access_policy_href' in local_var_params:
            path_params['access_policy_href'] = local_var_params['access_policy_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'patched_access_policy' in local_var_params:
            body_params = local_var_params['patched_access_policy']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{access_policy_href}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccessPolicyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, access_policy_href, **kwargs):  # noqa: E501
        """Inspect an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(access_policy_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessPolicyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(access_policy_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, access_policy_href, **kwargs):  # noqa: E501
        """Inspect an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(access_policy_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AccessPolicyResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'access_policy_href',
            'fields',
            'exclude_fields'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'access_policy_href' is set
        if self.api_client.client_side_validation and ('access_policy_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_policy_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_policy_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'access_policy_href' in local_var_params:
            path_params['access_policy_href'] = local_var_params['access_policy_href']  # noqa: E501

        query_params = []
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{access_policy_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccessPolicyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reset(self, access_policy_href, **kwargs):  # noqa: E501
        """reset  # noqa: E501

        Reset the access policy to its uncustomized default value.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset(access_policy_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessPolicyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.reset_with_http_info(access_policy_href, **kwargs)  # noqa: E501

    def reset_with_http_info(self, access_policy_href, **kwargs):  # noqa: E501
        """reset  # noqa: E501

        Reset the access policy to its uncustomized default value.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reset_with_http_info(access_policy_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AccessPolicyResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'access_policy_href'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reset" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'access_policy_href' is set
        if self.api_client.client_side_validation and ('access_policy_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_policy_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_policy_href` when calling `reset`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'access_policy_href' in local_var_params:
            path_params['access_policy_href'] = local_var_params['access_policy_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{access_policy_href}reset/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccessPolicyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update(self, access_policy_href, access_policy, **kwargs):  # noqa: E501
        """Update an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update(access_policy_href, access_policy, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param AccessPolicy access_policy: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessPolicyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.update_with_http_info(access_policy_href, access_policy, **kwargs)  # noqa: E501

    def update_with_http_info(self, access_policy_href, access_policy, **kwargs):  # noqa: E501
        """Update an access policy  # noqa: E501

        ViewSet for AccessPolicy.  NOTE: This API endpoint is in \"tech preview\" and subject to change  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_with_http_info(access_policy_href, access_policy, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str access_policy_href: (required)
        :param AccessPolicy access_policy: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AccessPolicyResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'access_policy_href',
            'access_policy'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'access_policy_href' is set
        if self.api_client.client_side_validation and ('access_policy_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_policy_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_policy_href` when calling `update`")  # noqa: E501
        # verify the required parameter 'access_policy' is set
        if self.api_client.client_side_validation and ('access_policy' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_policy'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_policy` when calling `update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'access_policy_href' in local_var_params:
            path_params['access_policy_href'] = local_var_params['access_policy_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'access_policy' in local_var_params:
            body_params = local_var_params['access_policy']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'cookieAuth']  # noqa: E501

        return self.api_client.call_api(
            '{access_policy_href}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccessPolicyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
