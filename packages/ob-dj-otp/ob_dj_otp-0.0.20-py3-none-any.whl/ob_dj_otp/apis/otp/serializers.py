import logging
import typing
from datetime import timedelta

from celery import current_app
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ob_dj_otp.core.otp.models import OneTruePairing

logger = logging.getLogger(__name__)


class OTPRequestCodeSerializer(serializers.ModelSerializer):
    """ Serializer for processing payloads for requesting an OTP Code
    for both registration and authentication;
    """

    phone_number = PhoneNumberField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OneTruePairing
        fields = ("phone_number", "status", "verification_code", "usage")
        extra_kwargs = {
            "verification_code": {"write_only": True, "required": False},
            "usage": {"read_only": True},
        }

    def get_status(self, obj: OneTruePairing) -> typing.Text:
        if obj.status == OneTruePairing.Statuses.init:
            return _("Verification code sent to phone number.")

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        phone_number = attrs["phone_number"]
        try:
            # Validate if user with same phone number exists for auth
            # TODO: `phone_number` configurable via settings with `phone_number` as default attr name
            user = get_user_model().objects.get(phone_number=phone_number)
            attrs["usage"] = OneTruePairing.Usages.auth
            attrs["user"] = user
        except ObjectDoesNotExist as e:
            if settings.OTP_AUTH_USAGE_ONLY:
                raise serializers.ValidationError(_("Invalid phone number.")) from e
            attrs["usage"] = OneTruePairing.Usages.register

        # Validate there is unused OTP code
        timeout = now() - timedelta(seconds=settings.OTP_TIMEOUT)

        filter_kwargs = {
            "phone_number": phone_number,
            "status": OneTruePairing.Statuses.init,
            "created_at__gte": timeout,
            "usage": attrs["usage"],
        }
        if "user" in attrs:
            filter_kwargs["user"] = attrs["user"]

        if OneTruePairing.objects.filter(**filter_kwargs).exists():
            # TODO: Add a mechanism to force a new code request
            #       with additional `write_only` parameter
            logger.warning(
                f"User with phone_number {phone_number} requested OTP code twice."
            )
            # TODO: Add time count down
            raise serializers.ValidationError(
                _(
                    "We sent a verification code please wait for "
                    "2 minutes; before requesting a new code."
                )
            )
        return attrs

    def create(self, validated_data: typing.Dict) -> OneTruePairing:
        instance = OneTruePairing.objects.create(**validated_data)
        # IF OTP_FORCE_CODE not set; triggers message to the configured provider
        if not getattr(settings, "OTP_FORCE_CODE", False):
            transaction.on_commit(
                lambda: current_app.send_task(
                    "otp.send_sms_via_provider", args=[instance.id],
                )
            )
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        # TODO: Make default False
        if not getattr(settings, "OTP_RETURN_USAGE", True) and "usage" in data:
            del data["usage"]
        return data


class OTPVerifyCodeSerializer(OTPRequestCodeSerializer):
    """ Serializer for processing payloads for validating
    verification codes for authentication purposes;
    """

    phone_number = PhoneNumberField(write_only=True)
    created = serializers.BooleanField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True, source="user.role")

    class Meta:
        model = OneTruePairing
        fields = (
            "phone_number",
            "verification_code",
            "refresh",
            "access",
            "role",
            "created",
        )
        extra_kwargs = {
            "verification_code": {"write_only": True, "required": True},
            "phone_number": {"write_only": True, "required": True},
        }

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        try:
            timeout = now() - timedelta(seconds=settings.OTP_TIMEOUT)
            instance = OneTruePairing.objects.get(
                phone_number=attrs["phone_number"],
                verification_code=attrs["verification_code"],
                status=OneTruePairing.Statuses.init,
                created_at__gte=timeout,
            )
            self.context["otp"] = instance
            return attrs
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(
                _("Invalid verification code or phone_number.")
            ) from e

    def create(self, validated_data: typing.Dict) -> OneTruePairing:
        instance = self.context["otp"]
        instance.mark_used()
        user = instance.user
        instance.created = False
        if not (user or settings.OTP_AUTH_USAGE_ONLY):
            instance.created = True
            validated_data.pop("verification_code",)
            user = get_user_model().objects.create(**validated_data)
            instance.user = user
            instance.save()
        # TODO: Create Generic Provider for Authentication backends
        refresh = RefreshToken.for_user(user)
        instance.refresh = str(refresh)
        instance.access = str(refresh.access_token)
        return instance
