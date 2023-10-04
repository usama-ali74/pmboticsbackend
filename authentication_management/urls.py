from django.urls import path
from .views import RegisterUserAPIView, LoginUserApi, Validate_otpAPI, allfyppanelApi
from project.views import projectAPIView, projectlistAPI, updateprojectAPI, deleteprojectAPI, addteammemberAPI, allprojectAPI, changesupervisorAPI, studentprojectwiseAPI, markasCompletedApi
from milestone.views import createmilestoneAPI, allmilestoneAPI, updatemilestoneAPI, deletemilestoneAPI, GetAllMilestones, SubmissionView, MilestoneSubmissionView, marksView, givemarksView
from supervisor.views import supervisorView
from department.views import departmentAPI
from notifications.views import createnotificationAPI, allnotificationsAPI, getallnotificationsAPI, deletenotificationAPI, updatenotificationAPI
from teamMember.views import RegisterteamMemberAPIView
from user_management.views import CreateUserView, allusersAPI, updatesupervisorAPI, studentlistAPI, deletesupervisorAPI, updatestudentAPI, deletestudentAPI
from sprint.views import createsprintAPI, updatesprintAPI, deletesprintAPI, getspecificsprintAPI, allsprintAPI, createticketAPI, allticketAPI, deleteticketAPI, updateticketAPI, getspecificticketAPI, ticketlogAPI, ProjectStatusAPI, ticketAPI, supervisorsprintAPI, studentticketAPI


urlpatterns = [
  path('registerpmo',RegisterUserAPIView.as_view()),
  path('login', LoginUserApi.as_view()),
  path('departmentcrud',departmentAPI.as_view()),
  path('createUser', CreateUserView.as_view()),
  path('alluser/', allusersAPI.as_view()),
  path('updatesupervisor', updatesupervisorAPI.as_view()),
  path('deletesupervisor/<int:pk>', deletesupervisorAPI.as_view()),
  path('studentlist',studentlistAPI.as_view()),
  path('updatestudent', updatestudentAPI.as_view()),
  path('deletestudent/<int:pk>', deletestudentAPI.as_view()),
  path('createproject',projectAPIView.as_view()),
  path('updateproject',updateprojectAPI.as_view()),
  path('projectlist',projectlistAPI.as_view()),
  path('projects',allprojectAPI.as_view()),
  path('studentprojectwise', studentprojectwiseAPI.as_view()),
  path('changesupervisor', changesupervisorAPI.as_view()),
  path('deleteproject/<int:pk>',deleteprojectAPI.as_view()),
  path('addteammember',addteammemberAPI.as_view()),
  path('createmilestone',createmilestoneAPI.as_view()),
  path('allmilestone', allmilestoneAPI.as_view()),
  path('updatemilestone',updatemilestoneAPI.as_view()),
  path('deletemilestone/<int:pk>', deletemilestoneAPI.as_view()),
  path('getallmilestone', GetAllMilestones.as_view()),
  path('createnotification',createnotificationAPI.as_view()),
  path('allnotifications', allnotificationsAPI.as_view()),
  path('getallnotifications', getallnotificationsAPI.as_view()),
  path('deletenotification/<int:pk>', deletenotificationAPI.as_view()),
  path('updatenotification', updatenotificationAPI.as_view()),
  path('createsprint', createsprintAPI.as_view()),
  path('updatesprint',updatesprintAPI.as_view()),
  path('deletesprint', deletesprintAPI.as_view()),
  path('getspecificsprint', getspecificsprintAPI.as_view()),
  path('allsprint', allsprintAPI.as_view()),
  path('createticket', createticketAPI.as_view()),
  path('allticket', allticketAPI.as_view()),
  path("deleteticket/<int:pk>",deleteticketAPI.as_view()),
  path("updateticket", updateticketAPI.as_view()),
  path('getspecificticket', getspecificticketAPI.as_view()),
  path('ticketlog', ticketlogAPI.as_view()),
  path("work", SubmissionView.as_view()),
  path("submitwork", MilestoneSubmissionView.as_view()),
  path("marks", marksView.as_view()),
  path('givemarks', givemarksView.as_view()),
  path('valotp', Validate_otpAPI.as_view()),
  path('allfyppanel', allfyppanelApi.as_view()),
  path('projectstatus', ProjectStatusAPI.as_view()),
  path('ticket', ticketAPI.as_view()),
  path('supervisorsprint', supervisorsprintAPI.as_view()),
  path('markasCompleted', markasCompletedApi.as_view()),
  path('studentticket', studentticketAPI.as_view()),
]
