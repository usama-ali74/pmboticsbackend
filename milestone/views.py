import base64
from fyp_management.permission import IsFYPPanel, IsStudent, IsSupervisor
from rest_framework.views import APIView
from milestone.serializers import milestoneSerializer, milestoneworkSerializer, milestonemarkSerializer
from core.models import milestone, project, supervisor
from rest_framework.response import Response
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from datetime import datetime, date
from fyp_management.settings import imagekit
from milestone.models import MilestoneWork
from core.models import milestone
from core.models import milestone, project, supervisor, teamMember, User
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .models import Milestonemarks
from rest_framework.exceptions import ValidationError
from sprint.models import Sprint

# # Create your views here.
class createmilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def post(self, request):
        try:
            serialize = milestoneSerializer(data=request.data)
            if serialize.is_valid():
                milestone_obj = serialize.save()
                projects = project.objects.filter(status="ongoing", deleted_at=None, department=request.user.department)
                for p in projects:
                    p.milestone.add(milestone_obj)
                return Response(
                    {
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
            else:
                return Response(
                    {
                    "status": 422,
                    "message": serialize.errors,
                    "body": {},
                    "exception": "some exception"
                    }
                )
        except Exception as e:
          return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class allmilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def get(self, request):
        try:
            mil = milestone.objects.filter(department=request.user.department, deleted_at=None)
            serialize = milestoneSerializer(mil, many=True) #, many=True   
            return Response(
                    {
                        "data":serialize.data,
                        "status": 200,
                        "message": "Success",
                        "body": {},
                        "exception": None 
                        }
                    )
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class updatemilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def patch(self, request):
        try:
            sup = milestone.objects.get(id=request.data.get("id"), deleted_at=None)
            serialize = milestoneSerializer(sup,data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(       
                    {
                    "data": serialize.data,
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None 
                    }
                )
            else:
                return Response(
                    {
                    "status": 422,
                    "message": serialize.errors,
                    "body": {},
                    "exception": "some exception" 
                    }
                )    
        except Exception as e:
            return Response(       
                {
                "status": 404,
                "message": "Some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class deletemilestoneAPI(APIView):
    permission_classes = [IsAuthenticated & IsFYPPanel]
    def delete(self, request, pk):
        try:
            my_object = milestone.objects.get(pk=pk, deleted_at=None)
            sprint = Sprint.objects.filter(milestone=my_object, deleted_at=None).count()
            if sprint == 0:
                my_object.deleted_at = timezone.now()
                my_object.save()
                return Response(
                    {
                    "status": 200,
                    "message": "Successfuly deleted",
                    "body": {},
                    "exception": None 
                    }
                )
            else:
                return Response(
                {
                "status": 403,
                "message": f"Milestone can not be deleted as there are sprints present in this milestone",
                "body": {},
                "exception": None 
                }
            )
        except Exception as e:
            return Response(       
                    {
                    "status": 404,
                    "message": "some exception",
                    "body": {},
                    "exception": str(e) 
                    }
                )


class GetAllMilestones(APIView):
    permission_classes = [IsAuthenticated & (IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            if request.user.role == User.SUPERVISOR:
                sup = supervisor.objects.get(user=request.user, deleted_at=None)
                projects = project.objects.filter(supervisor=sup)
                if len(projects) != 0:
                    milestones = milestone.objects.filter(project=projects[0], deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                        }
                    )
                else:
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": [],
                        "exception": None
                        }
                    )
            elif request.user.role == User.STUDENT:
                tm = teamMember.objects.get(user=request.user, deleted_at=None)
                pro = tm.project
                if pro != None:
                    milestones = milestone.objects.filter(project=pro, deleted_at=None)
                    serializer = milestoneSerializer(milestones, many=True)
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": serializer.data,
                        "exception": None
                        }
                    )
                else:
                    return Response({
                        "status": 200,
                        "message": "Success",
                        "body": [],
                        "exception": None
                        }
                    )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )
        

class SubmissionView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            milestone_work = MilestoneWork.objects.filter(project=project.objects.get(id=request.GET.get("pro_id"), deleted_at=None))
            serialize = milestoneworkSerializer(milestone_work, many=True)
            return Response({
                "status": 200,
                "message": "Success",
                "body": serialize.data,#[response]
                "exception": None
                }
            )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )

