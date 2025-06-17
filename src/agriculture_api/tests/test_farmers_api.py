import pytest

from rest_framework.test import APIClient

from agriculture_api.models import Farmer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_farmer(api_client):
    document = '50973944021'
    data = {
        'name': 'João Silva',
        'document': document,
    }
    response = api_client.post('/api/farmers/', data, format='json')
    assert response.status_code == 201
    assert Farmer.objects.filter(document=document).exists()


@pytest.mark.django_db
def test_list_farmers(api_client):
    documents = ['50973944021', '90718763068']
    Farmer.objects.create(name='Maria Lima', document=documents[0])
    Farmer.objects.create(name='Lucas Souza', document=documents[1])

    response = api_client.get('/api/farmers/')
    assert response.status_code == 200
    assert len(response.data) == 2
    documents = [farmers['document'] for farmers in response.data]
    assert sorted(documents) == sorted(documents)


@pytest.mark.django_db
def test_retrieve_farmers(api_client):
    document = '50973944021'
    farmer = Farmer.objects.create(name='Maria Lima', document=document)
    response = api_client.get(f'/api/farmers/{farmer.pk}/')
    assert response.status_code == 200
    assert document == response.data['document'] == farmer.document


@pytest.mark.django_db
def test_update_farmers(api_client):
    document = '50973944021'
    farmer = Farmer.objects.create(name='Mara Lima', document=document)
    assert farmer.name == 'Mara Lima'
    data = {
        'name': 'Maria Lima',
    }
    response = api_client.patch(f'/api/farmers/{farmer.pk}/', data, format='json')

    assert response.status_code == 200
    farmer.refresh_from_db()
    assert farmer.name == 'Maria Lima'


@pytest.mark.django_db
def test_delete_farmers(api_client):
    document = '50973944021'
    farmer = Farmer.objects.create(name='Maria Lima', document=document)
    response = api_client.delete(f'/api/farmers/{farmer.pk}/')
    assert response.status_code == 204
    with pytest.raises(Farmer.DoesNotExist):
        Farmer.objects.get(pk=farmer.pk)
