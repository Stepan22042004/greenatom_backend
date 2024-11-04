from rest_framework import serializers
from organisations.models import (Organisation,
                                  Storage, Capacity, StorageCapacity,
                                  OrganisationCapacity, OrganisationStorage,
                                  User)
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404


class UserSerializer(serializers.ModelSerializer):
    organisations = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'organisations',
        )


class PutOrganisationSerializer(serializers.ModelSerializer):
    organisations = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        many=True
    )

    class Meta:
        model = User
        fields = ('organisations', )

    def update(self, instance, data):
        organisations = data.get('organisations')
        instance.organisations.clear()
        for organisation in organisations:
            instance.organisations.add(organisation)

        return instance


class StorageCapacitySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='capacity',
        queryset=Capacity.objects.all(),
    )
    material = serializers.ReadOnlyField(
        source='capacity.material'
    )

    class Meta:
        model = StorageCapacity
        fields = ('id', 'amount', 'max_volume', 'material')


class OrganisationCapacitySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='capacity',
        queryset=Capacity.objects.all(),
    )
    material = serializers.ReadOnlyField(
        source='capacity.material'
    )

    class Meta:
        model = OrganisationCapacity
        fields = ('id', 'amount', 'max_volume', 'material')


class OrganisationStorageSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='storage',
        queryset=Storage.objects.all(),
    )
    name = serializers.ReadOnlyField(
        source='storage.name'
    )

    class Meta:
        model = OrganisationStorage
        fields = ('id', 'distance', 'name')


class ShowStorageSerializer(serializers.ModelSerializer):
    capacities = StorageCapacitySerializer(
        source='capacities_storage',
        many=True,
        read_only=True
    )

    class Meta:
        model = Storage
        fields = '__all__'


class ShowOrganisationSerializer(serializers.ModelSerializer):
    capacities = StorageCapacitySerializer(
        source='capacities_organisation',
        many=True,
        read_only=True
    )
    storages = OrganisationStorageSerializer(
        source='storages_organisation',
        many=True,
        read_only=True
    )

    class Meta:
        model = Organisation
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    capacities = StorageCapacitySerializer(many=True, required=True)

    class Meta:
        model = Storage
        fields = '__all__'

    def validate(self, data):
        capacities = data.get('capacities')
        list_of_capacities_materials = []

        for i in range(len(capacities)):
            list_of_capacities_materials.append(capacities[i]['capacity'])

        if (len(list_of_capacities_materials) !=
           len(set(list_of_capacities_materials))):
            raise ValidationError('Одинаковые материалы у capacity')

        for item in capacities:
            if item.get('amount') is None:
                raise ValidationError('Нет кол-ва хранимых отходов')

            if item.get('max_volume') is None:
                raise ValidationError('Нет объема хранилища')

            if item['max_volume'] < 0 or item['amount'] < 0:
                raise ValidationError('Кол-во меньше нуля')

            if item['max_volume'] < item['amount']:
                raise ValidationError('Хранится больше, чем может вместить')

        return data

    def create(self, validated_data):
        capacities = validated_data.get('capacities')
        name = validated_data.get('name')
        storage = Storage.objects.create(name=name)
        for capacity in capacities:
            StorageCapacity.objects.create(
                amount=capacity['amount'],
                storage=storage,
                capacity=capacity['capacity'],
                max_volume=capacity['max_volume']
            )
        return storage

    def update(self, instance, validated_data):
        capacities = validated_data.pop('capacities')
        super().update(instance, validated_data)
        instance.capacities.clear()
        for capacity in capacities:
            StorageCapacity.objects.create(
                amount=capacity['amount'],
                storage=instance,
                capacity=capacity['capacity'],
                max_volume=capacity['max_volume']
            )
        return instance

    def to_representation(self, instance):
        return ShowStorageSerializer(instance, context=self.context).data


class OrganisationSerializer(serializers.ModelSerializer):
    capacities = OrganisationCapacitySerializer(many=True, required=True)
    storages = OrganisationStorageSerializer(many=True)

    class Meta:
        model = Organisation
        fields = ('name', 'capacities', 'storages')

    def validate(self, data):
        capacities = data.get('capacities')
        list_of_capacities_materials = []

        for i in range(len(capacities)):
            list_of_capacities_materials.append(capacities[i]['capacity'])

        if (len(list_of_capacities_materials) !=
           len(set(list_of_capacities_materials))):
            raise ValidationError('Одинаковые материалы у capacity')

        for item in capacities:
            if item.get('amount') is None:
                raise ValidationError('Нет кол-ва хранимых отходов')

            if item.get('max_volume') is None:
                raise ValidationError('Нет объема хранилища')

            if item['max_volume'] < 0 or item['amount'] < 0:
                raise ValidationError('Кол-во меньше нуля')

            if item['max_volume'] < item['amount']:

                raise ValidationError('Хранится больше, чем может вместить')

        return data

    def create(self, validated_data):
        capacities = validated_data.get('capacities')
        storages = validated_data.get('storages')
        name = validated_data.get('name')
        organisation = Organisation.objects.create(name=name)
        for capacity in capacities:
            OrganisationCapacity.objects.create(
                amount=capacity['amount'],
                organisation=organisation,
                capacity=capacity['capacity'],
                max_volume=capacity['max_volume']
            )
        for storage in storages:
            OrganisationStorage.objects.create(
                organisation=organisation,
                storage=storage['storage'],
                distance=storage['distance']
            )
        return organisation

    def update(self, instance, validated_data):
        capacities = validated_data.pop('capacities')
        storages = validated_data.pop('storages')
        super().update(instance, validated_data)
        instance.capacities.clear()
        instance.storages.clear()
        for capacity in capacities:
            OrganisationCapacity.objects.create(
                amount=capacity['amount'],
                organisation=instance,
                capacity=capacity['capacity'],
                max_volume=capacity['max_volume']
            )

        for storage in storages:
            OrganisationStorage.objects.create(
                organisation=instance,
                storage=storage['storage'],
                distance=storage['distance']
            )
        return instance

    def to_representation(self, instance):
        return ShowOrganisationSerializer(instance, context=self.context).data


