"""
The HEA Server Buckets Microservice provides ...
"""
import http.client
import json
from typing import Optional, Dict, Union

from heaobject.root import Permission
from heaserver.service import response, appproperty
from heaserver.service.appproperty import HEA_DB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.bucket import Bucket
from heaserver.service.oidcclaimhdrs import SUB

MONGODB_BUCKET_COLLECTION = 'buckets'
VIEWER_PERMS = [Permission.COOWNER.name, Permission.VIEWER.name]


async def _get_bucket_dict(request: web.Request, var_parts_type: str) -> Optional[Union[web.Response, Dict]]:
    """
    Gets the bucket dict with the specified id.
    :param request: the HTTP request.
    :param var_parts_type: the var part type to query request with.
    :return: the requested bucket or http response error.
    """
    user = request.headers.get(SUB)
    volume_id = request.match_info["volume_id"]
    bucket_dict = await request.app[HEA_DB].get(request, MONGODB_BUCKET_COLLECTION, var_parts=var_parts_type, sub=user)

    def has_perms(obj_, user_, perms):
        def share_has_perms(share):
            return share.user == user_ and any(perm in perms for perm in share.permissions)

        return any(share_has_perms(share) for share in obj_.shares)

    if bucket_dict is None:
        return web.HTTPNotFound()
    # await mongoservicelib.get(request, MONGODB_BUCKET_COLLECTION)
    # bucket_body = json.loads(bucket_resp.body.decode("utf-8"))
    # todo
    # if bucket["owner"] == user or not (has_perms(bucket, user, VIEWER_PERMS)):
    #     return web.HTTPUnauthorized()
    return bucket_dict


@routes.get('/volume/{volume_id}/bucket/{id}')
async def get_bucket(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified id.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: 666f6f2d6261722d71757578
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    result = await _get_bucket_dict(request, 'id')
    if type(result) is dict:
        bucket_dict = result
    else:
        return result

    return await awsservicelib.get_bucket(request=request, volume_id=request.match_info['volume_id'], bucket=bucket_dict)


@routes.get('/volume/{volume_id}/buckets/byname/{name}')
async def get_bucket_by_name(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified name.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: Name of the bucket
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'

    """
    result = await _get_bucket_dict(request, 'name')
    if type(result) is dict:
        bucket_dict = result
    else:
        return result

    return await awsservicelib.get_bucket(request=request, volume_id=request.match_info['volume_id'], bucket=bucket_dict)


@routes.get('/volume/{volume_id}/buckets')
async def get_all_buckets(request: web.Request) -> web.Response:
    """
    Gets all buckets.
    :param request: the HTTP request.
    :return: all buckets.
    ---
    summary: get all buckets for a hea-volume associate with account.
    tags:
        - buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_buckets(request, volume_id=request.match_info["volume_id"])


@routes.post('/volume/{volume_id}/buckets/')
async def post_bucket(request: web.Request) -> web.Response:
    """
    Posts the provided bucket.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_BUCKET_COLLECTION, Bucket)


@routes.put('/volume/{volume_id}/buckets/{id}')
async def put_bucket(request: web.Request) -> web.Response:
    """
    Updates the bucket with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    """
    return await mongoservicelib.put(request, MONGODB_BUCKET_COLLECTION, Bucket)


@routes.delete('/volume/{volume_id}/bucket/{id}')
async def delete_bucket(request: web.Request) -> web.Response:
    """
    Deletes the bucket with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the bucket to delete.
          schema:
            type: string
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_bucket(request, request.match_info["volume_id"], request.match_info["id"])


def main() -> None:
    config = init_cmd_line(description='a service for managing buckets and their data within the cloud',
                           default_port=8080)
    start(db=mongo.Mongo, wstl_builder_factory=builder_factory(__package__), config=config)
