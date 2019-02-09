# -*- coding: utf-8 -*-
from plone import api


def creator_converter(userid):
    """return the fullname of the user"""
    membership = api.portal.get_tool('portal_membership')
    user_info = membership.getMemberInfo(userid)
    converted = ''
    if user_info:
        converted = user_info['fullname'] or user_info['username']
    return converted or userid