class MilestoneSubmissionView(APIView):
    permission_classes = [IsAuthenticated & IsStudent]

    def post(self, request):
        try:
            # uploaded_file = request.FILES.get('file')
            # extension = uploaded_file.name.split('.')[-1].lower()
            # print(extension)
            # if extension not in ['zip', 'rar']:
            #     return Response({
            #         "status": 422,
            #         "message": "File must be a ZIP or RAR archive.",
            #         "body": {},
            #         "exception": "File type not supported."
            #         }
            #     )
            mil = milestone.objects.get(id=request.data.get('milestone_id'), deleted_at=None)
            t = mil.milestone_name
            defend_date = mil.document_submission_date
            current_date = date.today()
            difference = current_date - defend_date
            if difference.days > 0:
                time_status = "late"
            else:
                time_status = "ontime"
            options = UploadFileRequestOptions(
                use_unique_file_name=False,
                tags=['abc', 'def'],
                folder=f"/milestone/work/{t}/",
            )
            with request.FILES['file'].open("rb") as file:
                file = base64.b64encode(file.read())
            # Upload the file to ImageKit
            upload_response = imagekit.upload_file(
                file=file,
                file_name=f"{request.FILES['file'].name}",
                options=options
            )
            try:
                milestone_work = MilestoneWork.objects.get(project=request.data.get("project_id"), milestone=request.data.get("milestone_id"), deleted_at=None)
                milestone_work.title=request.data.get("title")
                milestone_work.description=request.data.get("description")
                milestone_work.project=project.objects.get(id=request.data.get("project_id"))
                milestone_work.milestone=milestone.objects.get(id=request.data.get("milestone_id"))
                milestone_work.document=upload_response.url
                milestone_work.time_status = time_status
                milestone_work.save()
                return Response({
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
            except:
                MilestoneWork.objects.create(
                    milestone=milestone.objects.get(id=request.data.get("milestone_id")),
                    title=request.data.get("title"),
                    description=request.data.get("description"),
                    project=project.objects.get(id=request.data.get("project_id")),
                    document=upload_response.url
                )
                return Response({
                    "status": 200,
                    "message": "Success",
                    "body": {},
                    "exception": None
                    }
                )
        except Exception as e:
            return Response({
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e)
                }
            )


class givemarksView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor)]
    
    def post(self, request):
        try:
            pro = project.objects.get(id=request.data.get("project"), deleted_at=None)
            if pro.status == "completed":
                return Response(
                    {
                    "status": 200,
                    "message": "Project is completed You cannot mark it",
                    "body": {},
                    "exception": None
                    }
                )
            else:
                mil = milestone.objects.get(id=request.data.get("milestone"), deleted_at=None)
                defend_date = mil.milestone_defending_date
                current_date = date.today()
                difference = current_date - defend_date
                if difference.days >= 0:
                    marks = mil.marks
                    in_marks = request.data.get("marks")
                    if in_marks > marks:
                        return Response(
                        {
                        "status": 200,
                        "message": f"Marks should be less then or equal to {marks}",
                        "body": {},
                        "exception": None
                        }
                    )
                    mk = Milestonemarks.objects.filter(project=request.data.get("project"),milestone=request.data.get("milestone"), m_distributor=request.data.get("m_distributor"), deleted_at=None)
                    if len(mk) > 0:
                        return Response(
                            {
                            "status": 200,
                            "message": "This form is allowed once submission",
                            "body": {},
                            "exception": None
                            }
                        )
                    else:
                        serialize = milestonemarkSerializer(data=request.data)
                        if serialize.is_valid():
                            serialize.save()
                            return Response(
                                {
                                "status": 200,
                                "message": "Success",
                                "body": {},
                                "exception": None
                                }
                            )
                        else:
                            return Response(
                                {
                                "status": 422,
                                "message": serialize.errors,
                                "body": {},
                                "exception": "some exception"
                                }
                            )
                else:
                    return Response(
                        {
                        "status": 200,
                        "message": f"You have to give marks after and at {defend_date} milestone defending date. Not allowed today.",
                        "body": {},
                        "exception": None
                        }
                    )
        except Exception as e:
          return Response(       
                {
                "status": 404,
                "message": "some exception",
                "body": {},
                "exception": str(e) 
                }
            )

class marksView(APIView):
    permission_classes = [IsAuthenticated & (IsFYPPanel | IsSupervisor | IsStudent)]

    def get(self, request):
        try:
            project_id = request.GET.get("project_id")
            project_obj = project.objects.filter(id=project_id, deleted_at=None).first()
            if not project_obj:
                return Response({
                    "status": 400,
                    "message": "Invalid project ID",
                    "body": {},
                    "exception": None
                })

            milestone_marks = Milestonemarks.objects.filter(project=project_obj, deleted_at=None)
            milestone_marks_dict = {}
            for milestone_mark in milestone_marks:
                if milestone_mark.milestone_id not in milestone_marks_dict:
                    milestone_marks_dict[milestone_mark.milestone_id] = []
                milestone_marks_dict[milestone_mark.milestone_id].append(milestone_mark.marks)

            milestone_averages = []
            for milestone_id, marks_list in milestone_marks_dict.items():
                milestone_obj = milestone.objects.filter(id=milestone_id, deleted_at=None).first()
                if not marks_list:
                    milestone_averages.append({milestone_obj.milestone_name: None})
                else:
                    milestone_averages.append({milestone_obj.milestone_name: sum(marks_list) / len(marks_list)})

            milestone_marks_list = [{"title": list(d.keys())[0], "marks": list(d.values())[0]} for d in milestone_averages]

            return Response({
                "status": 200,
                "message": "Success",
                "data": milestone_marks_list,
                "body": {},
                "exception": None
            })

        except Exception as e:
            return Response({
                "status": 404,
                "message": "Some exception occurred",
                "body": {},
                "exception": str(e)
            })
