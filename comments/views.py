from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentCreateSerializer, CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
	queryset = Comment.objects.select_related('account', 'post').all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = CommentCreateSerializer(data=request.data)
		if not serializer.is_valid():
			print("Serializer errors:", serializer.errors)
			return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

		comment = serializer.save(account=request.user)
		return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Comment.objects.select_related('account', 'post').all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def update(self, request, *args, **kwargs):
		comment = self.get_object()
		if comment.account != request.user:
			return Response({"message": "You are not owner of this comment"}, status=status.HTTP_403_FORBIDDEN)

		partial = kwargs.pop('partial', False)
		serializer = CommentCreateSerializer(comment, data=request.data, partial=partial)
		if not serializer.is_valid():
			return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

		serializer.save(account=comment.account)
		return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		comment = self.get_object()
		if comment.account != request.user:
			return Response({"message": "You are not owner of this comment"}, status=status.HTTP_403_FORBIDDEN)
		return super().destroy(request, *args, **kwargs)
