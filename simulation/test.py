#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by gongxingfa on 16/3/15

import random


def random_mac():
    mac_list = []
    for i in range(1, 7):
        randstr = "".join(random.sample("0123456789abcdef", 2))
        mac_list.append(randstr)

    rand_mac = ":".join(mac_list)
    return rand_mac

print random_mac()