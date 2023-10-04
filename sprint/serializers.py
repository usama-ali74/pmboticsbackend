from rest_framework import serializers
from .models import Sprint, Ticket, TicketLog
from core.models import project, milestone, User

class sprintSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    project = serializers.PrimaryKeyRelatedField(queryset=project.objects.all())
    milestone = serializers.PrimaryKeyRelatedField(queryset=milestone.objects.all())
    

    class Meta:
        model = Sprint
        fields = ['id', 'project', 'milestone', 'title', 'start_date', 'end_date']

class ticketSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    sprint = serializers.PrimaryKeyRelatedField(queryset=Sprint.objects.all())    
    status = serializers.CharField()
    # github_link = serializers.CharField()
    creator_name = serializers.PrimaryKeyRelatedField(read_only = True, source='creator.name')
    assignee_name = serializers.PrimaryKeyRelatedField(read_only = True, source='assignee.name')

    class Meta:
        model = Ticket
        # fields = "__all__"
        fields = ['id', 'sprint', 'title', 'description', 'start_date', 'end_date', 'assignee', 'creator', 'assignee_name', 'creator_name', 'status', 'github_link', 'time_status']


    def create(self, validated_data):
        ticket = super().create(validated_data)

        # Create log entry for ticket creation
        TicketLog.objects.create(
            ticket=ticket,
            to_status=ticket.status,
            from_status=ticket.status,
            github_link = ticket.github_link,
            mover=ticket.creator
        )
        return ticket

    def update(self, instance, validated_data):
        ticket = super().update(instance, validated_data)

        # Create log entry for ticket update
        from_status = Ticket.objects.get(id=instance.id).status
        TicketLog.objects.create(
            ticket=ticket,
            to_status=ticket.status,
            from_status=from_status,
            github_link=ticket.github_link,
            mover=ticket.creator
        )

        return ticket

    def destroy(self, instance):
        # Create log entry for ticket deletion
        TicketLog.objects.create(
            ticket=instance,
            to_status=None,
            from_status=instance.status,
            mover=instance.creator,
            github_link=instane.github_link
        )

        instance.delete()