from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import NoteSerializer
from rest_framework import status
from django.db.models import F

#Signup process
@csrf_exempt
def signup(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]

    usernames = list(User.objects.values_list('username', flat=True))
    if username in usernames:
        return JsonResponse({"status" : 400, "error": "Username is already taken by others!"})
    if len(password)>4:
        if len(username)>4:
            userdata = User(username=username)
            userdata.set_password(password)
            userdata.save()
            return JsonResponse({"status" : 200, "data": "Account Created Succesfully!"})
        else:
            return JsonResponse({"status" : 400, "error": "Username can't be less than 4 characters"})
    else:
        return JsonResponse({"status" : 400, "error": "Password length must be more than 4 characters"})

def get_user_token(user):
    token_instance,  created = Token.objects.get_or_create(user=user)
    return token_instance.key

#Login Process
@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    username = request.POST["username"]
    password = request.POST["password"]
    try:
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({ "status" : 400, "error": "There is no account with this email!"})
        if( user.check_password(password)):
            usr_dict = User.objects.filter(username=username).values().first()
            usr_dict.pop("password")
            if user != request.user:
                login(request, user)
                token = get_user_token(user)
                return JsonResponse({"status" : 200,"token": token,"status":"Logged in"})
            else:
                return JsonResponse({"status":200,"message":"User already logged in!"})
        else:
            return JsonResponse({"status":400,"message":"Invalid Login!"})
    except Exception as e:
        return JsonResponse({"status":500,"message":"Something went wrong!"})

#Logout process
@csrf_exempt   
def signout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return JsonResponse({ "status" : 200, "success" : "logout successful"})
    except Exception as e:
        return JsonResponse({ "status" : 400, "error": "Something Went wrong! Please try again later."})

#Welcome View
class HelloView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello!'}
        return Response(content)
    
#Notes Sharing Api    
class NotesShareView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        if 'nid' in request.data:
            nid = request.POST['nid']
        note = Notes.objects.filter(id=int(nid)).first()
        if note:
            if note.owner == user:
                try:
                    if 'shared_with' in request.data:
                        shared_with = request.POST['shared_with']
                        try:
                            users = User.objects.filter(id__in=list(shared_with)).all()
                            print(users)
                        except Exception as e:
                            content["message"] = "Problem with user ids"
                            return Response(content, status=status.HTTP_404_NOT_FOUND)
                        note.shared.add(*users)
                        content = {}
                        content["message"] = "Note Shared successfully."
                        return Response(content, status=status.HTTP_201_CREATED)
                    else:
                        content = {"Message": "Send Request with Valid Parameters only!"}
                        return Response(content,status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    content = {"Message": "Something Went Wrong!"}
                    return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {"Message": "Access Denied!"}
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            content = {"Message": "Resouce doesn't Exist!"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

#Notes Crud API    
class NotesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        serializer = NoteSerializer(data=request.data)
        try:
            if serializer.is_valid():
                instance = serializer.save(owner=user)
                NotesVersionHistory.objects.create(notes=instance,created_by=user,created=True)
                content = {"Message": "Success"}
                serializer_dict = serializer.data
                serializer_dict["message"] = "Note Created successfully."
                return Response(serializer_dict, status=status.HTTP_201_CREATED)
            else:
                content = {"Message": "Failed"}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {"Message": "Something Went Wrong!"}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,nid):
        user = request.user
        note = Notes.objects.filter(id=nid).first()
        if note:
            if note.owner == user or note.shared== user:
                try:
                    serializer = NoteSerializer(note)
                    serializer_dict = serializer.data
                    serializer_dict["message"] = "Note Fetched successfully."
                    return Response(serializer_dict, status=status.HTTP_200_OK)
                except Exception as e:
                    content = {"Message": "Something Went Wrong!"}
                    return Response(content ,status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {"Message": "Access Denied!"}
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            content = {"Message": "Resource Not Found!"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,nid):
        user = request.user
        note = Notes.objects.filter(id=nid).first()
        if note.owner == user or note.shared== user:
            try:
                Notes.objects.filter(id=nid).delete()
                content={'Message': 'Note Deleted!'}
                return Response(content,status=status.HTTP_200_OK)
            except Exception as e:
                content={'Message': 'Something Went Wrong!'}
                return Response(content ,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,nid):
        user = request.user
        note = Notes.objects.filter(id=nid).first()
        if note.owner == user or note.shared == user:
            try:
                shared_with = ''
                text = request.POST['text']
                if 'shared_with' in request.data:
                    shared_with = request.POST['shared_with']
                note.text = text
                if shared_with:
                    sw = list(shared_with)
                    try:
                        users = User.objects.filter(id__in=sw).all()
                        print(users)
                    except Exception as e:
                        content["message"] = "Problem with user ids"
                        return Response(content, status=status.HTTP_404_NOT_FOUND)
                    note.shared.add(*users)
                note.save()
                NotesVersionHistory.objects.create(notes=note,updated_by=user,updated=True)
                content = {}
                content["message"] = "Note updated successfully."
                return Response(content, status=status.HTTP_200_OK)
            except Exception as e:
                content = {"Message": "Failed"}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
            
#Notes Version History Get API
class NotesVHView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,nid):
        user = request.user
        note = Notes.objects.filter(id=nid).first()
        if note:
            if note.owner == user or note.shared== user:
                try:
                    notevh = NotesVersionHistory.objects.filter(notes=note).annotate(created_user=F('created_by__username'),updated_user=F('updated_by__username'),note_text=F('notes__text')).values('note_text','created_user','updated_user','action_time','created','updated')
                    print(notevh)
                    content = {}
                    content["message"] = "NoteVH Fetched successfully."
                    content["data"] = notevh
                    return Response(content, status=status.HTTP_200_OK)
                except Exception as e:
                    content = {"Message": "Something Went Wrong!"}
                    return Response(str(e) ,status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {"Message": "Access Denied!"}
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            content = {"Message": "Resource Not Found!"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
