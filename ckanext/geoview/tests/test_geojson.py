import pytest 

from ckan.tests import factories
from ckan.plugins import toolkit

from ckanext.geoview.plugin import GeoJSONView

@pytest.mark.ckan_config('ckan.views.default_views', 'geojson_view')
def test_geojson_view_is_rendered(app):
    view_default_title = GeoJSONView().info()["title"]
    dataset = factories.Dataset()

    for format in GeoJSONView.GeoJSON:
        resource = factories.Resource(
            name='My Resource',
            format=format,
            package_id=dataset['id']
        )

        if toolkit.check_ckan_version("2.9"):
            url = toolkit.url_for(
                "{}_resource.read".format(dataset["type"]),
                id=dataset["name"],
                resource_id=resource["id"],
            )
        else:
            url = toolkit.url_for(
                controller="package",
                action="resource_read",
                id=resource["package_id"],
                resource_id=resource["id"],
            )
        
        res = app.get(url)
        assert 'class="resource-view"' in res.body
        assert 'data-title="{}"'.format(view_default_title) in res.body
        assert 'id="view-' in res.body
