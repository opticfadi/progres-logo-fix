from mitmproxy import http
import json

etablissement_id = None
pending_logo_requests = []  # store flows waiting for ID

def response(flow: http.HTTPFlow):
    global etablissement_id, pending_logo_requests

    # capture etablissementId from /dias
    if flow.request.pretty_url.endswith("/dias"):
        try:
            data = json.loads(flow.response.get_text())
            if isinstance(data, list) and data:
                etablissement_id = str(data[0].get("etablissementId"))
                print(f"captured etablissementId: {etablissement_id}")

                # process any pending logo requests
                for pending_flow in pending_logo_requests:
                    fix_logo_request(pending_flow)
                    pending_flow.resume()  # let it go through now
                pending_logo_requests.clear()

        except Exception as e:
                print(f"failed to parse /dias response: {e}")

def request(flow: http.HTTPFlow):
    global etablissement_id, pending_logo_requests

    # intercepts /logoEtablissement/undefined (the endpoint that returns the logo)
    if flow.request.pretty_url.startswith("https://progres.mesrs.dz/api/infos/logoEtablissement/") \
       and flow.request.pretty_url.endswith("/undefined"):

        if etablissement_id:
            fix_logo_request(flow)
        else:
            print("no etablissementId yet, holding request until /dias response arrives")
            flow.pause()
            pending_logo_requests.append(flow)

def fix_logo_request(flow: http.HTTPFlow):
    """replaces undefined with the captured etablissementId"""
    global etablissement_id
    fixed_url = flow.request.pretty_url.replace("/undefined", f"/{etablissement_id}")
    flow.request.url = fixed_url
    print(f"reewrote the URL to: {fixed_url}")
