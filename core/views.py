from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from firebase_admin import firestore

def home(request):
    return render(request, 'index.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def create_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'status': 'success', 'message': 'Request logged in backend', 'data': data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def register_volunteer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'status': 'success', 'message': 'Volunteer logged in backend', 'data': data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def run_matching(request):
    if request.method == 'POST':
        try:
            db = firestore.client()
            
            # Fetch pending requests
            requests_ref = db.collection('requests').where('status', '==', 'pending').stream()
            pending_requests = [{'id': doc.id, **doc.to_dict()} for doc in requests_ref]
            
            # Fetch available volunteers
            volunteers_ref = db.collection('volunteers').where('availability', '==', True).stream()
            available_volunteers = [{'id': doc.id, **doc.to_dict()} for doc in volunteers_ref]
            
            matches_made = 0
            
            for req in pending_requests:
                # Basic matching logic: Find a volunteer whose skills include the request type
                # (You can expand this with distance matching later)
                req_type = req.get('type', '').lower()
                
                matched_volunteer = None
                for vol in available_volunteers:
                    skills = [s.lower() for s in vol.get('skills', [])]
                    # If type is 'medical' and volunteer has 'medical', or if request type is 'other'
                    if req_type in skills or req_type == 'other' or any(req_type in s for s in skills):
                        matched_volunteer = vol
                        break
                
                if matched_volunteer:
                    vol_user_id = matched_volunteer.get('userId')
                    if not vol_user_id:
                        continue # Skip if volunteer data is invalid
                    
                    # 1. Create assignment record
                    assignment_data = {
                        'request_id': req['id'],
                        'volunteer_id': vol_user_id,
                        'status': 'assigned',
                        'created_at': firestore.SERVER_TIMESTAMP
                    }
                    db.collection('assignments').add(assignment_data)
                    
                    # 2. Update request status
                    db.collection('requests').document(req['id']).update({
                        'status': 'assigned',
                        'assignedVolunteerId': vol_user_id
                    })
                    
                    # Remove volunteer from available pool for this run
                    available_volunteers.remove(matched_volunteer)
                    matches_made += 1

            return JsonResponse({'status': 'success', 'message': f'Matching complete. {matches_made} new assignments made.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def my_requests(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'user_id is required'}, status=400)
        
    try:
        db = firestore.client()
        reqs = db.collection('requests').where('userId', '==', user_id).stream()
        data = [{'id': doc.id, **doc.to_dict()} for doc in reqs]
        # Firestore timestamps are not JSON serializable by default, so we convert them if needed
        # But for simple GET, we can just stringify them or ignore them if not strict. 
        # For safety, clean up datetime objects:
        for d in data:
            if 'createdAt' in d and hasattr(d['createdAt'], 'isoformat'):
                d['createdAt'] = d['createdAt'].isoformat()
                
        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def my_tasks(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'user_id is required'}, status=400)
        
    try:
        db = firestore.client()
        # Fetch assignments where volunteer_id == user_id
        assignments = db.collection('assignments').where('volunteer_id', '==', user_id).stream()
        
        tasks_data = []
        for assign_doc in assignments:
            assignment = assign_doc.to_dict()
            request_id = assignment.get('request_id')
            
            # Fetch the actual request details for the UI
            req_doc = db.collection('requests').document(request_id).get()
            if req_doc.exists:
                req_data = req_doc.to_dict()
                if 'createdAt' in req_data and hasattr(req_data['createdAt'], 'isoformat'):
                    req_data['createdAt'] = req_data['createdAt'].isoformat()
                    
                tasks_data.append({
                    'assignment_id': assign_doc.id,
                    'request_id': request_id,
                    'status': assignment.get('status'),
                    'request_details': req_data
                })
                
        return JsonResponse({'status': 'success', 'data': tasks_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

