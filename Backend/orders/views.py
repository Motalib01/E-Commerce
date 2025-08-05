# pylint: disable=no-member
# orders/views.py

# orders/views.py

from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(client=request.user).prefetch_related("items__product")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

# orders/views.py

# orders/views.py

import datetime
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseBadRequest
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from .models import Order, User


def oauth2_callback(request):
    if 'oauth_state' not in request.session:
        return HttpResponseBadRequest("OAuth state missing or expired.")

    # Step 1: Complete OAuth flow
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        state=request.session['oauth_state'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Step 2: Create Google Sheet
    sheets_service = build('sheets', 'v4', credentials=credentials)
    today = datetime.date.today()
    spreadsheet = sheets_service.spreadsheets().create(
        body={"properties": {"title": f"Orders Export - {today.isoformat()}"}} ,
        fields='spreadsheetId'
    ).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']

    # Step 3: Get today's orders with related items and products
    start = datetime.datetime.combine(today, datetime.time.min)
    end = datetime.datetime.combine(today, datetime.time.max)

    orders = (
        Order.objects
        .filter(created_at__range=(start, end))
        .select_related('client')
        .prefetch_related('items__product')
    )

    # Step 4: Prepare rows to insert
    sheet_data = [["Order ID", "Client Name", "Client Email", "Client Phone", "Created At", "Is Sent", "Product", "Quantity"]]

    for order in orders:
        client = order.client
        for item in order.items.all():
            sheet_data.append([
                order.id,
                client.name,
                client.email,
                client.phone,
                order.created_at.strftime("%Y-%m-%d %H:%M"),
                "Yes" if order.is_sent else "No",
                item.product.name,
                item.quantity
            ])

    # Step 5: Upload to Google Sheets
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        body={'values': sheet_data}
    ).execute()

    # Step 6: Redirect to created sheet
    return redirect(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

# Add this back in views.py if it was removed

from google_auth_oauthlib.flow import Flow

def oauth2_init(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['oauth_state'] = state
    return redirect(authorization_url)

