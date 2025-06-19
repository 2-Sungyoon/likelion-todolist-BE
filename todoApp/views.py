from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer

# Create your views here.
class Todos(APIView):
    #userid까지 받으니 유저 가져오는게 중요, 유저쪽에 이미 구현해놓음, 하는일은 다르다다

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    #투두리스트 조회
    def get(self, request, user_id):

        #유저 가져오기
        user = self.get_user(user_id)

        #기본적으로 전체 todo 리스트 조회
        todos = Todo.objects.filter(user=user)

        # 쿼리 파라미터에서 month, day 가져오기
        month = request.query_params.get("month")
        day = request.query_params.get("day")

        # month, day 가 둘 다 제공된 경우만 필터링 해주기
        if month is not None and day is not None:
            try:
                month = int(month)
                day = int(day)
                todos = todos.filter(date__month=month, date__day=day)
            except ValueError:
                raise ParseError("month와 day는 정수여야 합니다.")
            

        #정렬 및 추가 필터링을 위한 sort_by 파라미터 가져오기
        sort_by = request.query_params.get('sort_by', 'created_at')
        if sort_by not in ['created_at', 'updated_at']:
            sort_by = 'created_at'

        # 보낼 데이터들 직렬화
        serializer = TodoSerializer(todos, many=True)   
        return Response(serializer.data)