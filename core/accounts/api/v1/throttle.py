from action_throttle.rest import ActionThrottle


class UserActionThrottle(ActionThrottle):
    user_ip_limit = 'user_action_throttle'
