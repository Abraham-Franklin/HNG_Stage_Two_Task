from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Organisation
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        if User.objects.filter(email=data.get("email")).exists():
            return Response({"errors": [{"field": "email", "message": "Email already exists"}]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user = User.objects.create(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            email = data.get("email"),
            password = data.get("password"),
            phone = data.get("phone")
        )
        user.set_password(data.get("password"))  # Hash the password
        user.save()
        org = Organisation.objects.create(
            org_id = str(uuid.uuid4()),
            name = f"{user.first_name}'s Organisation"
        )
        org.users.add(user)
        org.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": {
                        "userId": user.user_id,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(refresh.access_token),
                "user": {
                    "userId": user.user_id,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }, status=status.HTTP_200_OK)



class UserDetailView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(user_id=id)
        except User.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "User not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response({
            "status": "success",
            "message": "User details retrieved",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserOrganisationsView(APIView):
    def get(self, request):
        user = request.user
        organisations = user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved",
            "data": {
                "organisations": serializer.data
            }
        }, status=status.HTTP_200_OK)


class OrganisationDetailView(APIView):
    def get(self, request, orgId):
        try:
            organisation = Organisation.objects.get(org_id=orgId)
        except Organisation.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "Organisation not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation details retrieved",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class CreateOrganisationView(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        print(organisation, "THIS IS IT")
        
        organisation = Organisation.objects.create(
            org_id=str(uuid.uuid4()),
            name=data.get('name'),
            description=data.get('description')
        )
        organisation.users.add(user)
        organisation.save()

        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class AddUserToOrganisationView(APIView):
    def post(self, request, orgId):
        data = request.data
        try:
            organisation = Organisation.objects.get(org_id=orgId)
        except Organisation.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "Organisation not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = User.objects.get(user_id=data.get('userId'))
        except User.DoesNotExist:
            return Response({
                "status": "Bad request",
                "message": "User not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully"
        }, status=status.HTTP_200_OK)