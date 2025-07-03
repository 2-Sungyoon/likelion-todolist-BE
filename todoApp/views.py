from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer
from rest_framework import status
from datetime import datetime, timedelta

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
        todos = Todo.objects.filter(user=user)   #   .order_by(sort_by)

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
    
    #투두작성 추가 - post
    def post(self, request, user_id):
        user = self.get_user(user_id)

        # date와 content를 요청에서 추출
        date = request.data.get('date')
        content = request.data.get('content')

        # 둘 중 하나라도 빠지면 400 에러
        if not date or not content:
            raise ParseError("date와 content는 필수 입력 항목입니다.")

        # 새로운 Todo 객체 생성 및 저장
        todo = Todo.objects.create(
            user=user,
            date=date,
            content=content
        )

        # 직렬화 및 반환
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 투두수정 추가 - 엔드포인트가 달라지므로 new class 추가
class TodoDetail(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")

    def get_todo(self, user, todo_id):
        try:
            return Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)

        date = request.data.get('date')
        content = request.data.get('content')

        if date:
            todo.date = date
        if content:
            todo.content = content

        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #투두삭제 추가
    def delete(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)

        todo.delete()
        return Response({"detail": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
    
#투두완료 - check class 추가
class TodoCheck(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")

    def get_todo(self, user, todo_id):
        try:
            return Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)

        is_checked = request.data.get('is_checked')

        if is_checked is None:
            raise ParseError("is_checked 값을 입력해 주세요.")

        if not isinstance(is_checked, bool):
            raise ParseError("is_checked는 true 또는 false여야 합니다.")

        todo.is_checked = is_checked
        todo.save()

        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#투두리뷰 -review class 추가
class TodoReview(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")

    def get_todo(self, user, todo_id):
        try:
            return Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)

        emoji = request.data.get('emoji')
        if not emoji:
            raise ParseError("emoji 값을 입력해 주세요.")

        todo.emoji = emoji
        todo.save()

        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#반복일정 등록
class RecurringTodoCreate(APIView):
    def post(self, request, user_id):
        title = request.data.get('title')
        day_of_week = request.data.get('day_of_week')  # 예: "Tuesday"
        weeks = int(request.data.get('weeks', 4))  # 몇 주 반복할지 (기본 4주)
        start_date_str = request.data.get('start_date')  # 시작 날짜 (예: '2025-07-02')

        if not all([title, day_of_week, start_date_str]):
            return Response({"error": "title, day_of_week, start_date를 모두 입력하세요."}, status=400)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day_of_week)

        created = []
        for i in range(weeks):
            next_date = start_date + timedelta(weeks=i)
            while next_date.weekday() != day_index:
                next_date += timedelta(days=1)

            todo = Todo.objects.create(
                user_id=user_id,
                title=title,
                due_date=next_date,
                is_completed=False
            )
            created.append(todo.id)

        return Response({"message": f"{len(created)}개의 반복 일정이 생성되었습니다.", "ids": created}, status=201)


#투두 순서 변경 (드래그 앤 드롭)
class TodoReorder(APIView):
    def patch(self, request, user_id):
        new_order = request.data.get('order')  # 예: [3, 1, 2]
        if not isinstance(new_order, list):
            return Response({"error": "order는 리스트 형태여야 합니다."}, status=400)

        for idx, todo_id in enumerate(new_order):
            try:
                todo = Todo.objects.get(id=todo_id, user_id=user_id)
                todo.order = idx
                todo.save()
            except Todo.DoesNotExist:
                return Response({"error": f"ID {todo_id}에 해당하는 투두가 없습니다."}, status=404)

        return Response({"message": "순서가 성공적으로 변경되었습니다."}, status=200)