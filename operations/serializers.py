from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from choices import Vaccinations, Vaccine_names, Vaccine_status
from .models import Clinitian, Parent, Baby, VaccineSchedule, VaccineRecord, Appointment, HealthCare


class ClinitianSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Clinitian
		fields  = ('user', 'email', 'first_name', 'last_name', 'contact', 'unique_id', 'HealthCare')

class ClinitianViewset(viewsets.ModelViewSet):
	"""ClinitianViewset for REST Endpoint"""
	serializer_class 	= ClinitianSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			return Clinitian.objects.filter(user = user)
		else:
			return Clinitian.objects.none()

class ParentSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Parent
		fields  = ('id', 'user', 'email', 'first_name', 'last_name', 'address', 'contact', 'unique_id')

class ParentViewset(viewsets.ModelViewSet):
	"""ParentViewset for REST Endpoint"""
	serializer_class 	= ParentSerializer
	permission_classes 	= (IsAuthenticated,)
	queryset 			= Parent.objects.all()

class BabySerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= Baby
		fields  = ('id', 'first_name', 'last_name', 'tag', 'parent', 'place_of_birth', 'weight', 'blood_group', 'gender', 'birth_date', 'special_notes', 'text_notifications', 'week')

class BabyViewset(viewsets.ModelViewSet):
	"""BabyViewset for REST Endpoint"""
	serializer_class 	= BabySerializer
	permission_classes 	= (IsAuthenticated,)

	def get_queryset(self):
		user 		= self.request.user
		parent 		= Parent.objects.filter(user = user)
		if parent:
			return Baby.objects.filter(parent = parent)
		queryset 	= Baby.objects.all()
		tag 		= self.request.query_params.get('tag', None)
		email 		= self.request.query_params.get('email', None)
		contact		= self.request.query_params.get('contact', None)
		name 		= self.request.query_params.get('name', None)
		aadhaar 	= self.request.query_params.get('aadhaar', None)
		if tag is not None:
			queryset = Baby.objects.filter(tag__contains = tag)
		elif name is not None:
			queryset = Baby.objects.filter(first_name__contains = name) | Baby.objects.filter(last_name__contains = name) 
		elif email is not None:
			parent = Parent.objects.filter(email = email)
			queryset = Baby.objects.filter(parent = parent)
		elif contact is not None:
			parent = Parent.objects.filter(contact = contact)
			queryset = Baby.objects.filter(parent = parent)
		elif aadhaar is not None:
			parent = Parent.objects.filter(unique_id = aadhaar)
			print parent
			queryset = Baby.objects.filter(parent = parent)
		return queryset


class ParentList(generics.ListAPIView):
	serializer_class = ParentSerializer

	def get_queryset(self):
		"""
		This view should return a list of all the purchases
		for the currently authenticated user.
		"""
		user = self.request.user
		return Parent.objects.filter(user=user)



class VaccineScheduleSerializer(serializers.ModelSerializer):
	class Meta:	
		model 	= VaccineSchedule
		fields  = ('baby', 'vaccine', 'week', 'tentative_date', 'status')

	vaccine = serializers.SerializerMethodField()

	def get_vaccine(self, obj):
		vaccinations = dict(Vaccine_names)
		obj.vaccine = vaccinations[obj.vaccine]
		return obj.vaccine
	

class VaccineScheduleViewset(viewsets.ModelViewSet):
	"""VaccineScheduleViewset for REST Endpoint"""
	serializer_class 	= VaccineScheduleSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk = pk)
				return VaccineSchedule.objects.filter(baby = baby)
			else:
				VaccineSchedule.objects.none()
		else:
			return Parent.objects.none()



class VaccineRecordSerializer(serializers.ModelSerializer):
	class Meta:	
		model 				= VaccineRecord
		fields  			= ('id', 'appointment', 'vaccine', 'dose', 'status', 'amount')
		read_only_fields 	= ('id', 'appointment', 'vaccine', 'dose', 'status', 'amount')


	vaccine = serializers.SerializerMethodField()

	def get_vaccine(self, obj):
		vaccinations = dict(Vaccine_names)
		obj.vaccine = vaccinations[obj.vaccine]
		return obj.vaccine

class VaccineRecordViewset(viewsets.ModelViewSet):
	"""VaccineRecordViewset for REST Endpoint"""
	serializer_class 	= VaccineRecordSerializer
	permission_classes 	= (IsAuthenticated,)
	
	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				appointment = get_object_or_404(Appointment, pk = pk)
				if appointment is not None:
					return VaccineRecord.objects.filter(appointment = appointment)
				else:
					return VaccineRecord.objects.none()
			else:
				return VaccineRecord.objects.none()
		else:
			return VaccineRecord.objects.none()


class HealthCareSerializer(serializers.ModelSerializer):
	"""docstring for HealthCareSerializer"""
	class Meta:
		model 				= HealthCare
		fields 				= ('id', 'name', 'address', 'email', 'contact')
		read_only_fields 	= ('id', 'name', 'address', 'email', 'contact')

class HealthCareViewSet(viewsets.ModelViewSet):
	"""docstring for HealthCareViewSet"""
	serializer_class 	= HealthCareSerializer
	permission_classes  = (IsAuthenticated, )

	def get_queryset(self):
		pk = self.request.query_params.get('pk', None)
		if pk is not None:
			return HealthCare.objects.filter(pk = pk)
		else:
			return HealthCare.objects.all()

class AppointmentSerializer(serializers.ModelSerializer):
	administered_at = HealthCareSerializer(read_only=True)
	class Meta:	
		model 				= Appointment
		fields  			= ('id', 'baby', 'administered_at', 'administered_on')
		read_only_fields 	= ('id', 'administered_at', 'administered_on')

class AppointmentViewSet(viewsets.ModelViewSet):
	"""docstring for AppointmentViewSet"""
	serializer_class 	= AppointmentSerializer
	permission_classes 	= (IsAuthenticated, )

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated:
			pk = self.request.query_params.get('pk', None)
			if pk is not None:
				baby = get_object_or_404(Baby, pk = pk)
				if baby is not None:
					return Appointment.objects.filter(baby = baby)
				else:
					return VaccineRecord.objects.none()
			else:
				return VaccineRecord.objects.none()
		else:
			return VaccineRecord.objects.none()

	def perform_create(self, serializer):
		user = self.request.user
		if user.is_authenticated:
			clinitian = get_object_or_404(Clinitian, user = user)
			healthcare = clinitian.HealthCare
			serializer.save(administered_at=healthcare)

