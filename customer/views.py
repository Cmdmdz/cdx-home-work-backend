from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CustomerSerializer, CourseSerializer, HomeWorkSerializer, WorkApproveSerializer
from .models import Customer, Course, HomeWork, WorkApprove
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from rest_framework.generics import ListAPIView
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            raise AuthenticationFailed('User not found!')

        if not customer.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        access_token = create_access_token(customer.id)

        status = customer.status

        refresh_token = create_refresh_token(customer.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
            'status': status
        }
        return response


class CustomerView(APIView):

    def get(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            customer = Customer.objects.filter(pk=id).first()

            return Response(CustomerSerializer(customer).data)

        raise AuthenticationFailed('unauthenticated')


class CustomerListView(APIView):

    def get(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if auth and len(auth) == 2:
            customer = Customer.objects.filter(status=1).all()
            return Response(CustomerSerializer(customer,many=True).data)
        raise AuthenticationFailed('unauthenticated')


class CustomerById(APIView):

    def get(self, request,pk):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            worked = HomeWork.objects.filter(
                customer_id=pk).select_related('course').select_related(
                'course__customer').select_related('status_work').values('title', 'course__course', 'deadline',
                                                                         'course__customer__first_name',
                                                                         'course__customer__last_name',
                                                                         'course__customer__status', 'course',
                                                                         'status_work__approve', 'status_work', 'id')

            return Response(worked)
        raise AuthenticationFailed('unauthenticated')


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message': 'success'
        }
        return response


class CourseView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            course = Course.objects.all().select_related('customer').values('customer__first_name',
                                                                            'customer__last_name', 'course', 'id')
            print(course.query)
            return Response(course)
        raise AuthenticationFailed('unauthenticated')

    def post(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            data = {
                'course': request.data.get('course'),
                'customer': id
            }

            serializer = CourseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

    def put(self, request, pk):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            course = Course.objects.get(id=pk)
            data = {
                'course': request.data.get('course'),
                'customer': id
            }
            serializer = CourseSerializer(course, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

    def delete(self, request, pk):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:

            worked = HomeWork.objects.select_related('course').filter(course_id=pk).values('course_id').first()
            course = Course.objects.get(id=worked.course_id)
            HomeWork.delete(worked)
            Course.delete(course,)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise AuthenticationFailed('unauthenticated')


class HomeWorkView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            worked = HomeWork.objects.filter(customer__status='1').filter(
                customer_id=id).select_related('course').select_related(
                'course__customer').select_related('status_work').values('title', 'course__course', 'deadline',
                                                                         'course__customer__first_name',
                                                                         'course__customer__last_name',
                                                                         'course__customer__status', 'course',
                                                                         'status_work__approve', 'status_work', 'id')
            print(worked.query)
            print(id)
            return Response(worked)
        raise AuthenticationFailed('unauthenticated')

    def post(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            data = {
                'title': request.data.get('title'),
                'deadline': request.data.get('deadline'),
                'course': request.data.get('course'),
                'status_work': request.data.get('status_work'),
                'customer': id,
            }

            serializer = HomeWorkSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

    def put(self, request, pk):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            idv = decode_access_token(token)
            worked = HomeWork.objects.get(id=pk)
            data = {
                'title': request.data.get('title'),
                'deadline': request.data.get('deadline'),
                'course': request.data.get('course'),
                'status_work': request.data.get('status_work'),
                'customer': idv,
            }
            serializer = HomeWorkSerializer(worked, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

    def delete(self, request, pk):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            worked = HomeWork.objects.get(id=pk)
            HomeWork.delete(worked)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise AuthenticationFailed('unauthenticated')


class ApproveView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        if auth and len(auth) == 2:
            worked = WorkApprove.objects.all()

            return Response(WorkApproveSerializer(worked, many=True).data)

        raise AuthenticationFailed('unauthenticated')