class DistanceSerializer(serializers.ModelSerializer):
    storages = OrganisationStorageSerializer(many=True)

    class Meta:
        model = Organisation
        fields = ('storages',)

    def validate(self, data):
        storages = data.get('storages')
        for storage in storages:
            if storage['distance'] < 0:
                raise ValidationError('Расстояние меньше нуля')
        return data

    def update(self, instance, validated_data):
        storages = validated_data.get('storages')
        for storage in storages:
            obj = get_object_or_404(
                OrganisationStorage,
                organisation=instance,
                storage=storage['storage'],
            )
            obj.distance = storage['distance']
            obj.save()
        return instance

    def to_representation(self, instance):
        return ShowOrganisationSerializer(instance, context=self.context).data


class GenerateSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(
        slug_field='material',
        queryset=Capacity.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = Organisation
        fields = ('material', 'amount')

    def validate(self, data):
        capacity = data.get('material')
        amount = data.get('amount')
        obj = get_object_or_404(
            OrganisationCapacity,
            capacity=capacity,
            organisation=self.instance
        )

        if amount < 0:
            raise ValidationError('Генерируется отрицательное кол-во')

        if obj.max_volume < obj.amount + amount:
            raise ValidationError('Не помещается')

        return data

    def update(self, instance, validated_data):
        amount = validated_data.get('amount')
        capacity = validated_data.get('material')
        obj = get_object_or_404(
            OrganisationCapacity,
            organisation=instance,
            capacity=capacity,
        )
        obj.amount += amount
        obj.save()
        return instance

    def to_representation(self, instance):
        return ShowOrganisationSerializer(instance, context=self.context).data


class UtilizeSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(
        slug_field='material',
        queryset=Capacity.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = Organisation
        fields = ('material', 'amount')

    def validate(self, data):
        amount = data.get('amount')
        capacity = data.get('material')
        obj_1 = get_object_or_404(
            OrganisationCapacity,
            organisation=self.instance,
            capacity=capacity,
        )

        organisation_storage = get_list_or_404(
            OrganisationStorage.objects.all().order_by('distance'),
            organisation=self.instance,
            storage__capacities_storage__capacity=capacity,
        )

        if amount < 0:
            raise ValidationError('Отрицательное кол-во')
        if amount > obj_1.amount:
            raise ValidationError('Нельзя утилизировать больше, чем хранится')

        for item in organisation_storage:
            storage_capacity = get_object_or_404(
                StorageCapacity,
                capacity=capacity,
                storage=item.storage
            )
            delta = storage_capacity.max_volume - storage_capacity.amount

        if amount > delta:
            raise ValidationError('Такое кол-во не влезает в хранилища')

        return data

    def update(self, instance, validated_data):
        amount = validated_data.get('amount')
        capacity = validated_data.get('material')
        organisation_capacity = get_object_or_404(
            OrganisationCapacity,
            organisation=instance,
            capacity=capacity,
        )

        organisation_storage = get_list_or_404(
            OrganisationStorage.objects.all().order_by('distance'),
            organisation=instance,
            storage__capacities_storage__capacity=capacity,
        )

        for item in organisation_storage:
            storage_capacity = get_object_or_404(
                StorageCapacity,
                capacity=capacity,
                storage=item.storage
            )
            delta = storage_capacity.max_volume - storage_capacity.amount
            if delta != 0 and amount <= delta:
                storage_capacity.amount += amount
                organisation_capacity.amount -= amount
                organisation_capacity.save()
                storage_capacity.save()
                amount -= delta
                if amount < 0:
                    amount = 0
                break
            elif delta != 0:
                storage_capacity.amount += delta
                organisation_capacity.amount -= delta
                amount -= delta
                organisation_capacity.save()
                storage_capacity.save()
        return instance

    def to_representation(self, instance):
        return ShowOrganisationSerializer(instance, context=self.context).data


class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacity
        fields = ('id', 'material',)
