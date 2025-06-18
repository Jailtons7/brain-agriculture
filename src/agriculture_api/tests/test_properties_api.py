import pytest

from rest_framework.test import APIClient

from agriculture_api.models import Property, Farmer
from agriculture_api.validators import AREAS_ERROR_MESSAGE


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def farmer():
    return Farmer.objects.create(name='Farmer 1', document='50973944021')


@pytest.mark.django_db
def test_create_property(api_client, farmer):
    data = {
        'name': 'Faz. Três Corações',
        'city': 'Nova Lima',
        'state': 'Minas Gerais',
        'total_area': '125.12',
        'arable_area': '25.12',
        'vegetation_area': '100.00',
        'farmer': farmer.pk,
    }
    response = api_client.post('/api/properties/', data, format='json')

    assert response.status_code == 201
    assert Property.objects.count() == 1
    assert Property.objects.get(farmer__document=farmer.document).name == data['name']


@pytest.mark.django_db
def test_create_property_invalid_are(api_client, farmer):
    data = {
        'name': 'Faz. Três Corações',
        'city': 'Nova Lima',
        'state': 'Minas Gerais',
        'total_area': 0.0,
        'arable_area': 25.13,
        'vegetation_area': 100.00,
        'farmer': farmer.pk,
    }
    response = api_client.post('/api/properties/', data, format='json')

    assert response.status_code == 400
    assert Property.objects.count() == 0
    assert AREAS_ERROR_MESSAGE['total_area'] in response.json()['total_area'][0]


@pytest.mark.django_db
def test_list_properties(api_client, farmer):
    farm_names = ['Faz. Três Corações', 'Faz. Esperança']
    data = [
        {
            'name': farm_names[0],
            'city': 'Nova Lima',
            'state': 'Minas Gerais',
            'total_area': '125.12',
            'arable_area': '25.12',
            'vegetation_area': '100.00',
            'farmer': farmer,
        },
        {
            'name': farm_names[1],
            'city': 'Nova Lima',
            'state': 'Minas Gerais',
            'total_area': '125.12',
            'arable_area': '25.12',
            'vegetation_area': '100.00',
            'farmer': farmer,
        }
    ]
    Property.objects.create(**data[0])
    Property.objects.create(**data[1])
    response = api_client.get('/api/properties/')
    assert response.status_code == 200
    assert Property.objects.count() == 2
    assert sorted([prop['name'] for prop in response.json()]) == sorted(farm_names)


@pytest.mark.django_db
def test_delete_property(api_client, farmer):
    property = Property.objects.create(**{
            'name': 'Faz. Três Corações',
            'city': 'Nova Lima',
            'state': 'Minas Gerais',
            'total_area': '125.12',
            'arable_area': '25.12',
            'vegetation_area': '100.00',
            'farmer': farmer,
        })

    response = api_client.delete(f'/api/properties/{property.pk}/')

    assert response.status_code == 204
    with pytest.raises(Property.DoesNotExist):
        Property.objects.get(pk=property.pk)


@pytest.mark.django_db
def test_update_property(api_client, farmer):
    wrong_name = 'Faz. Dez Corações'
    right_name = "Faz. Três Corações"
    property = Property.objects.create(**{
        'name': wrong_name,
        'city': 'Nova Lima',
        'state': 'Minas Gerais',
        'total_area': '125.12',
        'arable_area': '25.12',
        'vegetation_area': '100.00',
        'farmer': farmer,
    })

    response = api_client.patch(f'/api/properties/{property.pk}/', {"name": right_name})
    assert response.status_code == 200
    with pytest.raises(Property.DoesNotExist):
        Property.objects.get(name=wrong_name)
    property.refresh_from_db()
    assert property.name == right_name


@pytest.mark.django_db
def test_retrieve_property(api_client, farmer):
    property = Property.objects.create(**{
        'name': 'Faz. Três Corações',
        'city': 'Nova Lima',
        'state': 'Minas Gerais',
        'total_area': '125.12',
        'arable_area': '25.12',
        'vegetation_area': '100.00',
        'farmer': farmer,
    })
    response = api_client.get(f'/api/properties/{property.pk}/')
    assert response.status_code == 200
    assert response.json()['name'] == property.name
