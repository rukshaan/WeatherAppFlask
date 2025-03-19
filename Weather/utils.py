# # utils.py
# from functools import wraps
# from flask import redirect, url_for, session

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:  # Check if user is logged in
#             return redirect(url_for('auth.login'))  # Redirect to login page if not logged in
#         return f(*args, **kwargs)
#     return decorated_function


# <div class="col-lg-4 col-md-4 col-xs-4" style="margin-right: 650px;">
# 								<button aria-expanded="false" type="submit" class="btn btn-primary">
# 									<span>Add City</span>
# 								</button>
# 							</div>
# 							<div class="col-lg-5 col-md-5 col-xs-5 d-flex">
# 								<a href="javascript:void(1);" onclick="logout()" class="btn btn-success mr-2">
# 									Name
# 								</a>
# 								<a href="javascript:void(0);" onclick="logout()" class="btn btn-danger ">
# 									log out
# 								</a>
# 							</div>