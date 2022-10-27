from django.test import TestCase
from django.core import mail
from constance.test import override_config

from api.email import mail_admins


@override_config(EMAIL_ADMIN="admin@apps.crnan")
class AdminMailTestCase(TestCase):

    def test_mail_admin(self):
        mail_admins("Test subject", "Test message",
                    from_email="from@apps.crnan")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[DIAPASON] Test subject")
        self.assertEqual(mail.outbox[0].body, "Test message")
        self.assertEqual(mail.outbox[0].to, ["admin@apps.crnan"])
        self.assertEqual(mail.outbox[0].from_email, "from@apps.crnan")

    def test_mail_admin_with_html(self):
        mail_admins("Test subject", "Test message",
                    html_message="<p>Test message</p>")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[DIAPASON] Test subject")
        self.assertEqual(mail.outbox[0].body, "Test message")
        self.assertEqual(mail.outbox[0].to, ["admin@apps.crnan"])
        self.assertEqual(mail.outbox[0].alternatives[0]
                         [0], "<p>Test message</p>")

    @override_config(EMAIL_SUBJECT_PREFIX="[TEST] ")
    def test_mail_subject_prefix(self):
        mail_admins("Test subject", "Test message")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[TEST] Test subject")

    @override_config(EMAIL_ADMIN="")
    def test_mail_subject_prefix(self):
        mail_admins("Test subject", "Test message")
        self.assertEqual(len(mail.outbox), 0)
