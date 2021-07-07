from django.shortcuts import render
from django.http import HttpRequest
from core.forms import SubscribersForm
from core.sub_logger import logger
from core.tasks import (
    email_validity_check, generate_names, send_welcome_email_task
)
from django.shortcuts import redirect
from throttle.decorators import throttle


# Create your views here.
def index(request):
    """Renders the index page."""
    assert isinstance(request, HttpRequest)
    logger.info("index_view: Request")

    subscriber_names, no_of_subscribers = generate_names()

    return render(
        request,
        'index.html',
        {
            'title': 'Welcome',
            'names': subscriber_names,
            'len_names': no_of_subscribers
        }
    )


@throttle(zone='default')
def reserve(request):
    assert isinstance(request, HttpRequest)
    logger.info("reserve_view: Request")

    subscribers_form = SubscribersForm(request.POST or None)

    if subscribers_form.is_valid():
        logger.info("reserve_view: Valid Form")
        message = ""

        email = subscribers_form.cleaned_data['email']
        name = subscribers_form.cleaned_data['name']

        name = name.split()[0]
        name = name.capitalize()  # Capitalize the name

        # Check email validity
        email_validity = email_validity_check(email)

        if email_validity is True:
            logger.info("reserve_view: Valid Email Submission")

            subscribers_form.save()

            """Send welcome email in the background."""
            send_welcome_email_task.delay(
                email, name
            )

            message_A = "Congratulations {}! An email has been sent to ".format(name)
            message_B = "{} confirming your secured spot. See you soon!".format(email)
            message = message_A + message_B
        else:
            logger.info("reserve_view: Suspicious Email {}".format(email))
            message = (
                "Something is fishy about this email..." +
                " Did you type you email address correctly?"
            )

        # Save message to session
        request.session['message'] = message

        logger.info("reserve_view: Redirect Request")
        return redirect(info)

    return render(
        request,
        'subscribe.html',
        {
            'title': 'Reservation',
            'form': subscribers_form
        }
    )


# Create your views here.
def info(request):
    """Renders the index page."""
    assert isinstance(request, HttpRequest)
    logger.info("info_view: Request")

    try:
        message = request.session['message']
    except Exception as e:
        logger.error("info_view: {}".format(e.__class__))
        logger.info("info_view: Redirect Request")

        return redirect(reserve)

    return render(
        request,
        'info.html',
        {
            'title': 'Message',
            'message': message
        }
    )


def page_not_found(request, exception=None):
    error = 404
    logger.error('An Error: {}'.format(error))
    message = (
        "The page you requested does not exist. " +
        "If you're lost, just click the button below."
    )

    return render(
        request,
        'info.html',
        {
            'title': 'Page Not Found',
            'message': message
        }
    )


def server_side_error(request, exception=None):
    error = 500
    logger.error('server_side_error view: {}'.format(error))
    message = (
        "Its not you, its me... " +
        "It looks like a problem occurred on our server"
    )

    return render(
        request,
        'info.html',
        {
            'title': 'Server Error',
            'message': message
        }
    )


def bad_request(request, exception=None):
    error = 400
    logger.error('bad_request view: {}'.format(error))
    message = (
        "Something is fishy about your request... " +
        "Click the button below to go back."
    )

    return render(
        request,
        'info.html',
        {
            'title': 'Bad Request',
            'message': message
        }
    )


def permission_denied(request, exception=None):
    error = 403
    logger.error('permission_denied view: {}'.format(error))
    message = (
        "You're either making too many requests to this page or " +
        "do not have permissions to access it. " +
        "Please try again after a few minutes."
    )

    return render(
        request,
        'info.html',
        {
            'title': 'Permission Denied',
            'message': message
        }
    )
