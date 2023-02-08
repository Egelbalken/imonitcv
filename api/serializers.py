from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

# Add the models to serialize to json. This is accually like the form.py implementations.
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# reach objects that are many to many fields.
class ProjectSerializers(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # A method in a serializer object always starts with a  get_
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializers(reviews, many=True)
        return serializer.data
