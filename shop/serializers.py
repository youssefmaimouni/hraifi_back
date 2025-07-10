from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Region, Artisan, Product, ContactMessage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Region
        fields = ['id', 'name']

class ArtisanSerializer(serializers.ModelSerializer):
    region     = RegionSerializer(read_only=True)
    region_id  = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(),
                                                    source='region',
                                                    write_only=True,
                                                    allow_null=True)
    main_image = serializers.ImageField(required=False, allow_null=True)
    # expose new email field
    email      = serializers.EmailField()
    phone      = serializers.CharField(required=True)

    class Meta:
        model  = Artisan
        fields = ['id', 'name', 'email', 'phone', 'biography',
                  'region', 'region_id', 'main_image']

class ProductSerializer(serializers.ModelSerializer):
    category   = CategorySerializer(read_only=True)
    category_id= serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),
                                                    source='category',
                                                    write_only=True)
    region     = RegionSerializer(read_only=True)
    region_id  = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(),
                                                    source='region',
                                                    write_only=True)
    artisan    = ArtisanSerializer(read_only=True)
    artisan_id = serializers.PrimaryKeyRelatedField(queryset=Artisan.objects.all(),
                                                    source='artisan',
                                                    write_only=True,
                                                    allow_null=True)
    main_image = serializers.ImageField(required=False, allow_null=True)
    price      = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model  = Product
        fields = [
            'id','name','description','materials','dimensions',
            'cultural_significance',
            'category','category_id',
            'region','region_id',
            'artisan','artisan_id',
            'main_image','price',
        ]

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'submitted_at']
        read_only_fields = ['submitted_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            artisan = self.user.artisan_profile  # ✅ Use correct related_name
            data['artisan'] = ArtisanSerializer(artisan).data
        except Artisan.DoesNotExist:
            data['artisan'] = None

        return data
        fields = ['id','name','email','message','submitted_at']
        read_only_fields = ['submitted_at']

class ArtisanRegistrationSerializer(serializers.ModelSerializer):
    username    = serializers.CharField(write_only=True)
    password    = serializers.CharField(write_only=True, min_length=8)
    region_id   = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(),
                                                     source='region',
                                                     write_only=True,
                                                     allow_null=True)
    main_image  = serializers.ImageField(required=False, allow_null=True)
    email       = serializers.EmailField(write_only=True)
    phone       = serializers.CharField(required=True, write_only=True)

    class Meta:
        model  = Artisan
        fields = ['username','password','name','email','phone','biography','region_id','main_image']

    def create(self, validated_data):
        # extract user fields
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email    = validated_data.pop('email')
        phone    = validated_data.pop('phone')
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        # create artisan
        artisan = Artisan.objects.create(user=user, email=email, phone=phone, **validated_data)
        return artisan
