import urllib.request
import urllib.parse
import re

# Base URL of the local Flask application
BASE_URL = 'http://127.0.0.1:5000'

def get_page(path, cookies=None):
    """Sends a GET request and returns status code, html content, and cookies."""
    req = urllib.request.Request(f'{BASE_URL}{path}')
    if cookies:
        req.add_header('Cookie', cookies)
    try:
        response = urllib.request.urlopen(req)
        resp_cookies = response.headers.get('Set-Cookie', '')
        return response.status, response.read().decode('utf-8'), resp_cookies
    except Exception as e:
        return getattr(e, 'code', 500), str(e), ''

def extract_csrf_token(html):
    """Extracts CSRF token value from HTML."""
    match = re.search(r'id="csrf_token"[^>]*value="([^"]+)"', html)
    if not match:
        match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    return match.group(1) if match else None

def post_form(path, data, cookies=None):
    """Sends a POST request with optional cookies."""
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}{path}', data=encoded_data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    if cookies:
        req.add_header('Cookie', cookies)
    try:
        response = urllib.request.urlopen(req)
        resp_cookies = response.headers.get('Set-Cookie', '')
        return response.status, response.read().decode('utf-8'), resp_cookies
    except Exception as e:
        body = str(e)
        if hasattr(e, 'read'):
            try:
                body = e.read().decode('utf-8')
            except:
                pass
        return getattr(e, 'code', 500), body, ''

