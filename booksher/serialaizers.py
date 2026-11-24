from rest_framework import serializers
from .models import Category, City, Book, Trade, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category', write_only=True)
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(),source='city',write_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'is_exchanged']

class TradeSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    getter = serializers.StringRelatedField(read_only=True)
    requested_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    offered_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ['sender', 'getter', 'treade_at']

    def validate(self, data):
        requested = data['requested_book']
        offered = data['offered_book']
        user = self.context['request'].user

        if requested.owner == user:
            raise serializers.ValidationError('Шумо наметавонед китоби худро интихоб кунед!')

        if offered.owner != user:
            raise serializers.ValidationError('Китоби пешниҳодшуда ба шумо тааллуқ надорад!')

        if requested.is_exchanged or offered.is_exchanged:
            raise serializers.ValidationError('Яке аз китобҳо аллакай мубодила шудааст!')

        if Trade.objects.filter(requested_book=requested,offered_book=offered,status='pending').exists():
            raise serializers.ValidationError('Ин дархост аллакай вуҷуд дорад!')

        return data

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        validated_data['getter'] = validated_data['requested_book'].owner
        validated_data['status'] = 'pending'

        return Trade.objects.create(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Рейтинг бояд аз 1 то 5 бошад!'
            )
        return value

    def validate(self, data):
        trade = data['trade']
        user = self.context['request'].user

        if trade.status != 'accepted':
            raise serializers.ValidationError('Барои ин мубодила ҳанӯз отзыв гузоштан мумкин нест!')

        if user not in [trade.sender, trade.getter]:
            raise serializers.ValidationError('Шумо иштирокчии ин мубодила нестед!')

        if user == data['reviewed_user']:
            raise serializers.ValidationError('Шумо наметавонед ба худатон отзыв гузоред!')
        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return Review.objects.create(**validated_data)
