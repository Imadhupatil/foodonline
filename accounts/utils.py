

def detect_role(user):
  if user.role == 1:
    redirecURL = 'vendorDashboard'
    return redirecURL
  elif user.role == 2:
    redirecURL = 'custDashboard'
    return redirecURL
  elif user.role == None and user.is_superadmin:
    redirecURL = '/admin'
    return redirecURL