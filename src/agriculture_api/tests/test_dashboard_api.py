import pytest

from rest_framework.test import APIClient

from agriculture_api.models import (
    Farmer, Property, Harvest, CultivatedCrop, CropInProperty
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def dashboard_data():
    farmer_1 = dict(name='Farmer One', document='12345678900')
    farmer_2 = dict(name='Farmer Two', document='09876543211')
    total_area_1 = 1000.0
    total_area_2 = 500.0
    farmer1 = Farmer.objects.create(**farmer_1)
    farmer2 = Farmer.objects.create(**farmer_2)
    property_1 = dict(
        name='Property 1', city='Cidade A', state='Estado X',
        total_area=total_area_1, arable_area=total_area_1 / 2, vegetation_area=total_area_1 / 2,
        farmer=farmer1
    )
    property_2 = dict(
        name='Property 2', city='Cidade B', state='Estado Y',
        total_area=total_area_2, arable_area=total_area_2 / 2, vegetation_area=total_area_2 / 2,
        farmer=farmer2
    )

    prop_1 = Property.objects.create(**property_1)
    prop_2 = Property.objects.create(**property_2)

    harvest_1 = Harvest.objects.create(year=2022)
    harvest_2 = Harvest.objects.create(year=2023)

    crop_1 = CultivatedCrop.objects.create(name='Crop 1', harvest=harvest_1)
    crop_2 = CultivatedCrop.objects.create(name='Crop 1', harvest=harvest_2)
    crop_3 = CultivatedCrop.objects.create(name='Crop 2', harvest=harvest_1)
    crop_4 = CultivatedCrop.objects.create(name='Crop 2', harvest=harvest_2)

    CropInProperty.objects.create(cultivated_crop=crop_1, property=prop_1)
    CropInProperty.objects.create(cultivated_crop=crop_2, property=prop_1)
    CropInProperty.objects.create(cultivated_crop=crop_3, property=prop_2)
    CropInProperty.objects.create(cultivated_crop=crop_3, property=prop_2)
    CropInProperty.objects.create(cultivated_crop=crop_4, property=prop_1)
    return None


@pytest.mark.django_db
def test_dashboard_api(api_client, dashboard_data):
    response = api_client.get('/api/dashboard')
    data = response.json()

    assert response.status_code == 200
    assert 'total_farms' in data
    assert data['total_farms'] == 2
    assert 'total_area' in data
    assert data['total_area'] == 1500.0
    assert 'areas_by_state' in data
    assert data['areas_by_state'] == [
        {'arable_area': '250.00', 'vegetation_area': '250.00', 'state': 'Estado Y', 'total': '500.00'},
        {'arable_area': '500.00', 'vegetation_area': '500.00', 'state': 'Estado X', 'total': '1000.00'}
    ]
    assert 'properties_by_state' in data
    assert data['properties_by_state'] == [
        {'total': 1, 'state': 'Estado X'}, {'total': 1, 'state': 'Estado Y'}
    ]
    assert 'total_areas_by_land_usage' in data
    assert data['total_areas_by_land_usage'] == {'arable_area': '750.00', 'vegetation_area': '750.00'}
    assert 'top_cultivated_crops' in data
    assert data['top_cultivated_crops'] == [
        {'name': 'Crop 2', 'total_farms': 2}, {'name': 'Crop 2', 'total_farms': 1},
        {'name': 'Crop 1', 'total_farms': 1}, {'name': 'Crop 1', 'total_farms': 1}
    ]


@pytest.mark.django_db
def test_add_property_dashboard(api_client, dashboard_data):
    farmer_3 = dict(name='Farmer Three', document='0987654321')
    farmer3 = Farmer.objects.create(**farmer_3)
    Property.objects.create(
        name="Property 3", city='Cidade A', state='Estado X',
        total_area=100, arable_area=80, vegetation_area=20,
        farmer=farmer3
    )

    response = api_client.get('/api/dashboard')
    data = response.json()

    assert response.status_code == 200
    assert 'total_farms' in data
    assert data['total_farms'] == 3
    assert 'total_area' in data
    assert data['total_area'] == 1600.0
