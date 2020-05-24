#!/usr/bin/env python

from urllib.request import urlopen

urlopen("https://dynamicdns.park-your-domain.com/update?"
        "host={}"
        "&domain={}"
        "&password={}"
        .format("@", "Your_Domain_Name", "Your_Namecheap_Dynamic_DNS_Passwd"))
