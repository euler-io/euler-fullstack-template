from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

TypeX = TypeVar('TypeX')
TypeY = TypeVar('TypeY')


class ElasticsearchHitBaseModel(BaseModel):
    id: str
    score: Optional[float] = None


class ElasticsearchHitExtendedModel(ElasticsearchHitBaseModel):
    index: str


class ElasticsearchInnerHit(GenericModel, Generic[TypeY]):
    __root__: List[TypeY]


class ElasticsearchHitListModel(GenericModel, Generic[TypeX]):
    __root__: List[TypeX]


class ElasticsearchResponseModel(GenericModel, Generic[TypeX]):
    took: int
    total_hits: int
    max_score: Optional[float] = None
    hits: ElasticsearchHitListModel[TypeX] = []


class ElasticsearchModelConverter():

    __COMMON_FIELDS = {"id", "index", "score"}

    def __init__(self,
                 model: Type[ElasticsearchHitBaseModel],
                 inner_hits_fields: list = []):
        self.model = model
        self.common_fields = self.get_common_fields()
        self.inner_hits_fields = self.get_inner_hits_fields()
        self.highlightable_fields = self.get_highlightable_fields()

    def get_common_fields(self) -> List[Field]:
        return list(filter(lambda f: f.name in self.__COMMON_FIELDS,
                           self.model.__fields__.values()))

    def get_inner_hits_fields(self) -> List[Field]:
        return list(filter(lambda f: f.name not in self.__COMMON_FIELDS and issubclass(f.type_, ElasticsearchInnerHit),
                           self.model.__fields__.values()))

    def get_highlightable_fields(self) -> List[Field]:
        return list(filter(lambda f: f.name not in self.__COMMON_FIELDS and not issubclass(f.type_, ElasticsearchInnerHit),
                           self.model.__fields__.values()))

    def convert(self, resp: dict, highlightable: bool = True) -> ElasticsearchResponseModel:
        max_score = resp["hits"]["max_score"]
        return ElasticsearchResponseModel(
            took=resp["took"],
            total_hits=int(resp["hits"]["total"]["value"]),
            max_score=float(max_score if max_score else 0),
            hits=ElasticsearchHitListModel(__root__=[
                self.convert_hit(h, highlightable=highlightable) for h in resp["hits"]["hits"]
            ])
        )

    def convert_hit(self, hit: dict, highlightable: bool = True) -> ElasticsearchHitBaseModel:
        kwargs = self.get_common_fields_values(hit)

        kwargs.update(self.get_highlightable_fields_values(hit))
        kwargs.update(self.get_inner_hits_fields_values(hit))

        return self.model(**kwargs)

    def get_common_fields_values(self, hit: dict) -> dict:
        values = {}
        for field in self.common_fields:
            field_name = field.name
            key = f"_{field_name}"
            values[field_name] = hit[key]
        return values

    def get_highlightable_fields_values(self, hit: dict, highlightable: bool = True) -> dict:
        values = {}
        source = hit["_source"]
        highlight = hit["highlight"] if highlightable and "highlight" in hit else None

        for field in self.highlightable_fields:
            field_name = field.name

            if highlight and field_name in highlight:
                value = highlight[field_name][0]
            elif field_name in source:
                value = source[field_name]
            else:
                value = None

            values[field_name] = value

        return values

    def get_inner_hits_fields_values(self, hit: dict, highlightable: bool = True) -> dict:
        values = {}

        if "inner_hits" in hit:
            inner_hits = hit["inner_hits"]
            for field in self.inner_hits_fields:
                field_name = field.name
                value_list = []
                for inner_hit in inner_hits.values():
                    hits = inner_hit["hits"]["hits"]
                    for hit in hits:
                        source = hit["_source"]
                        highlight = hit["highlight"] if highlightable and "highlight" in hit else None

                        if highlight and field_name in highlight:
                            value_list.append(highlight[field_name][0])
                        elif field_name in source:
                            value_list.append(source[field_name])

                values[field_name] = value_list

        return values
