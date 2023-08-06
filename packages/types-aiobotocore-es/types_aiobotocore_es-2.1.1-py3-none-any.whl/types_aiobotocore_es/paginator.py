"""
Type annotations for es service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_es.client import ElasticsearchServiceClient
    from types_aiobotocore_es.paginator import (
        DescribeReservedElasticsearchInstanceOfferingsPaginator,
        DescribeReservedElasticsearchInstancesPaginator,
        GetUpgradeHistoryPaginator,
        ListElasticsearchInstanceTypesPaginator,
        ListElasticsearchVersionsPaginator,
    )

    session = get_session()
    with session.create_client("es") as client:
        client: ElasticsearchServiceClient

        describe_reserved_elasticsearch_instance_offerings_paginator: DescribeReservedElasticsearchInstanceOfferingsPaginator = client.get_paginator("describe_reserved_elasticsearch_instance_offerings")
        describe_reserved_elasticsearch_instances_paginator: DescribeReservedElasticsearchInstancesPaginator = client.get_paginator("describe_reserved_elasticsearch_instances")
        get_upgrade_history_paginator: GetUpgradeHistoryPaginator = client.get_paginator("get_upgrade_history")
        list_elasticsearch_instance_types_paginator: ListElasticsearchInstanceTypesPaginator = client.get_paginator("list_elasticsearch_instance_types")
        list_elasticsearch_versions_paginator: ListElasticsearchVersionsPaginator = client.get_paginator("list_elasticsearch_versions")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterable
else:
    from typing_extensions import AsyncIterable


__all__ = (
    "DescribeReservedElasticsearchInstanceOfferingsPaginator",
    "DescribeReservedElasticsearchInstancesPaginator",
    "GetUpgradeHistoryPaginator",
    "ListElasticsearchInstanceTypesPaginator",
    "ListElasticsearchVersionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeReservedElasticsearchInstanceOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#describereservedelasticsearchinstanceofferingspaginator)
    """

    def paginate(
        self,
        *,
        ReservedElasticsearchInstanceOfferingId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterable[DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstanceOfferings.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#describereservedelasticsearchinstanceofferingspaginator)
        """


class DescribeReservedElasticsearchInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#describereservedelasticsearchinstancespaginator)
    """

    def paginate(
        self,
        *,
        ReservedElasticsearchInstanceId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterable[DescribeReservedElasticsearchInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.DescribeReservedElasticsearchInstances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#describereservedelasticsearchinstancespaginator)
        """


class GetUpgradeHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.GetUpgradeHistory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#getupgradehistorypaginator)
    """

    def paginate(
        self, *, DomainName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterable[GetUpgradeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.GetUpgradeHistory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#getupgradehistorypaginator)
        """


class ListElasticsearchInstanceTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#listelasticsearchinstancetypespaginator)
    """

    def paginate(
        self,
        *,
        ElasticsearchVersion: str,
        DomainName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterable[ListElasticsearchInstanceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchInstanceTypes.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#listelasticsearchinstancetypespaginator)
        """


class ListElasticsearchVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchVersions)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#listelasticsearchversionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterable[ListElasticsearchVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Paginator.ListElasticsearchVersions.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_es/paginators.html#listelasticsearchversionspaginator)
        """
