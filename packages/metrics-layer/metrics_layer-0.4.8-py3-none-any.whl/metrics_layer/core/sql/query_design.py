from typing import List

import networkx

from metrics_layer.core.model.base import MetricsLayerBase
from metrics_layer.core.sql.query_errors import ParseError


class MetricsLayerDesign:
    """ """

    def __init__(self, no_group_by: bool, query_type: str, field_lookup: dict, explore, project) -> None:
        self.no_group_by = no_group_by
        self.query_type = query_type
        self.field_lookup = field_lookup
        self.explore = explore
        self.project = project

    def views(self) -> List[MetricsLayerBase]:
        return self.project.views(explore_name=self.explore.name)

    def joins(self) -> List[MetricsLayerBase]:
        _, access_filter_fields = self.get_access_filter()
        fields_in_query = list(self.field_lookup.values()) + access_filter_fields
        required_views = list(set([v for field in fields_in_query for v in field.required_views()]))
        if self.explore.always_join:
            required_views.extend(self.explore.always_join)

        joins_needed_for_query = []
        for view_name in reversed(sorted(required_views)):
            joins_needed_for_query.extend(self._find_needed_joins(view_name, joins_needed_for_query))
        return self._sort_joins(joins_needed_for_query)

    def _find_needed_joins(self, view_name: str, joins_already_added: list):
        joins_to_add = []

        join_already_added = any(view_name == j.from_ for j in joins_already_added)
        if not join_already_added and view_name != self.explore.from_:
            join = self.explore.get_join(view_name, by_view_name=True)
            if join is None:
                raise ValueError(
                    f"Could not locate join from view {view_name} for explore {self.explore.name}"
                )
            joins_to_add.append(join)
            for view_name in join.required_views():
                joins_to_add.extend(self._find_needed_joins(view_name, joins_already_added + [join]))
        return joins_to_add

    def _sort_joins(self, joins_needed: list):
        if len(joins_needed) == 0:
            return []

        G = networkx.DiGraph()
        for join in joins_needed:
            for view_name in join.required_views():
                G.add_edge(view_name, join.from_)
        ordered_names = list(networkx.bfs_tree(G, source=self.base_view_name))
        # Skip the first one because that's *always* the base of the explore
        return [self.explore.get_join(name, by_view_name=True) for name in ordered_names[1:]]

    def get_view(self, name: str) -> MetricsLayerBase:
        try:
            return next(t for t in self.views() if t.name == name)
        except StopIteration:
            raise ParseError(f"View {name} not found in explore {self.explore.name}")

    def get_join(self, name: str) -> MetricsLayerBase:
        return next((j for j in self.joins() if j.name == name), None)

    def get_field(self, field_name: str, view_name: str = None) -> MetricsLayerBase:
        return self.project.get_field(field_name, view_name=view_name, explore_name=self.explore.name)

    def get_access_filter(self):
        if self.explore.access_filters:
            conditions, fields = [], []
            for condition_set in self.explore.access_filters:
                field = self.project.get_field(condition_set["field"], explore_name=self.explore.name)
                sql = field.sql_query(self.query_type)
                user_attribute_value = condition_set["user_attribute"]

                if self.project._user and self.project._user.get(user_attribute_value):
                    condition = f"{sql} = '{self.project._user[user_attribute_value]}'"
                    conditions.append(condition)
                    fields.append(field)
            return " and ".join(conditions), fields
        return None, []

    @property
    def base_view_name(self):
        return self.explore.from_
