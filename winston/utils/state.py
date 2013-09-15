import ping

def device_is_present(host, tries=3, timeout=3):
    """
    Determines whether a device is present on the network
    using its IP address or hostname. If the device can be
    pinged successfully, it will return True, and False
    otherwise.

    Winston needs to run as root to use this function, since
    ICMP pings need root to run. That is even true for the
    ping command, so there is no way to circumvent this.

    See this post for details:
    http://stackoverflow.com/questions/1189389/python-non-privileged-icmp

    :param host: hostname or IP address
    :param tries: number of tries before giving up
    :param timeout: timeout in seconds
    """
    try:
        response = ping.quiet_ping(host, tries, timeout)

        # Returns true if more than 0% of packets were returned
        return (response[0] > 0)
    except:
        return False