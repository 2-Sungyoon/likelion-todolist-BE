from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User   # models라고 적어놓긴 함
        fields = "__all__"
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'required': '이 필드는 필수 항목입니다.',
                    'unique': 'user의 username은/는 이미 존재합니다.'
                }
            },
            'password': {
                'error_messages': {
                    'required': '이 필드는 필수 항목입니다.'
                }
            }
        }