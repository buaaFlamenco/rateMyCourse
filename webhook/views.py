from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt

import hmac
import json
import os
import git


@csrf_exempt
def github(request):
    ''' Once received webhooks from github, pull the specifed branch if the hook means a push event on the target branch.
    Read SECRET_KEY from environment variables.
    '''
    # Check Method
    if request.method != "POST":
        return HttpResponse(status=405)

    # Parse Header
    event = request.META.get("HTTP_X_GITHUB_EVENT", "")
    signature = request.META.get("HTTP_X_HUB_SIGNATURE", "")

    # Check Event
    if event != "push":
        return Http404("Not registered event [{0}].".format(event))

    # Check Signature
    if not signature:
        return Http404("No signature.")
    sha_name, sha_sign = signature.split("=")
    if sha_name != "sha1":
        return Http404("Not registered sign method")

    mac = hmac.new(
        bytes(os.environ["SECRET_KEY"], encoding="utf-8"),
        msg=request.body, 
        digestmod="sha1")
    if not hmac.compare_digest(str(mac.hexdigest()), str(sha_sign)):
        return HttpResponseForbidden("Signature not match.")

    # Parse Body
    if not request.body:
        return Http404("No body.")
    body = json.loads(request.body)
    
    # Deploy Work
    # Here we just pull the master branch
    branch_name = "master"
    body_ref = body.get("ref", "")
    if not body_ref:
        return Http404("No ref in body.")
    exp_ref = "refs/heads/" + branch_name
    if body_ref == exp_ref:
        repo = git.Repo(".")
        remote = repo.remote()
        remote.pull(branch_name + ":" + branch_name)
        return HttpResponse("Pull the branch " + branch_name)
    else:
        return HttpResponse("Not target branch " + branch_name)