def run_verification():
    session_cookie = None

    print("--- Verifying Dashboard page ---")
    status, html, cookies = get_page('/')
    if cookies:
        session_cookie = cookies.split(';')[0]
    print(f"GET / Status: {status}")
    if "Welcome to Placement PrepTracker" in html:
        print("Dashboard loaded successfully.")
    
    print("\n--- Verifying Companies CRUD ---")
    status, html, cookies = get_page('/companies/', session_cookie)
    if cookies:
        session_cookie = cookies.split(';')[0]
    
    # Get form
    status, html, cookies = get_page('/companies/new', session_cookie)
    if cookies:
        session_cookie = cookies.split(';')[0]
    company_csrf = extract_csrf_token(html)
    
    company_id = -1
    if company_csrf:
        # Create company
        post_data = {
            'csrf_token': company_csrf,
            'name': 'Google LLC',
            'role': 'Associate Engineer',
            'status': 'Applied',
            'application_date': '2026-08-30',
            'notes': 'Test run creation notes.'
        }
        status, html, cookies = post_form('/companies/new', post_data, session_cookie)
        if cookies:
            session_cookie = cookies.split(';')[0]
        print(f"POST /companies/new Status: {status}")
        
        # Check if listed and extract company ID dynamically
        _, list_html, _ = get_page('/companies/', session_cookie)
        if 'Google LLC' in list_html:
            print("SUCCESS: Company Google LLC created.")
            # Search for the edit link of Google LLC to extract its ID
            # In the table, we look for /companies/<id>/edit
            matches = re.findall(r'href="/companies/(\d+)/edit"', list_html)
            if matches:
                # Use the latest company ID
                company_id = int(matches[-1])
                print(f"Extracted Company ID dynamically: {company_id}")
        else:
            print("FAILURE: Company Google LLC not found.")
    else:
        print("Failed to get CSRF for company creation.")
        return

    print("\n--- Verifying Tasks CRUD ---")
    # Verify index
    status, html, cookies = get_page('/tasks/', session_cookie)
    if cookies:
        session_cookie = cookies.split(';')[0]
    print(f"GET /tasks/ Status: {status}")
    if "No Preparation Tasks Yet" in html or "Preparation Tasks" in html:
        print("Tasks index page loads correctly.")

    # Get task form
    status, html, cookies = get_page('/tasks/new', session_cookie)
    if cookies:
        session_cookie = cookies.split(';')[0]
    task_csrf = extract_csrf_token(html)
    print(f"GET /tasks/new Status: {status}")
    print(f"Task CSRF token extracted: {task_csrf is not None}")

    task_id = -1
    if task_csrf:
        # Create task linked to the dynamically found company ID
        task_data = {
            'csrf_token': task_csrf,
            'title': 'LeetCode Arrays Practice',
            'description': 'Solve 5 array questions.',
            'category': 'DSA',
            'due_date': '2026-08-30',
            'status': 'Pending',
            'company_id': company_id
        }
        status, html, cookies = post_form('/tasks/new', task_data, session_cookie)
        if cookies:
            session_cookie = cookies.split(';')[0]
        print(f"POST /tasks/new Status: {status}")

        # Check if listed and extract task ID dynamically
        _, list_html, _ = get_page('/tasks/', session_cookie)
        if 'LeetCode Arrays Practice' in list_html:
            print("SUCCESS: Task created and linked to company successfully!")
            # Extract task ID from edit / delete / complete links
            matches = re.findall(r'href="/tasks/(\d+)/edit"', list_html)
            if not matches:
                # Try finding in forms
                matches = re.findall(r'action="/tasks/(\d+)/(?:complete|delete)"', list_html)
            if matches:
                task_id = int(matches[-1])
                print(f"Extracted Task ID dynamically: {task_id}")
        else:
            print("FAILURE: Task not listed or not linked.")
            print("Response:", html[:500])

        if task_id != -1:
            # Complete task
            print("\n--- Testing Complete Task Route ---")
            list_csrf = extract_csrf_token(list_html)
            if list_csrf:
                status, html, cookies = post_form(f'/tasks/{task_id}/complete', {'csrf_token': list_csrf}, session_cookie)
                if cookies:
                    session_cookie = cookies.split(';')[0]
                print(f"POST /tasks/{task_id}/complete Status: {status}")
                
                # Verify status in list
                _, list_html, _ = get_page('/tasks/', session_cookie)
                if 'Completed' in list_html:
                    print("SUCCESS: Task successfully marked as Completed!")
                else:
                    print("FAILURE: Task status did not update.")
            else:
                print("Failed to get CSRF for task completion.")

            # Check dashboard stats
            print("\n--- Checking Dashboard Stats ---")
            status, dash_html, _ = get_page('/', session_cookie)
            if 'Completed Tasks' in dash_html:
                print("SUCCESS: Dashboard statistics page loaded successfully.")
                # Print stats summary lines for manual review
                print("Stats indicators:")
                for line in dash_html.split('\n'):
                    if 'stat-card-value' in line:
                        print("Value:", line.strip())
            else:
                print("FAILURE: Dashboard stats did not render.")

            # Edit task
            print("\n--- Editing Task ---")
            status, edit_html, cookies = get_page(f'/tasks/{task_id}/edit', session_cookie)
            if cookies:
                session_cookie = cookies.split(';')[0]
            edit_csrf = extract_csrf_token(edit_html)
            if edit_csrf:
                edit_task_data = {
                    'csrf_token': edit_csrf,
                    'title': 'LeetCode Arrays Practice - Advanced',
                    'description': 'Solve hard questions.',
                    'category': 'DSA',
                    'due_date': '2026-08-31',
                    'status': 'In Progress',
                    'company_id': -1
                }
                status, html, cookies = post_form(f'/tasks/{task_id}/edit', edit_task_data, session_cookie)
                if cookies:
                    session_cookie = cookies.split(';')[0]
                print(f"POST /tasks/{task_id}/edit Status: {status}")

                # Verify list updates
                _, list_html, _ = get_page('/tasks/', session_cookie)
                if 'LeetCode Arrays Practice - Advanced' in list_html and 'In Progress' in list_html:
                    print("SUCCESS: Task edited and updated successfully!")
                else:
                    print("FAILURE: Task edits not reflected.")
            else:
                print("Failed to get CSRF for editing task.")

            # Delete task
            print("\n--- Deleting Task ---")
            _, list_html, cookies = get_page('/tasks/', session_cookie)
            if cookies:
                session_cookie = cookies.split(';')[0]
            delete_csrf = extract_csrf_token(list_html)
            if delete_csrf:
                status, html, cookies = post_form(f'/tasks/{task_id}/delete', {'csrf_token': delete_csrf}, session_cookie)
                if cookies:
                    session_cookie = cookies.split(';')[0]
                print(f"POST /tasks/{task_id}/delete Status: {status}")
                
                # Verify deleted
                _, list_html, _ = get_page('/tasks/', session_cookie)
                if 'LeetCode Arrays Practice - Advanced' not in list_html:
                    print("SUCCESS: Task successfully deleted!")
                else:
                    print("FAILURE: Task still listed.")
            else:
                print("Failed to get CSRF for task deletion.")
        else:
            print("Aborting Task operations test: Task ID could not be extracted.")

if __name__ == '__main__':
    run_verification()
